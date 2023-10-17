import abc
from typing import List, Optional

import pandas as pd

from ....swagger.models import ModelResponse
from ....utils.typing import PathLike
from ...data_set import DataLike, DataSet
from ...prediction import Prediction
from ...test import Test


class BaseModel(abc.ABC):
    @abc.abstractmethod
    def fit(
        self,
        data: DataLike,
        target: str,
        excluded_columns: Optional[List[str]] = None,
        *,
        # Classification and Regression specific fit parameters
        sample_weight: Optional[str] = None,
        order_by: Optional[str] = None,
        partition_by: Optional[str] = None,
        hold_out_percentage: Optional[float] = 10.0,
        no_mixing: Optional[List[str]] = None,
    ) -> "BaseModel":
        """Fit the model and return a fitted version"""

    @property
    @abc.abstractmethod
    def model_id(self) -> int:
        """The ID of the model in Analyze"""

    @abc.abstractmethod
    def is_fitting(self) -> bool:
        """Specifies whether the model is currently fitting"""

    @abc.abstractmethod
    def is_fitted(self) -> bool:
        """Specifies whether the model fitting has succeeded"""

    @abc.abstractmethod
    def has_failed_fitting(self) -> bool:
        """Specifies whether the model fitting has failed"""

    @abc.abstractmethod
    def save(self, path: PathLike) -> None:
        """Save the model to the specified path"""

    @abc.abstractmethod
    def model_info(self) -> ModelResponse:
        """Get information about the model"""

    @abc.abstractmethod
    def url(self) -> str:
        """Get the URL to the model page on Analyze"""

    @abc.abstractmethod
    def predict(
        self,
        data: DataLike,
        *,
        name: str,
        description: Optional[str],
        wait_until_complete: bool,
    ) -> Prediction:
        """Use the model to perform a prediction on the supplied data"""

    @abc.abstractmethod
    def test(
        self,
        data: DataLike,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        wait_until_complete: bool = True,
    ) -> Test:
        """Use the model to perform a test on the supplied data"""

    @abc.abstractmethod
    def wait_until_fitted(self):
        """Wait for the model to finish and return whether the fitting was successful"""

    @abc.abstractmethod
    def results_as_df(self) -> pd.DataFrame:
        """A data frame containing the model results data. For classification & regression this result is the result of hold-out
        test, for clustering it is the clustered data."""

    @abc.abstractmethod
    def save_results_as_dataset(
        self, *, name: Optional[str] = None, description: Optional[str] = None
    ) -> DataSet:
        """Save the model results data as a data set to allow use in other places in the system - For classification & regression
        this result is the result of hold-out test, for clustering it is the clustered data.
        """
