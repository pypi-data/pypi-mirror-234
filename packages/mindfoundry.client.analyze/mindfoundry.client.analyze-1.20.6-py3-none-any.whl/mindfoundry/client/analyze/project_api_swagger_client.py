# pylint: disable=too-many-lines
import io
import json
import tempfile
from os import PathLike
from typing import List, Optional, Tuple, Union

import pandas as pd

from .swagger import Client
from .swagger import models as dto
from .swagger.api.ap_is import (
    create_model_api,
    create_model_api_client,
    create_pipeline_api,
    create_pipeline_api_client,
    delete_model_api,
    delete_model_api_client,
    delete_pipeline_api,
    delete_pipeline_api_client,
    edit_model_api,
    edit_pipeline_api,
    get_model_api,
    get_model_api_client,
    get_model_api_clients,
    get_model_apis,
    get_pipeline_api,
    get_pipeline_api_client,
    get_pipeline_api_clients,
    get_pipeline_apis,
    replace_model_api,
    replace_pipeline_api,
)
from .swagger.api.data import (
    apply_data_prep_steps,
    create_cloud_data_set,
    create_db_data_set,
    create_file_data_set,
    create_http_data_set,
    delete_data_prep_steps,
    delete_data_set,
    edit_data_set,
    get_data_set,
    get_data_sets,
    get_data_sets_csv_data,
    get_data_sets_parquet_data,
)
from .swagger.api.models import (
    configure_decisioning_model,
    create_auto_clustering_model,
    create_classification_model,
    create_clustering_model,
    create_decisioning_model,
    create_forecasting_model,
    create_multi_forecasting_model,
    create_regression_model,
    delete_model,
    edit_model,
    get_model,
    get_model_result_csv_data,
    get_model_result_parquet_data,
    get_models,
    optimize_decisioning_model,
    save_model_result,
    stop_model,
)
from .swagger.api.pipelines import (
    create_data_pipeline,
    delete_data_pipeline,
    edit_data_pipeline,
    get_data_pipeline,
    get_data_pipelines,
)
from .swagger.api.predictions import (
    create_prediction,
    delete_prediction,
    edit_prediction,
    get_prediction,
    get_prediction_forecast,
    get_prediction_result_csv_data,
    get_prediction_result_parquet_data,
    get_predictions,
    save_prediction,
)
from .swagger.api.tests import (
    create_test,
    delete_test,
    edit_test,
    get_test,
    get_test_result_csv_data,
    get_test_result_parquet_data,
    get_tests,
    save_test,
)
from .swagger.types import UNSET
from .utils import (
    check_exists,
    check_not_unset,
    check_response,
    get_data_file,
    wait_for_future_to_succeed,
    wait_for_model_to_complete,
    wait_for_prediction_to_complete,
    wait_for_test_to_complete,
)
from .utils._polling import wait_for_decider_model_test_to_complete

ValidDataPrepStepType = Union[
    dto.ApplyFormulaStep,
    dto.CombineStep,
    dto.DropStep,
    dto.FillMissingValueStep,
    dto.FilterRowsStep,
    dto.GroupByStep,
    dto.MergeColumnsStep,
    dto.NormalizeTextStep,
    dto.RenameStep,
    dto.ReplaceStep,
    dto.SentimentAnalysisStep,
    dto.SetColumnLevelStep,
    dto.SetColumnTypeStep,
    dto.SetTimeIndexStep,
    dto.SimplifyCategoriesStep,
    dto.SplitColumnStep,
    dto.TransformTextStep,
]

ParseOptions = Union[dto.CsvParseOptions, dto.ExcelParseOptions, dto.JsonParseOptions]


# pylint: disable=too-many-public-methods
class AnalyzeSwaggerClientWrapper:
    def __init__(self, client: Client):
        self._client = client

    ###############
    # Datasets
    ###############

    def create_file_data_set(
        self,
        data: Union[pd.DataFrame, str, io.TextIOBase, io.BytesIO],
        name: str,
        description: Optional[str] = None,
        parse_options: Optional[ParseOptions] = None,
    ) -> int:
        with get_data_file(data) as data_file:
            response = create_file_data_set.sync_detailed(
                client=self._client,
                multipart_data=dto.CreateFileDataSetRequest(
                    name=name,
                    data=data_file,
                    description=description or UNSET,
                    parse_options=json.dumps(parse_options) if parse_options else UNSET,
                ),
            )
        return wait_for_future_to_succeed(self._client, response).additional_properties[
            "id"
        ]

    def create_cloud_data_set(
        self,
        name: str,
        description: str,
        cloud_type: dto.CreateCloudDataSetRequestCloudType,
        access_key: str,
        secret_key: str,
        bucket_name: str,
        path: str,
        parse_options: Optional[ParseOptions] = None,
    ) -> int:
        payload = dto.CreateCloudDataSetRequest(
            name=name,
            description=description,
            data_origin=dto.CreateCloudDataSetRequestDataOrigin.CLOUD,
            cloud_type=cloud_type,
            access_key=access_key,
            secret_key=secret_key,
            bucket_name=bucket_name,
            path=path,
            parse_options=parse_options or UNSET,
        )
        response = create_cloud_data_set.sync_detailed(
            client=self._client,
            json_body=payload,
        )
        return wait_for_future_to_succeed(self._client, response).additional_properties[
            "id"
        ]

    def create_http_data_set(
        self,
        name: str,
        description: str,
        url: str,
        parse_options: Optional[ParseOptions] = None,
    ) -> int:
        payload = dto.CreateHttpDataSetRequest(
            name=name,
            description=description,
            data_origin=dto.CreateHttpDataSetRequestDataOrigin.HTTP,
            url=url,
            parse_options=parse_options or UNSET,
        )
        response = create_http_data_set.sync_detailed(
            client=self._client,
            json_body=payload,
        )
        return wait_for_future_to_succeed(self._client, response).additional_properties[
            "id"
        ]

    def create_db_data_set(
        self,
        name: str,
        description: str,
        db_type: dto.CreateDbDataSetRequestDbType,
        custom_db_url: bool,
        query: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[str] = None,
        db_name: Optional[str] = None,
        db_url: Optional[str] = None,
    ) -> int:
        payload = dto.CreateDbDataSetRequest(
            name=name,
            description=description,
            data_origin=dto.CreateDbDataSetRequestDataOrigin.DB,
            db_type=db_type,
            username=username or UNSET,
            password=password or UNSET,
            host=host or UNSET,
            port=port or UNSET,
            db_name=db_name or UNSET,
            custom_db_url=custom_db_url,
            db_url=db_url or UNSET,
            query=query,
        )
        response = create_db_data_set.sync_detailed(
            client=self._client,
            json_body=payload,
        )
        return wait_for_future_to_succeed(self._client, response).additional_properties[
            "id"
        ]

    def list_data_sets(self) -> List[dto.DataSetResponse]:
        return check_not_unset(
            check_exists(get_data_sets.sync(client=self._client)).data_sets
        )

    def get_data_set(self, data_set_id: int) -> dto.DataSetResponse:
        return check_exists(get_data_set.sync(client=self._client, id=data_set_id))

    def edit_data_set(
        self, data_set_id: int, name: str, description: Optional[str] = None
    ) -> dto.DataSetResponse:
        payload = dto.EditDataSetRequest(name=name, description=description)
        return check_exists(
            edit_data_set.sync(client=self._client, id=data_set_id, json_body=payload)
        )

    def download_data_set_as_csv(
        self,
        data_set_id: int,
        output_file: Union[str, PathLike],
        separator: str = ",",
        quote_char: str = '"',
        escape_char: str = "\\",
    ) -> None:
        response = get_data_sets_csv_data.sync_detailed(
            client=self._client,
            id=data_set_id,
            separator=separator,
            quote_char=quote_char,
            escape_char=escape_char,
        )
        if response.status_code != 200:
            raise ValueError(
                f"Error obtaining data set from server: {str(response.content)}"
            )
        with open(output_file, "bw") as file:
            file.write(response.content)

    def _get_data_set_bytes_as_parquet(self, data_set_id: int) -> bytes:
        response = get_data_sets_parquet_data.sync_detailed(
            client=self._client, id=data_set_id
        )
        if response.status_code != 200:
            raise ValueError(
                f"Error obtaining data set from server: {str(response.content)}"
            )
        return response.content

    def download_data_set_as_parquet(
        self, data_set_id: int, output_file: Union[str, PathLike]
    ) -> None:
        with open(output_file, "bw") as file:
            parquet_bytes = self._get_data_set_bytes_as_parquet(data_set_id)
            file.write(parquet_bytes)

    def get_data_set_as_pandas(self, data_set_id: int) -> pd.DataFrame:
        stream = io.BytesIO(self._get_data_set_bytes_as_parquet(data_set_id))
        return pd.read_parquet(stream)

    def delete_data_set(self, data_set_id: int) -> None:
        delete_data_set.sync_detailed(client=self._client, id=data_set_id)

    def apply_saved_data_preparation_steps(
        self,
        data_set_id: int,
        data_preparation_step_id: int,
        insertion_index: Optional[int] = None,
    ) -> int:
        response = apply_data_prep_steps.sync_detailed(
            client=self._client,
            id=data_set_id,
            json_body=dto.ApplyDataPrepStepsRequest(
                saved_steps_id=data_preparation_step_id,
                insertion_index=insertion_index or UNSET,
            ),
        )
        return wait_for_future_to_succeed(self._client, response).additional_properties[
            "id"
        ]

    def apply_new_data_preparation_steps(
        self,
        data_set_id: int,
        steps: List[ValidDataPrepStepType],
        insertion_index: Optional[int] = None,
    ) -> int:
        # Alas, the generated schema doesn't support the oneOf very well,
        # so we accept all the valid steps as inputs and type:ignore the call.
        response = apply_data_prep_steps.sync_detailed(
            client=self._client,
            id=data_set_id,
            json_body=dto.ApplyDataPrepStepsRequest(
                steps=steps,  # type:ignore
                insertion_index=insertion_index or UNSET,
            ),
        )
        return wait_for_future_to_succeed(self._client, response).additional_properties[
            "id"
        ]

    def delete_data_preparation_steps(
        self,
        data_set_id: int,
        delete_index: int,
        delete_children: bool,
    ) -> int:
        response = delete_data_prep_steps.sync_detailed(
            client=self._client,
            id=data_set_id,
            json_body=dto.DeleteDataPrepStepsRequest(
                delete_index=delete_index,
                delete_children=delete_children,
            ),
        )
        return wait_for_future_to_succeed(self._client, response).additional_properties[
            "id"
        ]

    ######################
    # Data set pipelines #
    ######################

    def list_data_pipelines(self) -> List[dto.DataPipelineResponse]:
        return check_not_unset(
            check_exists(get_data_pipelines.sync(client=self._client)).pipelines
        )

    def get_data_pipeline(self, pipeline_id: int) -> dto.DataPipelineResponse:
        return check_exists(get_data_pipeline.sync(client=self._client, id=pipeline_id))

    def delete_data_pipeline(self, pipeline_id: int) -> None:
        delete_data_pipeline.sync_detailed(client=self._client, id=pipeline_id)

    def create_data_pipeline(self, data_set_id: int, name: str) -> int:
        payload = dto.DataPipelineCreateRequest(
            data_set_id=data_set_id,
            name=name,
        )
        return check_exists(
            create_data_pipeline.sync(client=self._client, json_body=payload)
        ).id

    def edit_data_pipeline(
        self, pipeline_id: int, name: str
    ) -> dto.DataPipelineResponse:
        payload = dto.EditDataPipelineRequest(name=name)
        return check_exists(
            edit_data_pipeline.sync(
                client=self._client, id=pipeline_id, json_body=payload
            )
        )

    ###############
    # Models
    ###############

    def list_models(self) -> List[dto.ModelResponse]:
        return check_not_unset(
            check_exists(get_models.sync(client=self._client)).models
        )

    def get_model(self, model_id: int) -> dto.ModelResponse:
        return check_exists(get_model.sync(client=self._client, id=model_id))

    def delete_model(self, model_id: int):
        delete_model.sync_detailed(client=self._client, id=model_id)

    # pylint: disable=too-many-arguments,too-many-locals
    def create_classification_model(
        self,
        name: str,
        data_set_id: int,
        target_column: str,
        score_to_optimize: dto.ClassificationScorers = dto.ClassificationScorers.F1_WEIGHTED_AVG,
        excluded_columns: Optional[List[str]] = None,
        description: Optional[str] = None,
        draft_mode: bool = False,
        number_of_evaluations: int = 300,
        nlp_language: dto.NlpLanguage = dto.NlpLanguage.AUTO_DETECT,
        model_validation_method: dto.ModelValidationMethod = dto.ModelValidationMethod.FIVE_FOLD_CROSS,
        no_mixing_columns: Optional[List[str]] = None,
        data_partition_method: dto.DataPartitionMethod = dto.DataPartitionMethod.RANDOM,
        hold_out_percentage: Optional[float] = 10.0,
        partition_column: Optional[str] = None,
        order_by_column: Optional[str] = None,
        weight_column: Optional[str] = None,
        wait_until_complete: bool = True,
        model_types: Optional[List[dto.ClassificationModelType]] = None,
    ) -> int:
        payload = dto.CreateClassificationRequest(
            name=name,
            data_set_id=data_set_id,
            target_column=target_column,
            score_to_optimize=score_to_optimize,
            model_validation_method=model_validation_method,
            data_partition_method=data_partition_method,
            number_of_evaluations=number_of_evaluations,
            description=description or UNSET,
            excluded_columns=excluded_columns or UNSET,
            nlp_language=nlp_language,
            draft_mode=draft_mode,
            hold_out_percentage=hold_out_percentage or UNSET,
            no_mixing_columns=no_mixing_columns or UNSET,
            partition_column=partition_column or UNSET,
            order_by_column=order_by_column or UNSET,
            weight_column=weight_column or UNSET,
            model_types=model_types or UNSET,
        )

        model_id = check_exists(
            create_classification_model.sync(client=self._client, json_body=payload)
        ).id

        if not wait_until_complete:
            return model_id

        return wait_for_model_to_complete(self._client, model_id)

    # pylint: disable=too-many-arguments,too-many-locals
    def create_regression_model(
        self,
        name: str,
        data_set_id: int,
        target_column: str,
        target_distribution: Optional[dto.TargetDistributions] = None,
        score_to_optimize: dto.RegressionScorers = dto.RegressionScorers.RMSE,
        excluded_columns: Optional[List[str]] = None,
        description: Optional[str] = None,
        number_of_evaluations: int = 300,
        nlp_language: dto.NlpLanguage = dto.NlpLanguage.AUTO_DETECT,
        draft_mode: bool = False,
        model_validation_method: dto.ModelValidationMethod = dto.ModelValidationMethod.FIVE_FOLD_CROSS,
        no_mixing_columns: Optional[List[str]] = None,
        data_partition_method: dto.DataPartitionMethod = dto.DataPartitionMethod.RANDOM,
        hold_out_percentage: Optional[float] = 10.0,
        partition_column: Optional[str] = None,
        order_by_column: Optional[str] = None,
        weight_column: Optional[str] = None,
        wait_until_complete: bool = True,
        model_types: Optional[List[dto.RegressionModelType]] = None,
    ) -> int:
        payload = dto.CreateRegressionRequest(
            name=name,
            data_set_id=data_set_id,
            target_column=target_column,
            target_distribution=target_distribution or UNSET,
            score_to_optimize=score_to_optimize,
            model_validation_method=model_validation_method,
            data_partition_method=data_partition_method,
            number_of_evaluations=number_of_evaluations,
            description=description or UNSET,
            excluded_columns=excluded_columns or UNSET,
            nlp_language=nlp_language,
            draft_mode=draft_mode,
            hold_out_percentage=hold_out_percentage or UNSET,
            no_mixing_columns=no_mixing_columns or UNSET,
            partition_column=partition_column or UNSET,
            order_by_column=order_by_column or UNSET,
            weight_column=weight_column or UNSET,
            model_types=model_types or UNSET,
        )
        model_id = check_exists(
            create_regression_model.sync(client=self._client, json_body=payload)
        ).id
        if not wait_until_complete:
            return model_id

        return wait_for_model_to_complete(self._client, model_id)

    def create_clustering_model(
        self,
        name: str,
        data_set_id: int,
        number_of_clusters: int,
        description: Optional[str] = None,
        nlp_language: dto.NlpLanguage = dto.NlpLanguage.AUTO_DETECT,
        excluded_columns: Optional[List[str]] = None,
        wait_until_complete: bool = True,
    ) -> int:
        payload = dto.CreateClusteringRequest(
            name=name,
            data_set_id=data_set_id,
            description=description or UNSET,
            excluded_columns=excluded_columns or UNSET,
            nlp_language=nlp_language,
            number_of_clusters=number_of_clusters,
        )
        model_id = check_exists(
            create_clustering_model.sync(client=self._client, json_body=payload)
        ).id

        if not wait_until_complete:
            return model_id

        return wait_for_model_to_complete(self._client, model_id)

    def create_autoclustering_model(
        self,
        name: str,
        data_set_id: int,
        minimum_clusters: int,
        maximum_clusters: int,
        description: Optional[str] = None,
        nlp_language: dto.NlpLanguage = dto.NlpLanguage.AUTO_DETECT,
        excluded_columns: Optional[List[str]] = None,
        wait_until_complete: bool = True,
    ) -> int:
        payload = dto.CreateAutoClusteringRequest(
            name=name,
            data_set_id=data_set_id,
            description=description or UNSET,
            excluded_columns=excluded_columns or UNSET,
            nlp_language=nlp_language,
            minimum_clusters=minimum_clusters,
            maximum_clusters=maximum_clusters,
        )
        model_id = check_exists(
            create_auto_clustering_model.sync(client=self._client, json_body=payload)
        ).id

        if not wait_until_complete:
            return model_id

        return wait_for_model_to_complete(self._client, model_id)

    def create_forecasting_model(
        self,
        name: str,
        data_set_id: int,
        target_column: str,
        time_index_column: str,
        cadence: dto.Cadence,
        horizons: List[int],
        description: Optional[str] = None,
        excluded_columns: Optional[List[str]] = None,
        wait_until_complete: bool = True,
    ) -> int:
        payload = dto.CreateForecastingRequest(
            name=name,
            data_set_id=data_set_id,
            description=description or UNSET,
            target_column=target_column,
            time_index_column=time_index_column,
            cadence=cadence,
            horizons=horizons,
            excluded_columns=excluded_columns or UNSET,
        )
        model_id = check_exists(
            create_forecasting_model.sync(client=self._client, json_body=payload)
        ).id

        if not wait_until_complete:
            return model_id

        return wait_for_model_to_complete(self._client, model_id)

    def create_multi_forecasting_model(
        self,
        name: str,
        data_set_id: int,
        target_column: str,
        time_index_column: str,
        cadence: dto.Cadence,
        horizons: List[int],
        discriminator_columns: List[str],
        description: Optional[str] = None,
        excluded_columns: Optional[List[str]] = None,
        wait_until_complete: bool = True,
    ) -> int:
        payload = dto.CreateMultiForecastingRequest(
            name=name,
            data_set_id=data_set_id,
            description=description or UNSET,
            target_column=target_column,
            time_index_column=time_index_column,
            discriminator_columns=discriminator_columns,
            cadence=cadence,
            horizons=horizons,
            excluded_columns=excluded_columns or UNSET,
        )
        model_id = check_exists(
            create_multi_forecasting_model.sync(client=self._client, json_body=payload)
        ).id

        if not wait_until_complete:
            return model_id

        return wait_for_model_to_complete(self._client, model_id)

    def create_decisioning_model(
        self,
        name: str,
        data_set_id: int,
        parent_model_id: int,
        description: Optional[str] = None,
        wait_until_complete: bool = True,
    ) -> int:
        """
        Create a new *unconfigured* decisioning model
        """
        payload = dto.CreateDecisioningRequest(
            name=name,
            data_set_id=data_set_id,
            parent_model_id=parent_model_id,
            configuration=UNSET,
            description=description or UNSET,
        )

        model_id = check_exists(
            create_decisioning_model.sync(client=self._client, json_body=payload)
        ).id

        if not wait_until_complete:
            return model_id

        return wait_for_decider_model_test_to_complete(self._client, model_id)

    def optimize_decisioning_model(
        self,
        model_id: int,
        rewards: pd.DataFrame,
    ) -> dto.ConfigureDecisioningRequest:
        existing_model = self.get_model(model_id)
        assert existing_model.problem_type == dto.ProblemType.DECIDER
        assert existing_model.status == dto.ModelStatus.CONFIGURING

        target_class, decisions = _reward_matrix_dto_from_dataframe(rewards)
        payload = dto.ConfigureDecisioningRequest(
            target_class=target_class,
            decisions=decisions,
        )

        return check_exists(
            optimize_decisioning_model.sync(
                client=self._client, id=model_id, json_body=payload
            )
        )

    def configure_decisioning_model(
        self,
        model_id: int,
        configuration: dto.ConfigureDecisioningRequest,
        wait_until_complete: bool = True,
    ) -> int:
        """
        Specify the decision thresholds for a configuring decisioning model
        :param model_id: The decisioning model to configure
        :param configuration: The configuration to use for the model
        :param wait_until_complete: Automatically sleep until the model is complete?
        :return:
        """
        model_id = check_exists(
            configure_decisioning_model.sync(
                client=self._client, id=model_id, json_body=configuration
            )
        ).id

        if not wait_until_complete:
            return model_id

        return wait_for_model_to_complete(self._client, model_id)

    def edit_model(
        self, model_id: int, name: str, description: Optional[str] = None
    ) -> dto.ModelResponse:
        payload = dto.EditModelRequest(name=name, description=description)
        return check_exists(
            edit_model.sync(client=self._client, id=model_id, json_body=payload)
        )

    def stop_optimization(self, model_id: int):
        stop_model.sync_detailed(client=self._client, id=model_id)

    def download_model_results_as_csv(
        self,
        model_id: int,
        output_file: Union[str, PathLike],
        separator: str = ",",
        quote_char: str = '"',
        escape_char: str = "\\",
    ) -> None:
        response = get_model_result_csv_data.sync_detailed(
            client=self._client,
            id=model_id,
            separator=separator,
            quote_char=quote_char,
            escape_char=escape_char,
        )
        if response.status_code != 200:
            raise ValueError(
                f"Error obtaining model results from server: {str(response.content)}"
            )
        with open(output_file, "bw") as file:
            file.write(response.content)

    def _get_model_results_bytes_as_parquet(self, model_id: int) -> bytes:
        response = get_model_result_parquet_data.sync_detailed(
            client=self._client, id=model_id
        )
        if response.status_code != 200:
            raise ValueError(
                f"Error obtaining model results from server: {str(response.content)}"
            )
        return response.content

    def download_model_results_as_parquet(
        self, model_id: int, output_file: Union[str, PathLike]
    ) -> None:
        with open(output_file, "bw") as file:
            parquet_bytes = self._get_model_results_bytes_as_parquet(model_id)
            file.write(parquet_bytes)

    def get_model_results_as_pandas(self, model_id: int) -> pd.DataFrame:
        stream = io.BytesIO(self._get_model_results_bytes_as_parquet(model_id))
        return pd.read_parquet(stream)

    def save_model_results_as_data_set(
        self, model_id: int, name: str, description: Optional[str] = None
    ) -> int:
        payload = dto.SaveModelResultsRequest(name=name, description=description)
        return check_exists(
            save_model_result.sync(client=self._client, id=model_id, json_body=payload)
        ).id

    ###############
    # Prediction
    ###############

    def create_prediction(
        self,
        model_id: int,
        data_set_id: int,
        name: str,
        description: Optional[str] = None,
        wait_until_complete: bool = True,
    ) -> int:
        prediction_id = check_exists(
            create_prediction.sync(
                client=self._client,
                json_body=dto.CreatePredictionRequest(
                    model_id=model_id,
                    data_set_id=data_set_id,
                    name=name,
                    description=description or UNSET,
                ),
            )
        ).id
        if not wait_until_complete:
            return prediction_id

        return wait_for_prediction_to_complete(self._client, prediction_id)

    def edit_prediction(
        self, prediction_id: int, name: str, description: Optional[str] = None
    ) -> dto.PredictionResponse:
        payload = dto.EditPredictionRequest(name=name, description=description)
        return check_exists(
            edit_prediction.sync(
                client=self._client, id=prediction_id, json_body=payload
            )
        )

    def get_prediction_overview(self, prediction_id: int) -> dto.PredictionResponse:
        return check_response(
            get_prediction.sync_detailed(client=self._client, id=prediction_id)
        )

    def get_prediction_forecast(
        self, prediction_id: int
    ) -> dto.PredictionForecastResponse:
        return check_response(
            get_prediction_forecast.sync_detailed(client=self._client, id=prediction_id)
        )

    def list_predictions(self) -> List[dto.PredictionResponse]:
        return check_not_unset(
            check_exists(get_predictions.sync(client=self._client)).predictions
        )

    def download_prediction_as_csv(
        self,
        prediction_id: int,
        output_file: Union[str, PathLike],
        separator: str = ",",
        quote_char: str = '"',
        escape_char: str = "\\",
    ) -> None:
        response = get_prediction_result_csv_data.sync_detailed(
            client=self._client,
            id=prediction_id,
            separator=separator,
            quote_char=quote_char,
            escape_char=escape_char,
        )
        if response.status_code != 200:
            raise ValueError(
                f"Error obtaining prediction from server: {str(response.content)}"
            )
        with open(output_file, "bw") as file:
            file.write(response.content)

    def _get_prediction_bytes_as_parquet(self, prediction_id: int) -> bytes:
        response = get_prediction_result_parquet_data.sync_detailed(
            client=self._client, id=prediction_id
        )
        if response.status_code != 200:
            raise ValueError(
                f"Error obtaining prediction from server: {str(response.content)}"
            )
        return response.content

    def download_prediction_as_parquet(
        self, prediction_id: int, output_file: Union[str, PathLike]
    ) -> None:
        with open(output_file, "bw") as file:
            parquet_bytes = self._get_prediction_bytes_as_parquet(prediction_id)
            file.write(parquet_bytes)

    def get_prediction_result_as_pandas(self, prediction_id: int) -> pd.DataFrame:
        stream = io.BytesIO(self._get_prediction_bytes_as_parquet(prediction_id))
        return pd.read_parquet(stream)

    def delete_prediction(self, prediction_id: int) -> None:
        delete_prediction.sync_detailed(client=self._client, id=prediction_id)

    def save_prediction_result_as_data_set(
        self, prediction_id: int, name: str, description: Optional[str] = None
    ) -> int:
        payload = dto.SavePredictionRequest(name=name, description=description)
        return check_exists(
            save_prediction.sync(
                client=self._client, id=prediction_id, json_body=payload
            )
        ).id

    ###############
    # Tests
    ###############

    def create_test(
        self,
        model_id: int,
        data_set_id: int,
        name: str,
        description: Optional[str] = None,
        wait_until_complete: bool = True,
    ) -> int:
        test_id = check_exists(
            create_test.sync(
                client=self._client,
                json_body=dto.CreateTestRequest(
                    model_id=model_id,
                    data_set_id=data_set_id,
                    name=name,
                    description=description or UNSET,
                ),
            )
        ).id
        if not wait_until_complete:
            return test_id

        return wait_for_test_to_complete(self._client, test_id)

    def edit_test(
        self, test_id: int, name: str, description: Optional[str] = None
    ) -> dto.TestResponse:
        payload = dto.EditTestRequest(name=name, description=description)
        return check_exists(
            edit_test.sync(client=self._client, id=test_id, json_body=payload)
        )

    def get_test_overview(self, test_id: int) -> dto.TestResponse:
        return check_response(get_test.sync_detailed(client=self._client, id=test_id))

    def list_test(self) -> List[dto.TestResponse]:
        return check_not_unset(check_exists(get_tests.sync(client=self._client)).tests)

    def download_test_as_csv(
        self,
        test_id: int,
        output_file: Union[str, PathLike],
        separator: str = ",",
        quote_char: str = '"',
        escape_char: str = "\\",
    ) -> None:
        response = get_test_result_csv_data.sync_detailed(
            client=self._client,
            id=test_id,
            separator=separator,
            quote_char=quote_char,
            escape_char=escape_char,
        )
        if response.status_code != 200:
            raise ValueError(
                f"Error obtaining test from server: {str(response.content)}"
            )
        with open(output_file, "bw") as file:
            file.write(response.content)

    def _get_test_bytes_as_parquet(self, test_id: int) -> bytes:
        response = get_test_result_parquet_data.sync_detailed(
            client=self._client, id=test_id
        )
        if response.status_code != 200:
            raise ValueError(
                f"Error obtaining test from server: {str(response.content)}"
            )
        return response.content

    def download_test_as_parquet(
        self, test_id: int, output_file: Union[str, PathLike]
    ) -> None:
        with open(output_file, "bw") as file:
            parquet_bytes = self._get_test_bytes_as_parquet(test_id)
            file.write(parquet_bytes)

    def get_test_result_as_pandas(self, test_id: int) -> pd.DataFrame:
        with tempfile.TemporaryFile() as file:
            file.write(self._get_test_bytes_as_parquet(test_id))
            file.seek(0)
            return pd.read_parquet(path=file)

    def delete_test(self, test_id: int) -> None:
        delete_test.sync_detailed(client=self._client, id=test_id)

    def save_test_result_as_data_set(
        self, test_id: int, name: str, description: Optional[str] = None
    ) -> int:
        payload = dto.SaveTestRequest(name=name, description=description)
        return check_exists(
            save_test.sync(client=self._client, id=test_id, json_body=payload)
        ).id

    ################
    # APIs - Model #
    ################

    def list_model_apis(self) -> List[dto.DeployedModelApiResponse]:
        return check_not_unset(
            check_exists(get_model_apis.sync(client=self._client)).published_models
        )

    def delete_model_api(self, model_api_id: int) -> None:
        delete_model_api.sync_detailed(client=self._client, model_api_id=model_api_id)

    def create_model_api(
        self, model_id: int, name: str, description: Optional[str] = None
    ) -> int:
        response = create_model_api.sync_detailed(
            client=self._client,
            json_body=dto.CreateDeployedModelApiRequest(
                model_id=model_id, name=name, description=description or UNSET
            ),
        )
        return wait_for_future_to_succeed(self._client, response).additional_properties[
            "id"
        ]

    def edit_model_api(
        self, api_id: int, name: str, description: Optional[str] = None
    ) -> dto.DeployedModelApiResponse:
        payload = dto.EditDeployedModelApiRequest(name=name, description=description)
        return check_exists(
            edit_model_api.sync(
                client=self._client, model_api_id=api_id, json_body=payload
            )
        )

    def get_model_api(self, api_id: int) -> dto.DeployedModelApiResponse:
        return check_exists(
            get_model_api.sync(client=self._client, model_api_id=api_id)
        )

    def replace_model_api_model(
        self, api_id: int, new_model_id: int, notes: str
    ) -> int:
        response = replace_model_api.sync_detailed(
            client=self._client,
            model_api_id=api_id,
            json_body=dto.UpdateDeployedModelApiRequest(
                new_model_id=new_model_id, notes=notes
            ),
        )
        return wait_for_future_to_succeed(self._client, response).additional_properties[
            "id"
        ]

    def list_model_api_clients(
        self, api_id: int
    ) -> List[dto.DeployedApiClientResponse]:
        return check_not_unset(
            check_exists(
                get_model_api_clients.sync(client=self._client, model_api_id=api_id)
            ).api_clients
        )

    def delete_model_api_client(self, model_api_id: int, client_id: str) -> None:
        delete_model_api_client.sync_detailed(
            client=self._client, model_api_id=model_api_id, client_id=client_id
        )

    def create_model_api_client(
        self, api_id: int, name: str
    ) -> dto.DeployedApiClientCreateResponse:
        return check_exists(
            create_model_api_client.sync(
                client=self._client,
                model_api_id=api_id,
                json_body=dto.CreateDeployedApiClientRequest(name=name),
            )
        )

    def get_model_api_client(
        self, api_id: int, client_id: str
    ) -> dto.DeployedApiClientResponse:
        return check_exists(
            get_model_api_client.sync(
                client=self._client, model_api_id=api_id, client_id=client_id
            )
        )

    ###################
    # APIs - Pipeline #
    ###################

    def list_pipeline_apis(self) -> List[dto.DeployedPipelineApiResponse]:
        return check_not_unset(
            check_exists(
                get_pipeline_apis.sync(client=self._client)
            ).published_pipelines
        )

    def delete_pipeline_api(self, pipeline_api_id: int) -> None:
        delete_pipeline_api.sync_detailed(
            client=self._client, pipeline_api_id=pipeline_api_id
        )

    def create_pipeline_api(
        self, pipeline_id: int, name: str, description: Optional[str] = None
    ) -> int:
        response = create_pipeline_api.sync_detailed(
            client=self._client,
            json_body=dto.CreateDeployedPipelineApiRequest(
                pipeline_id=pipeline_id, name=name, description=description or UNSET
            ),
        )
        return wait_for_future_to_succeed(self._client, response).additional_properties[
            "id"
        ]

    def edit_pipeline_api(
        self, api_id: int, name: str, description: Optional[str] = None
    ) -> dto.DeployedPipelineApiResponse:
        payload = dto.EditDeployedPipelineApiRequest(name=name, description=description)
        return check_exists(
            edit_pipeline_api.sync(
                client=self._client, pipeline_api_id=api_id, json_body=payload
            )
        )

    def get_pipeline_api(self, api_id: int) -> dto.DeployedPipelineApiResponse:
        return check_exists(
            get_pipeline_api.sync(client=self._client, pipeline_api_id=api_id)
        )

    def replace_pipeline_api_pipeline(
        self, api_id: int, new_pipeline_id: int, notes: str
    ) -> int:
        response = replace_pipeline_api.sync_detailed(
            client=self._client,
            pipeline_api_id=api_id,
            json_body=dto.UpdateDeployedPipelineApiRequest(
                new_pipeline_id=new_pipeline_id, notes=notes
            ),
        )
        return wait_for_future_to_succeed(self._client, response).additional_properties[
            "id"
        ]

    def list_pipeline_api_clients(
        self, api_id: int
    ) -> List[dto.DeployedApiClientResponse]:
        return check_not_unset(
            check_exists(
                get_pipeline_api_clients.sync(
                    client=self._client, pipeline_api_id=api_id
                )
            ).api_clients
        )

    def delete_pipeline_api_client(self, pipeline_api_id: int, client_id: str) -> None:
        delete_pipeline_api_client.sync_detailed(
            client=self._client, pipeline_api_id=pipeline_api_id, client_id=client_id
        )

    def create_pipeline_api_client(
        self, api_id: int, name: str
    ) -> dto.DeployedApiClientCreateResponse:
        return check_exists(
            create_pipeline_api_client.sync(
                client=self._client,
                pipeline_api_id=api_id,
                json_body=dto.CreateDeployedApiClientRequest(name=name),
            )
        )

    def get_pipeline_api_client(
        self, api_id: int, client_id: str
    ) -> dto.DeployedApiClientResponse:
        return check_exists(
            get_pipeline_api_client.sync(
                client=self._client, pipeline_api_id=api_id, client_id=client_id
            )
        )


def _reward_matrix_dto_from_dataframe(
    rewards: pd.DataFrame,
) -> Tuple[str, List[dto.DecisioningDecision]]:
    n_class, n_decision = rewards.shape
    if n_class != 2:
        raise ValueError(
            "The decisions must have exactly two rewards, one for each class in the target."
        )
    if n_decision < 2:
        raise ValueError("You must provide at least two decisions to choose from")

    target_class = rewards.iloc[
        0
    ].name  # Choose the class of the first reward as the target

    return target_class, [
        dto.DecisioningDecision(
            label,
            # We don't have any chosen thresholds at this point...
            chosen_threshold=dto.DecisioningThreshold(0, 0),
            rewards=[
                dto.DecisioningReward(class_name=class_name, reward=reward)
                for class_name, reward in decision.items()
            ],
        )
        for label, decision in rewards.items()
    ]
