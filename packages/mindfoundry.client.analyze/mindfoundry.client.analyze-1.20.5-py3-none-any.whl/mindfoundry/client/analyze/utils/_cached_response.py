import abc
from typing import Generic, TypeVar, Union

from ..swagger import Client
from ..swagger.api.models import get_model
from ..swagger.api.predictions import get_prediction
from ..swagger.api.tests import get_test
from ..swagger.models import (
    ModelResponse,
    ModelStatus,
    PredictionResponse,
    Status,
    TestResponse,
)
from ._swagger_response_utils import check_exists
from .typing import UNSET, Unset

T = TypeVar("T")


class CachedResponse(Generic[T], abc.ABC):
    def __init__(self):
        self._cached_info: Union[Unset, T] = UNSET

    def get_response(self) -> T:
        self._cached_info = self._sync_info(self._cached_info)
        if isinstance(self._cached_info, Unset):
            raise Exception("Could not obtain information from remote server")
        return self._cached_info

    @abc.abstractmethod
    def _sync_info(self, current: Union[Unset, T]) -> Union[Unset, T]:
        """Get the latest version of the information"""


class CachedModelResponse(CachedResponse[ModelResponse]):
    def __init__(self, client: Client, model_id: int):
        super().__init__()
        self._client = client
        self._model_id = model_id

    def _sync_info(
        self, current: Union[Unset, ModelResponse]
    ) -> Union[Unset, ModelResponse]:
        # Get the info *unless* the previous info was already complete or failed
        if not isinstance(current, Unset) and current.status in (
            ModelStatus.COMPLETE,
            ModelStatus.FAILED,
        ):
            return current
        return check_exists(get_model.sync(client=self._client, id=self._model_id))


class CachedPredictionResponse(CachedResponse[PredictionResponse]):
    def __init__(self, client: Client, prediction_id: int):
        super().__init__()
        self._client = client
        self._prediction_id = prediction_id

    def _sync_info(
        self, current: Union[Unset, PredictionResponse]
    ) -> Union[Unset, PredictionResponse]:
        # Get the info *unless* the previous info was already complete or failed
        if not isinstance(current, Unset) and current.status in (
            Status.SUCCEEDED,
            Status.MISSING,
            Status.FAILED,
        ):
            return current
        return check_exists(
            get_prediction.sync(client=self._client, id=self._prediction_id)
        )


class CachedTestResponse(CachedResponse[TestResponse]):
    def __init__(self, client: Client, test_id: int):
        super().__init__()
        self._client = client
        self._test_id = test_id

    def _sync_info(
        self, current: Union[Unset, TestResponse]
    ) -> Union[Unset, TestResponse]:
        # Get the info *unless* the previous info was already complete or failed
        if not isinstance(current, Unset) and current.status in (
            Status.SUCCEEDED,
            Status.MISSING,
            Status.FAILED,
        ):
            return current
        return check_exists(get_test.sync(client=self._client, id=self._test_id))
