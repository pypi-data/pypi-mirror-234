from typing import Dict

from attr import attrs

from mindfoundry.client.analyze.swagger import Client
from mindfoundry.client.analyze.utils._refreshable_access_token import (
    RefreshableAccessToken,
)


@attrs(auto_attribs=True)
class TokenAuthenticatedClient(Client):
    """A client for the swagger API that adds an authentication token to the request using the provided token generator"""

    token_generator: RefreshableAccessToken

    def get_headers(self) -> Dict[str, str]:
        """Get headers to be used in authenticated endpoints"""
        return {
            "Authorization": f"Bearer {self.token_generator.get_token()}",
            **self.headers,
        }
