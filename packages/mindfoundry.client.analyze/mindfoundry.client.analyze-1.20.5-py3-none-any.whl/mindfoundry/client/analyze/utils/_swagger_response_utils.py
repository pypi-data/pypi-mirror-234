import io
import json
import tempfile
from contextlib import contextmanager
from typing import Iterator, Optional, TypeVar, Union

import pandas as pd

from mindfoundry.client.analyze.swagger.types import File, Response, Unset

T = TypeVar("T")


def check_response(response: Response[Optional[T]]) -> T:
    """
    Checks that the response succeeded and has a parseable response body
    :param response: The response to check
    :return: The parsed response body
    """
    if response.status_code >= 200 and response.status_code < 300:
        return check_exists(response.parsed)
    raise Exception(response.content)


def check_exists(response_object: Optional[T]) -> T:
    """
    Checks that the response is not null, and raises an exception if it is
    :param response_object: The object to check
    :return: The non-null value of the object
    """
    if response_object is None:
        raise Exception("No parsed response received")
    return response_object


def check_not_unset(response_object: Union[Unset, T]) -> T:
    """
    Checks that the response is not UNSET, and raises an exception if it is
    :param response_object: The object to check
    :return: The value of the object
    """
    if isinstance(response_object, Unset):
        raise Exception("Expected value was unset")
    return response_object


@contextmanager
def get_data_file(data) -> Iterator[File]:
    """
    Convert a range of data inputs into a suitable File object for passing to the API.
    :param data: The data to send - Can be a text or bytes stream, a pandas data frame, or any object to be serialized as json
    """
    if isinstance(data, (io.TextIOBase, io.BytesIO)):
        yield File(file_name="input", payload=data)  # type:ignore

    if isinstance(data, pd.DataFrame):
        with tempfile.TemporaryFile(mode="w+", newline="\n") as file:
            data.to_csv(file, index=False)
            file.seek(0)
            yield File(file_name="input", payload=file)  # type: ignore
    else:
        with tempfile.TemporaryFile(mode="w+", newline="\n") as file:
            json.dump(data, file)
            file.seek(0)
            yield File(file_name="input", payload=file)  # type: ignore
