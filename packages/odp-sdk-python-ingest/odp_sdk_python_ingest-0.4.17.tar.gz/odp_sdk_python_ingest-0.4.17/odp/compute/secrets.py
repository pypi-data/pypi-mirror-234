import base64
import logging
import platform
from abc import ABC, abstractmethod
from os import environ, getenv, path
from typing import Any, Dict, Optional, Type, Union

import pykube
from azure.identity import ClientSecretCredential, DefaultAzureCredential

LOG = logging.getLogger(__name__)

KUBERNETES_SECRET_NAME = "azure-sp-secret"


def is_windows():
    return platform.system().upper() == "WINDOWS"


class RuntimeSecretBackend(ABC):
    def __init__(
        self,
        secret_name: str,
        secret_key: Optional[str] = None,
        raise_if_missing: Optional[bool] = True,
        **_,
    ):
        self.secret_name = secret_name
        self.secret_key = secret_key
        self.raise_if_missing = raise_if_missing

    @abstractmethod
    def _get(self) -> Any:
        pass

    @classmethod
    def get(
        cls,
        secret_name: str,
        secret_key: Optional[str] = None,
        raise_if_missing: Optional[bool] = True,
        **kwargs: Dict,
    ) -> Any:
        obj = cls(
            secret_name=secret_name,
            secret_key=secret_key,
            raise_if_missing=raise_if_missing,
            **kwargs,
        )

        return obj._get()


class EnvRuntimeSecret(RuntimeSecretBackend):
    def __init__(
        self,
        secret_name: str,
        secret_key: Optional[str] = None,
        raise_if_missing: Optional[bool] = True,
        allow_platform_compensation: Optional[bool] = is_windows(),
    ):
        super().__init__(secret_name, secret_key, raise_if_missing)
        self.allow_platform_compensation = allow_platform_compensation

    def _maybe_raise(self, key: str, value: Any) -> Any:
        if value is None:
            if self.raise_if_missing:
                raise KeyError(f"Missing secret: {key}")
            else:
                return None
        else:
            return value

    def _platform_compatible_key(self, key: str):
        return key.upper()

    def _getenv(self, key, default=None):
        if self.allow_platform_compensation:
            key = self._platform_compatible_key(key)

        return getenv(key, default)

    def _get(self):
        if self.secret_name:
            if self.secret_key:
                value = self._getenv(f"{self.secret_name}_{self.secret_key}")
                return self._maybe_raise(self.secret_key, value)
            else:
                if self.allow_platform_compensation:
                    sn = self._platform_compatible_key(self.secret_name)
                else:
                    sn = self.secret_name

                ret = {key[len(sn) + 1 :]: environ[key] for key in environ if key.startswith(sn)}
                if self.allow_platform_compensation:
                    return {key.lower(): val for key, val in ret.items()}
                else:
                    return ret

        elif not self.secret_key:
            raise ValueError("At least one of secret_name or secret_key must be set")
        else:
            value = self._getenv(self.secret_key)
            return self._maybe_raise(self.secret_key, value)


class KubernetesRuntimeSecret(RuntimeSecretBackend):
    SERVICE_ACCOUNT_MOUNT_PATH = "/var/run/secrets/kubernetes.io/serviceaccount"

    def __init__(
        self,
        secret_name: str,
        secret_key: Optional[str] = None,
        namespace: Optional[str] = None,
        exclude_sa_credential: Optional[bool] = False,
        raise_if_missing: Optional[bool] = True,
        k8s_api: Optional[pykube.HTTPClient] = None,
    ):
        super().__init__(secret_name, secret_key, raise_if_missing)
        self.namespace = namespace
        self.exclude_sa_credential = exclude_sa_credential
        self.k8s_api = k8s_api

    def _get(self):
        if self.k8s_api is None:
            self.k8s_api = pykube.HTTPClient(pykube.KubeConfig.from_service_account())

        namespace = self.namespace
        if not namespace and not self.exclude_sa_credential:
            LOG.debug("Namespace not set. Attempting to read from service account")
            namespace = open(path.join(self.SERVICE_ACCOUNT_MOUNT_PATH, "namespace")).read()

        LOG.info(f"Reading secret for {namespace}.{self.secret_name}")

        secret_obj = pykube.Secret.objects(self.k8s_api, namespace=namespace).get_by_name(self.secret_name)
        secret_data = secret_obj.obj["data"]

        if self.secret_key:
            if self.secret_key in secret_data:
                return base64.b64decode(secret_data[self.secret_key]).decode("utf-8")
            else:
                if self.raise_if_missing:
                    raise KeyError(f"Cannot find the key {self.secret_key} in {self.secret_name}")
                else:
                    return None
        else:
            return {key: base64.b64decode(value).decode("utf-8") for key, value in secret_data.items()}


def get_runtime_secret_backend() -> Type:
    if "PREFECT__CONTEXT__FLOW_RUN_ID" in environ:
        return KubernetesRuntimeSecret
    else:
        return EnvRuntimeSecret


def get_client_credential() -> Union[ClientSecretCredential, DefaultAzureCredential]:
    if "PREFECT__CONTEXT__FLOW_RUN_ID" in environ:
        secret_backend = get_runtime_secret_backend()
        return ClientSecretCredential(**secret_backend.get(secret_name=KUBERNETES_SECRET_NAME))
    else:
        return DefaultAzureCredential(
            exclude_visual_studio_code_credential=True,
            exclude_shared_token_cache_credential=True,
        )
