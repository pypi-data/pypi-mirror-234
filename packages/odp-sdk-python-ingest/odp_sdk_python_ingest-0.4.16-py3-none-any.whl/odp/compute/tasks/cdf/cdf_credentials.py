import json
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from datetime import timedelta
from typing import Callable, Dict, List, Optional, Union

from cognite.experimental import CogniteClient

from odp.auth.cdf import FederatedCogniteClient

TOKEN_EXPIRY_BUFFER_PERIOD_DEFAULT_SECONDS = 60.0
DEFAULT_CDF_CLUSTER = "westeurope-1"
DEFAULT_LOGIN_URL = (
    "https://oceandataplatform.b2clogin.com/oceandataplatform.onmicrosoft.com/B2C_1A_ROPC_Auth/oauth2/v2.0/token"
)
DEFAULT_SCOPES = ["openid"]


class CdfCredentials(ABC):
    @abstractmethod
    def client(self) -> CogniteClient:
        pass

    def login(self, client: Optional[CogniteClient] = None) -> CogniteClient:
        client = client or self.client()
        client.iam.token.inspect()

        return client

    @staticmethod
    def _nop(*args, **kwargs):
        pass

    @classmethod
    def make_client(cls, **kwargs) -> CogniteClient:
        return cls(**kwargs).client()

    @classmethod
    def from_str(cls, s: str):
        dct = json.loads(s)

        cls_str = dct.pop("cls", cls.__name__)

        if cls_str == CdfTokenCredentials.__name__ or cls_str == CdfCredentials.__name__:
            cls = CdfTokenCredentials
        elif cls_str == CdfFederatedCredentials.__name__:
            cls = CdfFederatedCredentials
        else:
            raise ValueError(f"Unsupported CDF credential class: {cls_str}")

        ret = cls(**dct)
        ret.login()

        return ret

    @classmethod
    def client_from_str(cls, s: str, client_name="prefect"):
        dct = json.loads(s)
        return cls.make_client(**dct, client_name=client_name)


@dataclass
class CdfTokenCredentials(CdfCredentials):
    api_key: str = None
    project: str = None
    client_name: str = None
    base_url: str = None
    max_workers: int = None
    headers: Dict[str, str] = None
    timeout: int = None
    token: Union[str, Callable[[], str], None] = None
    token_url: Optional[str] = None
    token_client_id: Optional[str] = None
    token_client_secret: Optional[str] = None
    token_scopes: Optional[List[str]] = None
    token_custom_args: Optional[Dict[str, str]] = None
    disable_pypi_version_check: Optional[bool] = None
    debug: bool = False
    server: Optional[str] = None

    def client(self) -> CogniteClient:
        client = CogniteClient(**{key: val for key, val in asdict(self).items() if val is not None})
        client.geospatial._log_request = self._nop
        return client


@dataclass
class CdfFederatedCredentials(CdfCredentials):
    project: str = None
    client_name: str = None
    token_client_id: Optional[str] = None
    token_username: Optional[str] = None
    token_password: Optional[str] = None
    token_scopes: Optional[List[str]] = None
    server: Optional[str] = None
    login_url: str = DEFAULT_LOGIN_URL
    token_expiry_leeway: Optional[timedelta] = None

    def client(self) -> CogniteClient:
        client = FederatedCogniteClient(**{key: val for key, val in asdict(self).items() if val is not None})
        client.geospatial._log_request = self._nop
        return client


__all__ = ["CdfCredentials", "CdfTokenCredentials", "CdfFederatedCredentials"]
