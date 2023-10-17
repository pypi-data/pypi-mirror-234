from time import sleep
from typing import Optional

from ..swagger import Client
from ..swagger import models as dto
from ..swagger.api.models import get_model
from ..swagger.api.other import get_future
from ..swagger.api.predictions import get_prediction
from ..swagger.api.tests import get_test
from ..swagger.types import Response
from ..utils._swagger_response_utils import (
    check_exists,
    check_not_unset,
    check_response,
)


def wait_for_future_to_succeed(
    client: Client, response: Response[Optional[dto.Future]]
) -> dto.FutureOutputOfYourRequest:
    status = check_response(response).status
    future_id = check_not_unset(check_response(response).future_id)

    while status == dto.Status.IN_PROGRESS:
        sleep(5)
        response = get_future.sync_detailed(client=client, future_id=future_id)
        status = check_response(response).status

    if status == dto.Status.SUCCEEDED:
        return check_exists(check_not_unset(check_response(response).response))
    else:
        raise Exception(response.content)


def _wait_for_model_status(
    client: Client, model_id: int, expected_status: dto.ModelStatus
) -> int:
    while True:
        model_response = check_exists(get_model.sync(client=client, id=model_id))
        status = model_response.status
        if status == expected_status:
            return model_response.id
        if status == dto.ModelStatus.FAILED:
            raise Exception(model_response.failure_details)
        sleep(5)


def wait_for_model_to_complete(client: Client, model_id: int) -> int:
    return _wait_for_model_status(client, model_id, dto.ModelStatus.COMPLETE)


def wait_for_decider_model_test_to_complete(client: Client, model_id: int) -> int:
    # Decider models have a BUILDING status until the test is ready, then they flip to CONFIGURING rather than complete
    return _wait_for_model_status(client, model_id, dto.ModelStatus.CONFIGURING)


def wait_for_prediction_to_complete(client: Client, prediction_id: int) -> int:
    while True:
        prediction_response = check_response(
            get_prediction.sync_detailed(client=client, id=prediction_id)
        )
        status = prediction_response.status
        if status != dto.Status.IN_PROGRESS:
            break
        sleep(10)

    if status == dto.Status.SUCCEEDED:
        return prediction_response.id
    else:
        raise Exception(prediction_response.failure_details)


def wait_for_test_to_complete(client: Client, test_id: int) -> int:
    while True:
        test_response = check_response(
            get_test.sync_detailed(client=client, id=test_id)
        )
        status = test_response.status
        if status != dto.Status.IN_PROGRESS:
            break
        sleep(10)

    if status == dto.Status.SUCCEEDED:
        return test_response.id
    else:
        raise Exception(test_response.failure_details)
