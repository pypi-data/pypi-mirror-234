import json
from typing import Union

from mindfoundry.client.analyze.client import create_project_api_swagger_client
from mindfoundry.client.analyze.swagger import Client
from mindfoundry.client.analyze.utils import get_valid_base_url
from mindfoundry.client.analyze.utils.typing import PathLike


class Connection:
    def __init__(self, base_url: str, client_id: str, client_secret: str):
        self.base_url = get_valid_base_url(base_url)
        self.client_id = client_id
        self.client_secret = client_secret

    def to_file(self, path: PathLike) -> None:
        dict_repr = {
            "connection": {
                "base_url": self.base_url,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            }
        }
        with open(path, "w", encoding="UTF-8") as file:
            json.dump(dict_repr, file)

    @classmethod
    def from_file(cls, path: PathLike) -> "Connection":
        with open(path, mode="r", encoding="UTF-8") as file:
            config = json.load(file)

            if "connection" not in config.keys():
                raise Exception("Not a connection")
            connection_config = config["connection"]

            if "base_url" not in connection_config.keys():
                raise Exception(
                    "Configuration did not represent an Analyze connection - No base_url saved"
                )
            base_url = connection_config["base_url"]

            if "client_id" not in connection_config.keys():
                raise Exception(
                    "Configuration did not represent an Analyze connection - No client_id saved"
                )
            client_id = connection_config["client_id"]

            if "client_secret" not in connection_config.keys():
                raise Exception(
                    "Configuration did not represent an Analyze connection - No client_secret saved"
                )
            client_secret = connection_config["client_secret"]

        return Connection(base_url, client_id, client_secret)


ConnectionLike = Union[PathLike, "Connection"]


def from_connectionlike(connection: ConnectionLike) -> Connection:
    if isinstance(connection, Connection):
        return connection
    # If we've been given a pathlike, load the connection information from the pathlike
    return Connection.from_file(connection)


def client_from_connectionlike(connection: ConnectionLike) -> Client:
    connection = from_connectionlike(connection)
    return create_project_api_swagger_client(
        connection.base_url,
        connection.client_id,
        connection.client_secret,
    )
