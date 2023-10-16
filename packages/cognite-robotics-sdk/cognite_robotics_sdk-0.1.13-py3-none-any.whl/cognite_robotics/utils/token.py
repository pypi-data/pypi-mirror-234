# -*- coding: utf-8 -*-
"""Token generator."""
import datetime
from typing import Callable, Dict, List

from cognite.client.exceptions import CogniteAPIError
from oauthlib.oauth2 import BackendApplicationClient, OAuth2Error
from requests_oauthlib import OAuth2Session


class TokenGenerator:
    """Token generator for OAuth2.0 client credentials flow."""

    def __init__(
        self,
        token_url: str,
        client_id: str,
        client_secret: str,
        scopes: List[str],
        custom_args: Dict[str, str],
    ):
        """Initialize token generator."""
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = scopes
        self.custom_args = custom_args

        if self.token_params_set():
            self._generate_access_token()
        else:
            self._access_token = None
            self._access_token_expires_at = None

    def return_access_token(self) -> str:
        """Return access token."""
        if not self.token_params_set():
            raise CogniteAPIError(message="Could not generate access token - missing token generation arguments", code=401)
        elif self._access_token is None:
            raise CogniteAPIError(message="Could not generate access token from provided token generation arguments", code=401)

        if self._access_token_expires_at < datetime.datetime.now().timestamp():
            self._generate_access_token()

        return self._access_token

    def _generate_access_token(self) -> None:
        try:
            client = BackendApplicationClient(client_id=self.client_id)
            oauth = OAuth2Session(client=client)
            token_result = oauth.fetch_token(
                token_url=self.token_url,
                client_id=self.client_id,
                client_secret=self.client_secret,
                scope=self.scopes,
                **self.custom_args,
            )
        except OAuth2Error as oauth_error:
            raise CogniteAPIError(
                message="Error generating access token: {0}, {1}, {2}".format(
                    oauth_error.error, oauth_error.status_code, oauth_error.description
                ),
                code=oauth_error.status_code,
            )
        else:
            self._access_token = token_result.get("access_token")
            self._access_token_expires_at = token_result.get("expires_at")

    def token_params_set(self) -> bool:
        """Check if token params are set."""
        return self.client_id is not None and self.client_secret is not None and self.token_url is not None and self.scopes is not None


def get_token_generator(tenant_id: str, client_id: str, client_secret: str, scopes: List[str]) -> Callable[[], str]:
    """Get token generator."""
    tg = TokenGenerator(
        f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token",
        client_id,
        client_secret,
        scopes,
        {},
    )
    return tg.return_access_token
