from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Optional


class TokenHandler(ABC):
    TOKEN_EXPIRY_LEEWAY_PERIOD_DEFAULT_SECONDS = 60.0
    DEFAULT_LOGIN_URL = (
        "https://oceandataplatform.b2clogin.com/oceandataplatform.onmicrosoft.com/B2C_1A_ROPC_Auth/oauth2/v2.0/token"
    )
    DEFAULT_SCOPES = ["openid"]

    def __init__(
        self,
        scopes: Optional[List[str]] = None,
        login_url: str = DEFAULT_LOGIN_URL,
        token_expiry_leeway: Optional[timedelta] = None,
    ):
        self._token = None
        self._token_expiry = datetime.fromtimestamp(0)

        self._login_url = login_url or self.DEFAULT_LOGIN_URL
        self._token_expiry_leeway = token_expiry_leeway or timedelta(self.TOKEN_EXPIRY_LEEWAY_PERIOD_DEFAULT_SECONDS)
        self._scopes = scopes or self.DEFAULT_SCOPES

    def get_token(self) -> str:
        """Check token expiry and renew if necessary

        Returns:
            Bearer token
        """

        if datetime.utcnow() + self._token_expiry_leeway > self._token_expiry:
            self._renew_token()
        return self._token

    @abstractmethod
    def _renew_token(self) -> None:
        """Abstract method that must renew the token.

        This method must overwrite `self._token` and `self._token_expiry_time`
        """
