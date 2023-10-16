import os
from datetime import datetime, timedelta
from typing import Any, List, Optional

import requests

__all__ = ["CdfTokenHandler"]

from odp.auth.odp.token_handler import TokenHandler


def not_none(value: Any) -> Any:
    if value is None:
        raise ValueError("Value should not be None")
    return value


class CdfTokenHandler(TokenHandler):
    """Automatically obtain CogniteClient bearer tokens, checks expiry"""

    DEFAULT_CDF_CLUSTER = "westeurope-1"
    DEFAULT_LOGIN_URL = (
        "https://oceandataplatform.b2clogin.com/oceandataplatform.onmicrosoft.com/B2C_1A_ROPC_Auth/oauth2/v2.0/token"
    )

    def __init__(
        self,
        client_id: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        cdf_cluster: Optional[str] = None,
        scopes: Optional[List[str]] = None,
        login_url: str = DEFAULT_LOGIN_URL,
        token_expiry_leeway: Optional[timedelta] = None,
    ):
        """

        Args:
            client_id: Azure Client ID
            username: Azure username
            password: Azure password
            cdf_cluster: CDF Cluster name. Example: "westeurope-1"
            scopes: Auth-scopes
            login_url: Azure AD login URL
            token_expiry_leeway: How long before actual token expiry to actually renew token
        """
        self._client_id = not_none(client_id or os.getenv("FEDERATED_CDF_CLIENT_ID"))
        self._username = not_none(username or os.getenv("FEDERATED_CDF_USERNAME"))
        self._password = not_none(password or os.getenv("FEDERATED_CDF_PASSWORD"))
        self.cluster = cdf_cluster or os.getenv("FEDERATED_CDF_CLUSTER") or self.DEFAULT_CDF_CLUSTER

        login_url = login_url or os.getenv("FEDERATED_CDF_LOGIN_URL", self.DEFAULT_LOGIN_URL)

        if not token_expiry_leeway:
            token_expiry_leeway = timedelta(
                seconds=float(os.getenv("FEDERATED_CDF_TOKEN_EXPIRY_BUFFER_PERIOD_SECONDS", 3600))
                or self.TOKEN_EXPIRY_LEEWAY_PERIOD_DEFAULT_SECONDS  # noqa: W503
            )

        if not scopes:
            load_scopes = os.getenv("FEDERATED_CDF_SCOPES")
            if load_scopes:
                scopes = load_scopes.split(",")
            else:
                scopes = [
                    f"https://{self.cluster}.cognitedata.com/user_impersonation",
                    *self.DEFAULT_SCOPES,
                ]

        super().__init__(scopes, login_url, token_expiry_leeway)

    def __call__(self) -> str:
        return self.get_token()

    def _renew_token(self) -> None:
        """Renew token"""

        req = requests.post(
            self._login_url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "password",
                "client_id": self._client_id,
                "scope": " ".join(self._scopes),
                "username": self._username,
                "password": self._password,
            },
        )

        req.raise_for_status()
        creds = req.json()

        # Update token and expiry date
        self._token = creds["access_token"]
        self._token_expiry = datetime.now() + timedelta(seconds=int(creds["expires_in"]))
