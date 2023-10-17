from time import time

import httpx


class RefreshableAccessToken:
    def __init__(self, auth_token_url: str, credentials: httpx.Auth):
        """
        Get an OAuth access token that is currently valid

        :param auth_token_url: The address of the authentication token endpoint
        :param credentials: The credentials to use to access the authentication token endpoint
        """
        self.auth_token_url = auth_token_url
        self.credentials = credentials
        self._token_expiry_time = 0
        self._access_token = "invalid"

    def get_token(self) -> str:
        """Get a token that is currently valid, refreshing the token if necessary"""

        if self._token_expiry_time <= (int(time()) + 10):
            self._get_new_access_token()

        return self._access_token

    def _get_new_access_token(self):
        """Get a new token from the access token endpoint using the supplied credentials"""
        response = httpx.post(
            self.auth_token_url,
            auth=self.credentials,
            data={"grant_type": "client_credentials"},
        )

        if response.status_code == httpx.codes.CREATED:
            self._access_token = response.json()["access_token"]
            self._token_expiry_time = int(time()) + int(response.json()["expires_in"])
        else:
            raise Exception(response.text)
