from datetime import datetime
from io import BytesIO
from typing import Optional, Union

import pandas as pd

from ..swagger import Client
from ..swagger.api.predictions import (
    create_prediction,
    get_prediction_result_parquet_data,
    save_prediction,
)
from ..swagger.models import (
    CreatePredictionRequest,
    PredictionResponse,
    PredictionResponseProblemType,
    PredictionResponseTaskStatus,
    SavePredictionRequest,
    Status,
)
from ..swagger.types import UNSET, Unset
from ..utils import (
    CachedPredictionResponse,
    check_exists,
    wait_for_prediction_to_complete,
)
from .connection import ConnectionLike, client_from_connectionlike, from_connectionlike
from .data_set import DataSet, load_data_set_from_server


def _default_saved_dataset_name() -> str:
    return f"Saved Prediction from Python Client {datetime.utcnow().strftime('%Y/%m/%d %H:%M:%S')}"


def _download_as_parquet(
    client: Client,
    prediction_id: int,
) -> BytesIO:
    response = get_prediction_result_parquet_data.sync_detailed(
        client=client, id=prediction_id
    )
    if response.status_code != 200:
        raise ValueError(
            f"Error obtaining prediction from server: {str(response.content)}"
        )
    return BytesIO(response.content)


def _raise_if_prediction_is_not_finished(status: Union[Unset, Status]):
    if isinstance(status, Unset):
        raise Exception("Status could not be obtained")

    if status == Status.SUCCEEDED:
        return

    if status == Status.IN_PROGRESS:
        raise Exception("The prediction is still running")
    if status == Status.FAILED:
        raise Exception("The prediction has failed")
    raise Exception("The prediction has not succeeded")


class Prediction:
    def __init__(self, prediction_id: int, *, connection: ConnectionLike):
        self.prediction_id = prediction_id
        self._connection = from_connectionlike(connection)
        self._client = client_from_connectionlike(connection)
        self._cached_prediction_info = CachedPredictionResponse(
            self._client, self.prediction_id
        )

    @classmethod
    def create_prediction(
        cls,
        model_id: int,
        data_set_id: int,
        *,
        connection: ConnectionLike,
        name: str,
        description: Optional[str],
        wait_until_complete: bool,
    ) -> "Prediction":
        """
        Create a new prediction for the specified Analyze model id and data set id.
        Usually you should use the `model.predict(data_set)` method rather than this method.
        """
        client = client_from_connectionlike(connection)
        prediction_id = check_exists(
            create_prediction.sync(
                client=client,
                json_body=CreatePredictionRequest(
                    model_id=model_id,
                    data_set_id=data_set_id,
                    name=name,
                    description=description or UNSET,
                ),
            )
        ).id

        if wait_until_complete:
            wait_for_prediction_to_complete(client, prediction_id)

        return Prediction(prediction_id, connection=connection)

    @property
    def is_in_progress(self) -> bool:
        """Specifies whether the prediction is currently running"""
        return self.info.status == Status.IN_PROGRESS

    @property
    def is_ready(self) -> bool:
        """Specifies whether the prediction is finished and available for use"""
        return self.info.status == Status.SUCCEEDED

    def wait_until_ready(self):
        wait_for_prediction_to_complete(self._client, self.prediction_id)

    @property
    def info(self) -> PredictionResponse:
        """Information about the prediction"""
        return self._cached_prediction_info.get_response()

    def as_df(self) -> pd.DataFrame:
        """
        A data frame containing the prediction input data, the predicted output
        and additional information about the predicted output.
        e.g. class confidences for classification predictions.
        The prediction is stored in the column identified by `info.predicted_column_name`.
        """
        _raise_if_prediction_is_not_finished(self.info.status)
        return pd.read_parquet(_download_as_parquet(self._client, self.prediction_id))

    def prediction(self) -> pd.Series:
        """
        A series of predictions, one for each row in the input data set, in the same order as the data set.
        Equivalent to `prediction.as_df()[prediction.info.predicted_column_name]`
        """
        _raise_if_prediction_is_not_finished(self.info.status)
        return self.as_df()[self.info.prediction_column_name]

    def save_as_dataset(
        self, *, name: Optional[str] = None, description: Optional[str] = None
    ) -> DataSet:
        """Save the prediction data as a data set to allow use in other places in the system"""
        _raise_if_prediction_is_not_finished(self.info.status)
        if not self.is_ready:
            raise Exception("Prediction is not available")
        name = name or _default_saved_dataset_name()
        payload = SavePredictionRequest(name=name, description=description)
        data_set_id = check_exists(
            save_prediction.sync(
                client=self._client, id=self.prediction_id, json_body=payload
            )
        ).id
        return load_data_set_from_server(data_set_id, connection=self._connection)

    @property
    def url(self):
        """Get the url of the prediction page in Analyze"""
        base_url = self._connection.base_url
        project_id = self.info.project_id
        prediction_id = self.prediction_id

        return f"{base_url}/{project_id}/predictions/{prediction_id}"

    # TODO: Get prediction forecast - only needed for multiseries / regular forecast models


def load_prediction_from_server(
    prediction_id: int, *, connection: ConnectionLike
) -> Prediction:
    """Load the prediction with the specified id from the Analyze server"""
    return Prediction(prediction_id, connection=connection)


__all__ = [
    "Prediction",
    "load_prediction_from_server",
    "PredictionResponse",
    "PredictionResponseProblemType",
    "PredictionResponseTaskStatus",
    "Status",
    "UNSET",
]
