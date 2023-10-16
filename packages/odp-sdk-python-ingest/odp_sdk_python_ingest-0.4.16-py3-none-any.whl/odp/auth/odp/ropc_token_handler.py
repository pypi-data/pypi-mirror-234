import os
from datetime import datetime, timedelta
from typing import List, Optional

import requests

from .token_handler import TokenHandler


class RopcTokenHandler(TokenHandler):
    DEFAULT_CLIENT_ID = "33b5d769-787b-466b-bc94-a10125f4c1ee"
    DEFAULT_LOGIN_URL = (
        "https://oceandataplatform.b2clogin.com/oceandataplatform.onmicrosoft.com/B2C_1A_ROPC_Auth/oauth2/v2.0/token"
    )
    DEFAULT_SCOPES = [
        "openid",
        "https://oceandataplatform.onmicrosoft.com/odp-backend/ODP_ACCESS",
    ]

    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        client_id: Optional[str] = None,
        scopes: Optional[List[str]] = None,
        login_url: Optional[str] = None,
        token_expiry_leeway: Optional[timedelta] = None,
    ):
        super().__init__(
            scopes=scopes,
            login_url=login_url or self.DEFAULT_LOGIN_URL,
            token_expiry_leeway=token_expiry_leeway,
        )

        self.__username = username or os.environ["ODP_ROPC_USERNAME"]
        self.__password = password or os.environ["ODP_ROPC_PASSWORD"]
        self._client_id = client_id or self.DEFAULT_CLIENT_ID

    def _renew_token(self) -> None:
        res = requests.post(
            self._login_url,
            params={
                "username": self.__username,
                "password": self.__password,
                "grant_type": "password",
                "client_id": self._client_id,
                "response_type": "token id_token",
                "scope": " ".join(self._scopes),
            },
        )

        res.raise_for_status()
        token = res.json()

        self._token = token["access_token"]
        self._token_expiry = datetime.now() + timedelta(seconds=int(token["expires_in"]))
