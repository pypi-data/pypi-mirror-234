import datetime
from io import BytesIO
from typing import List, Optional

import pandas as pd

from ....swagger.api.models import get_model_result_parquet_data, save_model_result
from ....swagger.models import ModelResponse, ModelStatus, SaveModelResultsRequest
from ....utils import CachedModelResponse, check_exists, wait_for_model_to_complete
from ....utils.typing import PathLike
from ...connection import (
    ConnectionLike,
    client_from_connectionlike,
    from_connectionlike,
)
from ...data_set import (
    DataLike,
    DataSet,
    get_dataset_from_datalike,
    load_data_set_from_server,
)
from ...prediction import Prediction
from ...test import Test
from ..serialization import SerializedModel, save_model
from .base import BaseModel


def _default_saved_results_dataset_name(name: str) -> str:
    return f"Saved Model results for {name} from Python Client {datetime.datetime.utcnow().strftime('%Y/%m/%d %H:%M:%S')}"


class RemoteModel(BaseModel):
    """
    A model that is saved to Analyze
    """

    def __init__(self, connection: ConnectionLike, model_id: int):
        self._model_id = model_id
        self._connection = from_connectionlike(connection)
        self._client = client_from_connectionlike(connection)
        self._cached_model_info = CachedModelResponse(self._client, self.model_id)

    @classmethod
    def from_serialized_model(cls, connection, serialized_model) -> "RemoteModel":
        if serialized_model.base_url != connection.base_url:
            raise Exception(
                "The connection and the model are from different instances of Analyze"
            )

        remote_model = RemoteModel(connection, serialized_model.model_id)

        if remote_model.model_info().project_id != serialized_model.project_id:
            raise Exception(
                "The connection and the model are from different projects within Analyze"
            )
        return remote_model

    @property
    def model_id(self) -> int:
        """The ID of the model in Analyze"""
        return self._model_id

    def is_fitting(self) -> bool:
        # Any remote model counts as 'fitting' for our purposes unless the computation has completed
        # Later we could split out the model having been saved from the model post-calculation
        return self.model_info().status not in (
            ModelStatus.COMPLETE,
            ModelStatus.FAILED,
        )

    def is_fitted(self) -> bool:
        return self.model_info().status == ModelStatus.COMPLETE

    def has_failed_fitting(self) -> bool:
        return self.model_info().status == ModelStatus.FAILED

    def wait_until_fitted(self):
        wait_for_model_to_complete(self._client, self.model_id)

    def save(self, path: PathLike) -> None:
        save_model(
            path,
            SerializedModel(
                base_url=self._connection.base_url,
                project_id=self.model_info().project_id,
                model_id=self.model_id,
                problem_type=self.model_info().problem_type,
            ),
        )

    def model_info(self) -> ModelResponse:
        """Get information about the model"""
        # For the moment, the model information will just be the model response object.
        return self._cached_model_info.get_response()

    def url(self) -> str:
        base_url = self._connection.base_url
        project_id = self.model_info().project_id
        model_id = self.model_id

        return f"{base_url}/{project_id}/models/{model_id}"

    def predict(
        self,
        data: DataLike,
        *,
        name: str,
        description: Optional[str],
        wait_until_complete: bool,
    ) -> Prediction:
        if not self.is_fitted():
            raise Exception("Model must be fitted before performing a prediction")
        data = get_dataset_from_datalike(data, connection=self._connection)
        return Prediction.create_prediction(
            self.model_id,
            data.data_set_id,
            name=name,
            description=description,
            connection=self._connection,
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
        if not self.is_fitted():
            raise Exception("Model must be fitted before performing a test")
        data = get_dataset_from_datalike(data, connection=self._connection)
        return Test.create_test(
            self.model_id,
            data.data_set_id,
            name=name,
            description=description,
            connection=self._connection,
            wait_until_complete=wait_until_complete,
        )

    def results_as_df(self) -> pd.DataFrame:
        """A data frame containing the model results data. For classification & regression this result is the result of hold-out
        test, for clustering it is the clustered data."""

        response = get_model_result_parquet_data.sync_detailed(
            client=self._client, id=self.model_id
        )
        if response.status_code != 200:
            raise ValueError(
                f"Error obtaining model results from server: {str(response.content)}"
            )

        return pd.read_parquet(BytesIO(response.content))

    def save_results_as_dataset(
        self, *, name: Optional[str] = None, description: Optional[str] = None
    ) -> DataSet:
        """Save the model results data as a data set to allow use in other places in the system - For classification & regression
        this result is the result of hold-out test, for clustering it is the clustered data.
        """

        name = name or _default_saved_results_dataset_name(self.model_info().name)
        payload = SaveModelResultsRequest(name=name, description=description)
        data_set_id = check_exists(
            save_model_result.sync(
                client=self._client, id=self.model_id, json_body=payload
            )
        ).id
        return load_data_set_from_server(data_set_id, connection=self._connection)

    ######################
    # Local only methods #
    ######################

    def fit(
        self,
        data: DataLike,
        target: str,
        excluded_columns: Optional[List[str]] = None,
        *,
        sample_weight: Optional[str] = None,
        order_by: Optional[str] = None,
        partition_by: Optional[str] = None,
        hold_out_percentage: Optional[float] = 10.0,
        no_mixing: Optional[List[str]] = None,
    ) -> BaseModel:
        raise Exception("Model is already fitted - cannot refit")
