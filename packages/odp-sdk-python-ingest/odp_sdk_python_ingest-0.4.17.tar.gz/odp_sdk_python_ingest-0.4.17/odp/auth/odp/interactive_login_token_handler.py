import logging
import sys
from datetime import datetime, timedelta
from typing import List, Optional

import msal
import msal_extensions

from .token_handler import TokenHandler

__all__ = ["InteractiveLoginTokenHandler"]

LOG = logging.getLogger(__name__)


class InteractiveLoginTokenHandler(TokenHandler):
    DEFAULT_CLIENT_ID = "2a18c352-e7ab-4437-96df-6036d815b3fc"
    DEFAULT_AUTHORITY = (
        "https://oceandataplatform.b2clogin.com/oceandataplatform.onmicrosoft.com/B2C_1A_signup_signin_custom"
    )
    DEFAULT_SCOPES = ["https://oceandataplatform.onmicrosoft.com/odp-backend/ODP_ACCESS"]

    def __init__(
        self,
        client_id: Optional[str] = None,
        authority: Optional[str] = None,
        scopes: Optional[List[str]] = None,
        token_expiry_leeway: Optional[timedelta] = None,
    ):
        super().__init__(scopes=scopes, token_expiry_leeway=token_expiry_leeway)

        self._client_id = client_id or self.DEFAULT_CLIENT_ID
        self._authority = authority or self.DEFAULT_AUTHORITY

        persistence = self._build_persistence(".token_cache.bin", True)
        cache = msal_extensions.PersistedTokenCache(persistence)

        self._app = msal.PublicClientApplication(
            client_id=self._client_id, authority=self._authority, token_cache=cache
        )

    @staticmethod
    def _build_persistence(location: str, fallback_to_plaintext: bool = False):
        if sys.platform.startswith("win"):
            return msal_extensions.FilePersistenceWithDataProtection(location)
        elif sys.platform.startswith("darwin"):
            return msal_extensions.KeychainPersistence(location, "odp-prefect", "prefect-user")
        elif sys.platform.startswith("linux"):
            try:
                return msal_extensions.LibsecretPersistence(
                    location,
                    schema_name="prefect",
                    attributes={"app": "prefect", "component": "odp-prefect-cli"},
                )
            except Exception:
                if not fallback_to_plaintext:
                    raise
                LOG.warning("Encryption unavailable. Opting in to plaintext")
        return msal_extensions.FilePersistence(location)

    def _renew_token(self) -> None:
        accounts = self._app.get_accounts()
        if accounts and len(accounts) == 1:
            account = accounts[0]

            LOG.info("Account '%s' exists in cache. Trying token..", account["username"])
            token = self._app.acquire_token_silent(scopes=self._scopes, account=account)
        else:
            token = None

        if token is None:
            LOG.info("Not suitable token exists in cache. Refreshing token..")
            token = self._app.acquire_token_interactive(
                scopes=self._scopes,
            )

        if not token:
            raise RuntimeError("Failed to obtain user token")

        if "id_token_claims" in token:
            claims = token["id_token_claims"]
            exp = claims["exp"]
            self._token = token["id_token"]
        elif "access_token" in token:
            exp = token["expires_in"]
            self._token = token["access_token"]
        else:
            raise RuntimeError("Invalid user token")

        self._token_expiry = datetime.fromtimestamp(exp)
