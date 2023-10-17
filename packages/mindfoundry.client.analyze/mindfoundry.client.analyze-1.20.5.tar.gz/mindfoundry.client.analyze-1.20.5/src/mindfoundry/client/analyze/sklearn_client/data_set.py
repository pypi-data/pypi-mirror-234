import tempfile
from datetime import datetime
from enum import Enum
from io import BytesIO
from typing import IO, Dict, List, Optional, Union

import pandas as pd

from ..swagger import Client
from ..swagger.api.data import (
    apply_data_prep_steps,
    create_file_data_set,
    get_data_set,
    get_data_sets_parquet_data,
)
from ..swagger.models import (
    ApplyDataPrepStepsRequest,
    CreateFileDataSetRequest,
    DataPrepStepResponse,
    DataSetResponse,
    SetColumnTypeStep,
    SetColumnTypeStepStepType,
)
from ..swagger.types import UNSET, File
from ..utils import wait_for_future_to_succeed
from .connection import ConnectionLike, client_from_connectionlike, from_connectionlike


def _default_dataset_name() -> str:
    return (
        f"Data set from Python Client {datetime.utcnow().strftime('%Y/%m/%d %H:%M:%S')}"
    )


def _upload_file(
    client: Client,
    name: str,
    description: Optional[str],
    file: Union[IO[str], IO[bytes]],
) -> int:
    payload = CreateFileDataSetRequest(
        name=name,
        data=File(file_name="input", payload=file),  # type: ignore
        description=description or UNSET,
    )
    future = create_file_data_set.sync_detailed(
        client=client,
        multipart_data=payload,
    )
    future_response = wait_for_future_to_succeed(client, future)
    return future_response.additional_properties["id"]


def _download_as_parquet(
    client: Client,
    data_set_id: int,
) -> BytesIO:
    response = get_data_sets_parquet_data.sync_detailed(client=client, id=data_set_id)
    if response.status_code != 200:
        raise ValueError(
            f"Error obtaining data set from server: {str(response.content)}"
        )
    return BytesIO(response.content)


class ColumnType(str, Enum):
    INT = "INT"
    FLOAT = "FLOAT"
    TEXT = "TEXT"
    DATETIME = "DATETIME"


def _set_type_step(
    column_names: List[str], type_: ColumnType
) -> Optional[SetColumnTypeStep]:
    if len(column_names) == 0:
        return None
    return SetColumnTypeStep(
        columns=column_names,
        new_type=type_.name,
        step_type=SetColumnTypeStepStepType.TYPE,
        invalid="null",
        not_int="null",
        # Use some sensible defaults for these
        # Could potentially allow the user to specify them?
        epoch="unix_secs",
        datetime_format="%Y/%m/%d %H:%M:%S",
    )


def _apply_steps(client: Client, data_set_id: int, steps):
    response = apply_data_prep_steps.sync_detailed(
        client=client,
        id=data_set_id,
        json_body=ApplyDataPrepStepsRequest(
            steps=steps,  # type:ignore
            insertion_index=UNSET,
        ),
    )
    return wait_for_future_to_succeed(client, response).additional_properties["id"]


def _pretty_step(step_number: int, step: DataPrepStepResponse) -> str:
    step_type = step.step.additional_properties["stepType"]
    # TODO: Pretty print all the additional properties ^
    return f"# {step_number}: '{step_type}' - {step.status} {step.warning_count} warning(s)"


def _pretty_info(info: DataSetResponse) -> str:
    inner_steps_text = "\n".join(
        [
            _pretty_step(step_number, step)
            for step_number, step in enumerate(info.data_prep_steps)
        ]
    )
    if inner_steps_text == "":
        steps_text = "# Steps: None"
    else:
        steps_text = "# Steps\n" + inner_steps_text

    return f"""\
########################################
# Analyze Data Set
# ------------------------------------
# Project: {info.project_id}
# Data Set Id: {info.id}
# Name: {info.name}
# Description: {info.description}
# Shape: ({info.columns} columns x {info.rows} rows)
# Created at {info.created_at} by {info.created_by}
# Status: {info.status}
{steps_text}
########################################
"""


class DataSet:
    """
    An analyze data set stored on the system
    """

    def __init__(self, data_set_id: int, *, connection: ConnectionLike):
        self._connection = from_connectionlike(connection)
        self._client = client_from_connectionlike(connection)
        self.data_set_id = data_set_id

    def as_df(self) -> pd.DataFrame:
        return pd.read_parquet(_download_as_parquet(self._client, self.data_set_id))

    def set_type(self, types: Dict[str, ColumnType]):
        steps = [_set_type_step([column], type_) for column, type_ in types.items()]
        steps = [step for step in steps if step is not None]
        _apply_steps(self._client, self.data_set_id, steps)

    @property
    def info(self) -> DataSetResponse:
        # We could cache this once it is succeeded / failed *if* we
        # (a) cleared it each time we ran steps, and
        # (b) didn't mind if it was out of date if the UI was used to run a data prep step
        response = get_data_set.sync(client=self._client, id=self.data_set_id)
        if response is None:
            raise Exception("Failed to get data set information from server")
        return response

    @property
    def pretty_info(self) -> str:
        return _pretty_info(self.info)

    @property
    def url(self) -> str:
        base_url = self._connection.base_url
        project_id = self.info.project_id
        data_set_id = self.data_set_id
        return f"{base_url}/{project_id}/data/{data_set_id}"

    @classmethod
    def from_df(
        cls,
        data: pd.DataFrame,
        name: Optional[str] = None,
        description: Optional[str] = None,
        *,
        connection: ConnectionLike,
    ) -> "DataSet":
        client = client_from_connectionlike(connection)
        name = name or _default_dataset_name()
        with tempfile.TemporaryFile(mode="w+", newline="\n") as file:
            data.to_csv(file, index=False)
            file.seek(0)
            data_set_id = _upload_file(client, name, description, file)

        return DataSet(data_set_id, connection=connection)

    @classmethod
    def from_csv(
        cls,
        file_name: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        *,
        connection: ConnectionLike,
    ) -> "DataSet":
        client = client_from_connectionlike(connection)
        name = name or _default_dataset_name()
        with open(file_name, "rb") as file:
            data_set_id = _upload_file(client, name, description, file)
        return DataSet(data_set_id, connection=connection)

    @classmethod
    def from_server(cls, data_set_id: int, *, connection: ConnectionLike) -> "DataSet":
        return DataSet(data_set_id, connection=connection)


DataLike = Union[pd.DataFrame, DataSet]


def get_dataset_from_datalike(data: DataLike, *, connection: ConnectionLike) -> DataSet:
    if isinstance(data, DataSet):
        return data
    return DataSet.from_df(data, connection=connection)


def load_data_set_from_server(
    data_set_id: int, *, connection: ConnectionLike
) -> DataSet:
    return DataSet.from_server(data_set_id, connection=connection)


def from_df(
    data: pd.DataFrame,
    name: Optional[str] = None,
    description: Optional[str] = None,
    *,
    connection: ConnectionLike,
) -> DataSet:
    return DataSet.from_df(data, name, description, connection=connection)


def from_csv(
    file_name: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    *,
    connection: ConnectionLike,
) -> DataSet:
    return DataSet.from_csv(file_name, name, description, connection=connection)


__all__ = [
    "ColumnType",
    "DataLike",
    "DataSet",
    "load_data_set_from_server",
    "from_df",
    "from_csv",
]
