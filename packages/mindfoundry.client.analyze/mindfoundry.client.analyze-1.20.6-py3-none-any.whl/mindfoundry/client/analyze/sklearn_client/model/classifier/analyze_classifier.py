from datetime import datetime
from typing import List, Optional, Union, overload

from ....swagger.models import (
    ClassificationModelType,
    ClassificationScorers,
    ModelValidationMethod,
    NlpLanguage,
    ProblemType,
)
from ....utils.typing import UNSET, PathLike, Unset
from ...connection import ConnectionLike, from_connectionlike
from ...data_set import DataLike
from ..serialization import parse_model_from_path
from ..shared import AnalyzeModel, BaseModel, RemoteModel
from .local import InitialConfig, LocalClassifier


def _default_model_name() -> str:
    return f"Classification Model from Python Client {datetime.utcnow().strftime('%Y/%m/%d %H:%M:%S')}"


class AnalyzeClassifier(AnalyzeModel):
    @overload
    def __init__(
        self,
        scorer: ClassificationScorers = ClassificationScorers.F1_SINGLE_CLASS,
        model_validation_method: ModelValidationMethod = ModelValidationMethod.FIVE_FOLD_CROSS,
        name: Optional[str] = None,
        description: Optional[str] = None,
        number_of_evaluations: int = 250,
        nlp_language: NlpLanguage = NlpLanguage.AUTO_DETECT,
        draft_mode: bool = False,
        *,
        connection: ConnectionLike,
    ):
        """
        Create a new Analyze classification model
        :param scorer: The scorer to use to determine the optimal model
        :param model_validation_method: The method to use to validate the model
        :param name: A name for the model
        :param description: A description for the model
        :param number_of_evaluations: The number of models to evaluate during optimization
        :param nlp_language: The language used when performing NLP on text columns
        :param draft_mode: Create a draft model rather than a fully optimized model
        :param connection: The connection to the Analyze project in which the model will be created
        """

    @overload
    def __init__(self, *, _internal_model: BaseModel):
        """Internal constructor - DO NOT USE"""

    def __init__(
        self,
        scorer: ClassificationScorers = ClassificationScorers.F1_SINGLE_CLASS,
        model_validation_method: ModelValidationMethod = ModelValidationMethod.FIVE_FOLD_CROSS,
        name: Optional[str] = None,
        description: Optional[str] = None,
        number_of_evaluations: int = 250,
        nlp_language: NlpLanguage = NlpLanguage.AUTO_DETECT,
        draft_mode: bool = False,
        *,
        connection: Union[ConnectionLike, Unset] = UNSET,
        _internal_model: Union[BaseModel, Unset] = UNSET,
        model_types: Optional[List[ClassificationModelType]] = None,
    ):
        """Internal constructor - DO NOT USE"""
        if not isinstance(_internal_model, Unset):
            # Default to using the classifier if it was specified
            super().__init__(_internal_model=_internal_model)
        else:
            # Use the user parameters
            if isinstance(connection, Unset):
                raise Exception(
                    "You must specify either the connection or the _classifier parameter."
                )
            initial_config = InitialConfig(
                scorer=scorer,
                model_validation_method=model_validation_method,
                name=name if name is not None else _default_model_name(),
                description=description,
                number_of_evaluations=number_of_evaluations,
                nlp_language=nlp_language,
                draft_mode=draft_mode,
                model_types=model_types,
            )
            super().__init__(
                _internal_model=LocalClassifier(connection, initial_config)
            )

    @classmethod
    def load_model(
        cls, path: PathLike, *, connection: ConnectionLike
    ) -> "AnalyzeClassifier":
        """
        Load a regression model from a saved file
        :param path: The path of the file to load
        :param connection: A connection to the project that contains the model
        :return:
        """
        connection = from_connectionlike(connection)
        serialized_model = parse_model_from_path(path)
        remote_model = RemoteModel.from_serialized_model(connection, serialized_model)

        if remote_model.model_info().problem_type != ProblemType.CLASSIFICATION:
            raise Exception("The model is not an Analyze classification model.")
        return AnalyzeClassifier(_internal_model=remote_model)

    @classmethod
    def load_model_from_server(
        cls, model_id: int, *, connection: ConnectionLike
    ) -> "AnalyzeClassifier":
        """
        Load a classification model from the Analyze server
        :param model_id: The model ID
        :param connection: A connection to the project that contains the model
        :return: A fitted classifier that uses the server model to perform predictions
        """
        return AnalyzeClassifier(_internal_model=RemoteModel(connection, model_id))

    @overload
    def fit(
        self,
        data: DataLike,
        target: str,
        excluded_columns: Optional[List[str]] = None,
        *,
        wait_until_complete: bool = True,
        # Classification specific fit parameters
        sample_weight: Optional[str] = None,
        hold_out_percentage: Optional[float] = 10.0,
    ) -> "AnalyzeClassifier":
        """Fit the classification model using random data partitioning"""

    @overload
    def fit(
        self,
        data: DataLike,
        target: str,
        excluded_columns: Optional[List[str]] = None,
        *,
        wait_until_complete: bool = True,
        # Classification specific fit parameters
        sample_weight: Optional[str] = None,
        order_by: str,
        hold_out_percentage: Optional[float] = 10.0,
    ) -> "AnalyzeClassifier":
        """Fit the classification model using ordered data partitioning"""

    @overload
    def fit(
        self,
        data: DataLike,
        target: str,
        excluded_columns: Optional[List[str]] = None,
        *,
        wait_until_complete: bool = True,
        # Classification specific fit parameters
        partition_by: str,
        sample_weight: Optional[str] = None,
        hold_out_percentage=None,
    ) -> "AnalyzeClassifier":
        """Fit the classification model using manual data partitioning"""

    @overload
    def fit(
        self,
        data: DataLike,
        target: str,
        excluded_columns: Optional[List[str]] = None,
        *,
        wait_until_complete: bool = True,
        # Classification specific fit parameters
        sample_weight: Optional[str] = None,
        no_mixing: List[str],
        hold_out_percentage: Optional[float] = 10.0,
    ) -> "AnalyzeClassifier":
        """Fit the classification model using a no-mixing column data partitioning"""

    def fit(
        self,
        data: DataLike,
        target: str,
        excluded_columns: Optional[List[str]] = None,
        *,
        wait_until_complete: bool = True,
        # Classification specific fit parameters
        sample_weight: Optional[str] = None,
        order_by: Optional[str] = None,
        partition_by: Optional[str] = None,
        hold_out_percentage: Optional[float] = 10.0,
        no_mixing: Optional[List[str]] = None,
    ) -> "AnalyzeClassifier":
        """Internal method - DO NOT USE"""
        super()._fit(
            data,
            target,
            excluded_columns,
            wait_until_complete=wait_until_complete,
            order_by=order_by,
            partition_by=partition_by,
            no_mixing=no_mixing,
            sample_weight=sample_weight,
            hold_out_percentage=hold_out_percentage,
        )
        return self
