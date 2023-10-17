import io
import json
from typing import Any, Dict

import attr

from ...swagger.models import ProblemType
from ...utils.typing import PathLike


@attr.s(auto_attribs=True)
class SerializedModel:
    base_url: str
    model_id: int
    project_id: int
    problem_type: ProblemType


def parse_model_from_path(path: PathLike):
    with open(path, mode="r", encoding="UTF-8") as file:
        config = json.load(file)
    return parse_model(config)


def parse_model(config: Dict[str, Any]) -> SerializedModel:
    if "model" not in config.keys():
        raise Exception("Not a model")
    model_config = config["model"]

    if "base_url" not in model_config.keys():
        raise Exception(
            "Configuration did not represent an Analyze model - No base_url saved"
        )
    base_url = model_config["base_url"]

    if "project_id" not in model_config.keys():
        raise Exception(
            "Configuration did not represent an Analyze model - No project_id saved"
        )
    project_id = model_config["project_id"]

    if "model_id" not in model_config.keys():
        raise Exception(
            "Configuration did not represent an Analyze model - No model_id saved"
        )
    model_id = model_config["model_id"]

    if "problem_type" not in model_config.keys():
        raise Exception(
            "Configuration did not represent an Analyze model - No problem_type saved"
        )
    try:
        problem_type = ProblemType[model_config["problem_type"]]
    except KeyError:
        raise Exception(  # pylint: disable=raise-missing-from
            "Configuration did not represent an Analyze model - problem_type did not match a valid Analyze problem type"
        )

    return SerializedModel(
        base_url=base_url,
        project_id=project_id,
        model_id=model_id,
        problem_type=problem_type,
    )


def save_model(path: PathLike, serialized_model: SerializedModel):
    with io.open(path, mode="w", encoding="UTF-8") as file:
        dict_repr = {
            "model": {
                "base_url": serialized_model.base_url,
                "project_id": serialized_model.project_id,
                "model_id": serialized_model.model_id,
                "problem_type": str(serialized_model.problem_type),
            }
        }
        json.dump(dict_repr, file)
