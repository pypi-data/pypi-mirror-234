from datetime import datetime
from io import BytesIO
from typing import Optional, Union

import pandas as pd

from ..swagger import Client
from ..swagger.api.tests import create_test, get_test_result_parquet_data, save_test
from ..swagger.models import (
    CreateTestRequest,
    SaveTestRequest,
    ScoreType,
    Status,
    TestResponse,
    TestResponseProblemType,
    TestResponseTaskStatus,
)
from ..swagger.types import UNSET, Unset
from ..utils import (
    CachedTestResponse,
    check_exists,
    check_not_unset,
    wait_for_test_to_complete,
)
from .connection import ConnectionLike, client_from_connectionlike, from_connectionlike
from .data_set import DataSet, load_data_set_from_server


def _default_test_name() -> str:
    return f"Test from Python Client {datetime.utcnow().strftime('%Y/%m/%d %H:%M:%S')}"


def _default_saved_dataset_name() -> str:
    return f"Saved Test from Python Client {datetime.utcnow().strftime('%Y/%m/%d %H:%M:%S')}"


def _download_as_parquet(
    client: Client,
    test_id: int,
) -> BytesIO:
    response = get_test_result_parquet_data.sync_detailed(client=client, id=test_id)
    if response.status_code != 200:
        raise ValueError(f"Error obtaining test from server: {str(response.content)}")
    return BytesIO(response.content)


def _raise_if_test_is_not_finished(status: Union[Unset, Status]):
    if isinstance(status, Unset):
        raise Exception("Status could not be obtained")

    if status == Status.SUCCEEDED:
        return

    if status == Status.IN_PROGRESS:
        raise Exception("The test is still running")
    if status == Status.FAILED:
        raise Exception("The test has failed")
    raise Exception("The test has not succeeded")


class Test:
    def __init__(self, test_id: int, *, connection: ConnectionLike):
        self.test_id = test_id
        self._connection = from_connectionlike(connection)
        self._client = client_from_connectionlike(connection)
        self._cached_test_info = CachedTestResponse(self._client, self.test_id)

    @classmethod
    def create_test(
        cls,
        model_id: int,
        data_set_id: int,
        *,
        connection: ConnectionLike,
        name: Optional[str] = None,
        description: Optional[str] = None,
        wait_until_complete: bool = True,
    ) -> "Test":
        """
        Create a new test for the specified Analyze model id and data set id.
        Usually you should use the `model.test(data_set)` method rather than this method.
        """
        client = client_from_connectionlike(connection)
        test_id = check_exists(
            create_test.sync(
                client=client,
                json_body=CreateTestRequest(
                    model_id=model_id,
                    data_set_id=data_set_id,
                    name=name or _default_test_name(),
                    description=description or UNSET,
                ),
            )
        ).id

        if wait_until_complete:
            wait_for_test_to_complete(client, test_id)

        return Test(test_id, connection=connection)

    @property
    def is_in_progress(self) -> bool:
        """Specifies whether the test is currently running"""
        return self.info.status == Status.IN_PROGRESS

    @property
    def is_ready(self) -> bool:
        """Specifies whether the test is finished and available for use"""
        return self.info.status == Status.SUCCEEDED

    def wait_until_ready(self):
        wait_for_test_to_complete(self._client, self.test_id)

    @property
    def info(self) -> TestResponse:
        """Information about the test"""
        return self._cached_test_info.get_response()

    def as_df(self) -> pd.DataFrame:
        """
        A data frame containing the test input data, the predicted output and additional information about the predicted output.
        e.g. class confidences for classification predictions.
        The prediction is stored in the column identified by `info.predicted_column_name`.
        """
        _raise_if_test_is_not_finished(self.info.status)
        return pd.read_parquet(_download_as_parquet(self._client, self.test_id))

    def prediction(self) -> pd.Series:
        """
        A series of predictions, one for each row in the input data set, in the same order as the data set.
        Equivalent to `test.as_df()[test.info.predicted_column_name]`
        """
        _raise_if_test_is_not_finished(self.info.status)
        return self.as_df()[self.info.predicted_column_name]

    @property
    def score(self) -> float:
        _raise_if_test_is_not_finished(self.info.status)
        return check_exists(check_not_unset(self.info.score)).value

    def save_as_dataset(
        self, *, name: Optional[str] = None, description: Optional[str] = None
    ) -> DataSet:
        """Save the test data as a data set to allow use in other places in the system"""
        _raise_if_test_is_not_finished(self.info.status)
        if not self.is_ready:
            raise Exception("Test is not available")
        name = name or _default_saved_dataset_name()
        payload = SaveTestRequest(name=name, description=description)
        data_set_id = check_exists(
            save_test.sync(client=self._client, id=self.test_id, json_body=payload)
        ).id
        return load_data_set_from_server(data_set_id, connection=self._connection)

    @property
    def url(self):
        """Get the url of the test page in Analyze"""
        base_url = self._connection.base_url
        project_id = self.info.project_id
        test_id = self.test_id

        return f"{base_url}/{project_id}/tests/{test_id}"

    # TODO: Get test forecast - only needed for multiseries / regular forecast models


def load_test_from_server(test_id: int, *, connection: ConnectionLike) -> Test:
    """Load the test with the specified id from the Analyze server"""
    return Test(test_id, connection=connection)


__all__ = [
    "Test",
    "load_test_from_server",
    "TestResponse",
    "TestResponseProblemType",
    "TestResponseTaskStatus",
    "ScoreType",
]
