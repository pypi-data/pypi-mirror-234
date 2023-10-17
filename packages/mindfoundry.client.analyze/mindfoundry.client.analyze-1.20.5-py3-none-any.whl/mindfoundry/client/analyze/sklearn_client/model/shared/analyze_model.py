import abc
from datetime import datetime
from typing import List, Optional

import pandas as pd

from ....swagger.models import ModelResponse
from ....utils.typing import PathLike
from ...data_set import DataLike, DataSet
from ...prediction import Prediction
from ...test import Test
from .base import BaseModel


def _default_prediction_name() -> str:
    return f"Prediction from Python Client {datetime.utcnow().strftime('%Y/%m/%d %H:%M:%S')}"


class AnalyzeModel(abc.ABC):
    """Implements the shared methods that call into any internal model regardless of type"""

    def __init__(self, *, _internal_model: BaseModel):
        """Internal constructor - DO NOT USE"""
        self._internal_model = _internal_model

    ########################################################################
    # Methods used or extended by child models to return the correct types #
    ########################################################################

    def _fit(
        self,
        data: DataLike,
        target: str,
        excluded_columns: Optional[List[str]] = None,
        *,
        wait_until_complete: bool = True,
        # Classification and Regression specific fit parameters
        sample_weight: Optional[str] = None,
        order_by: Optional[str] = None,
        partition_by: Optional[str] = None,
        hold_out_percentage: Optional[float] = 10.0,
        no_mixing: Optional[List[str]] = None,
    ) -> "AnalyzeModel":
        """Internal method - DO NOT USE"""
        # Fit must explicitly override the model with the new fitted model
        self._internal_model = self._internal_model.fit(
            data,
            target,
            excluded_columns,
            order_by=order_by,
            partition_by=partition_by,
            no_mixing=no_mixing,
            sample_weight=sample_weight,
            hold_out_percentage=hold_out_percentage,
        )
        if wait_until_complete:
            self._internal_model.wait_until_fitted()
        return self

    ########################################################
    # Generic methods passed through to the internal model #
    ########################################################

    @property
    def model_id(self) -> int:
        """The ID of the model in Analyze"""
        return self._internal_model.model_id

    @property
    def is_fitting(self) -> bool:
        """Specifies whether the model is currently fitting"""
        return self._internal_model.is_fitting()

    @property
    def is_fitted(self) -> bool:
        """Specifies whether the model fitting has succeeded"""
        return self._internal_model.is_fitted()

    @property
    def has_failed_fitting(self) -> bool:
        """Specifies whether the model fitting has failed"""
        return self._internal_model.has_failed_fitting()

    def wait_until_fitted(self):
        """
        Sleep until the model has finished fitting
        """
        self._internal_model.wait_until_fitted()

    def save(self, path: PathLike) -> None:
        """
        Save the model to the specified path
        :param path: The path to which to save the file
        """
        self._internal_model.save(path)

    @property
    def info(self) -> ModelResponse:
        """Get information about the model"""
        return self._internal_model.model_info()

    @property
    def url(self) -> str:
        """Get the url of the model page in Analyze"""
        return self._internal_model.url()

    def predict(self, data) -> pd.Series:
        """
        Use the model to perform a prediction on the supplied data
        and return just the prediction
        :param data: The data to predict
        :return: A series containing the prediction for each row in the data, in the same order as the input data
        """
        return self.predict_object(data).prediction()

    def predict_object(
        self,
        data: DataLike,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        wait_until_complete: bool = True,
    ) -> Prediction:
        """
        Use the model to perform a prediction on the supplied data
        :param data: The data to use to perform the prediction
        :param name: The name to use for the prediction in Analyze
        :param description: The description to use for the prediction in Analyze
        :param wait_until_complete: If True, this method blocks until the model has been fitted and can be used for a prediction.
        :return: An object representing the prediction
        """
        return self._internal_model.predict(
            data,
            name=name or _default_prediction_name(),
            description=description,
            wait_until_complete=wait_until_complete,
        )

    def test(
        self,
        data: DataLike,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        wait_until_complete: bool = True,
    ) -> Test:
        """
        Use the model to perform a test on the supplied data
        :param data: The data to use to perform the test. This must include a column with the Target
        :param name: The name to use for the test in Analyze
        :param description: The description to use for the test in Analyze
        :param wait_until_complete: If True, this method blocks until the model has been fitted and can be used for a test.
        :return: An object representing the test
        """
        return self._internal_model.test(
            data,
            name=name,
            description=description,
            wait_until_complete=wait_until_complete,
        )

    def results_as_df(self) -> pd.DataFrame:
        """A data frame containing the model results data. For classification & regression this result is the result of hold-out
        test, for clustering it is the clustered data."""
        return self._internal_model.results_as_df()

    def save_results_as_dataset(
        self, *, name: Optional[str] = None, description: Optional[str] = None
    ) -> DataSet:
        """Save the model results data as a data set to allow use in other places in the system - For classification & regression
        this result is the result of hold-out test, for clustering it is the clustered data.
        """
        return self._internal_model.save_results_as_dataset(
            name=name, description=description
        )
