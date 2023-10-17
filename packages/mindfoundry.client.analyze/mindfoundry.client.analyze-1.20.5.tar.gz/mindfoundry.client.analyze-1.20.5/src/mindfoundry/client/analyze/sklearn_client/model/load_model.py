from typing import Union

from ...swagger.api.models import get_model
from ...swagger.models import ProblemType
from ...utils import check_exists
from ...utils.typing import PathLike
from ..connection import ConnectionLike, client_from_connectionlike
from . import AnalyzeClassifier
from .regressor.analyze_regressor import AnalyzeRegressor
from .serialization import parse_model_from_path


def load_model(
    path: PathLike, *, connection: ConnectionLike
) -> Union[AnalyzeRegressor, AnalyzeClassifier]:
    serialized_model = parse_model_from_path(path)

    if serialized_model.problem_type == ProblemType.REGRESSION:
        return AnalyzeRegressor.load_model(path, connection=connection)

    if serialized_model.problem_type == ProblemType.CLASSIFICATION:
        return AnalyzeClassifier.load_model(path, connection=connection)

    raise Exception("Unsupported model type")


def _work_out_model_type(connection: ConnectionLike, model_id: int):
    client = client_from_connectionlike(connection)
    model_info = check_exists(get_model.sync(client=client, id=model_id))
    return model_info.problem_type


def load_model_from_server(
    model_id: int, *, connection: ConnectionLike
) -> Union[AnalyzeRegressor, AnalyzeClassifier]:
    problem_type = _work_out_model_type(connection, model_id)

    if problem_type == ProblemType.REGRESSION:
        return AnalyzeRegressor.load_model_from_server(model_id, connection=connection)
    if problem_type == ProblemType.CLASSIFICATION:
        return AnalyzeClassifier.load_model_from_server(model_id, connection=connection)
    raise Exception("Unsupported model type")
