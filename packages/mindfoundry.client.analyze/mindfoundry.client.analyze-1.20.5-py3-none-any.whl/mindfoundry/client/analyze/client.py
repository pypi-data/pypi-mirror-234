import pandas as pd
import requests
from httpx import BasicAuth

from mindfoundry.client.analyze.project_api_swagger_client import (
    AnalyzeSwaggerClientWrapper,
)
from mindfoundry.client.analyze.swagger import Client
from mindfoundry.client.analyze.utils import (
    RefreshableAccessToken,
    TokenAuthenticatedClient,
    get_valid_base_url,
)


def create_project_api_swagger_client(
    base_url: str, client_id: str, client_secret: str
) -> Client:
    """
    Create a client for calling the Analyze Project API

    e.g.
    >>> base_url = "https://example.app.mindfoundry.ai/"
    >>> analyze_client = create_project_api_client(base_url, "<client_id>", "<client_secret>")
    >>> data = pd.DataFrame({"foo": [1, 2], "bar": [3, 4]})
    >>> model_api = analyze_client.create_file_data_set(data, "Data Set Name")

    :param base_url: the base url for Analyze
    :param client_id: the client id for the Project API
    :param client_secret: the client secret for the Project API
    """
    base_url = get_valid_base_url(base_url)
    auth_token_url = base_url.strip("/") + "/api/auth/token"
    api_url = base_url.strip("/") + "/api"
    client = TokenAuthenticatedClient(
        base_url=api_url,
        token_generator=RefreshableAccessToken(
            auth_token_url=auth_token_url,
            credentials=BasicAuth(client_id, client_secret),
        ),
        timeout=60,
    )
    return client


def create_project_api_client(
    base_url: str, client_id: str, client_secret: str
) -> AnalyzeSwaggerClientWrapper:
    """
    Create a client for calling the Analyze Project API

    e.g.
    >>> base_url = "https://example.app.mindfoundry.ai/"
    >>> analyze_client = create_project_api_client(base_url, "<client_id>", "<client_secret>")
    >>> data = pd.DataFrame({"foo": [1, 2], "bar": [3, 4]})
    >>> model_api = analyze_client.create_file_data_set(data, "Data Set Name")

    :param base_url: the base url for Analyze
    :param client_id: the client id for the Project API
    :param client_secret: the client secret for the Project API
    """
    client = create_project_api_swagger_client(base_url, client_id, client_secret)
    return AnalyzeSwaggerClientWrapper(client)


class PublishedApi:
    def __init__(
        self, base_url: str, api_endpoint: str, client_id: str, client_secret: str
    ):
        """
        Create a client for calling a published model api.

        e.g.
        >>> base_url = "https://example.app.mindfoundry.ai"
        >>> analyze_client = create_project_api_client(base_url, "client_id", "client_secret")
        >>> model_api_id = analyze_client.create_model_api(123, "new api")
        >>> model_api = analyze_client.get_model_api(model_api_id)
        >>> client_credentials = analyze_client.create_model_api_client(model_api.id, "credentials for new api")
        >>>
        >>> model_api_client = PublishedApi(base_url, model_api.api_endpoint, client_credentials.id, client_credentials.secret))  # pylint: disable=line-too-long
        >>> features = pd.DataFrame(...)
        >>> predictions = model_api_client.transform(features)

        :param base_url: the same base url used for the analyze client
        :param api_endpoint: the 'apiEndpoint' value from AnalyzeClient.create_model_api response
        :param client_id: the 'id' value from AnalyzeClient.create_api_client response
        :param client_secret: the 'secret' value from AnalyzeClient.create_api_client response
        """
        base_url = get_valid_base_url(base_url)
        self._base_url = base_url.strip("/")
        self._token_generator = RefreshableAccessToken(
            auth_token_url=self._base_url + "/api/auth/token",
            credentials=BasicAuth(client_id, client_secret),
        )
        self._api_endpoint = api_endpoint

    def transform(self, features: pd.DataFrame):
        payload = {
            "records": features.to_dict("records"),
        }

        response = self._request("POST", self._api_endpoint, json=payload)

        return response.json()

    def _request(self, *args, **kwargs):
        kwargs["headers"] = {
            "Authorization": "Bearer " + self._token_generator.get_token()
        }
        response = requests.request(*args, **kwargs, timeout=60)
        if response.ok:
            return response
        else:
            raise Exception(response.text)
