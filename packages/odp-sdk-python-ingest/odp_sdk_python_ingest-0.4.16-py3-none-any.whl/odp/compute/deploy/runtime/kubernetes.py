import os
from typing import Any, Dict, List, Optional, Union

from prefect.flows import Flow
from prefect.infrastructure import KubernetesJob
from prefect.utilities.pydantic import JsonPatch

from ..storage import AbstractStorage, Docker
from .abstract_runtime import AbstractRuntime

__all__ = ["Kubernetes"]


class Kubernetes(AbstractRuntime):
    ENV_KUBERNETES_NAMESPACE = "PREFECT_RUNTIME_NAMESPACE"
    ENV_ODP_WATERMARK_STORE_CLS = "ODP_WATERMARK_STORE_CLS"
    ENV_ODP_WATERMARK_STORE_ARGS = "ODP_WATERMARK_STORE_ARGS"
    ENV_ODP_METRIC_CLIENT_CLS = "ODP_METRIC_CLIENT_CLS"
    ENV_ODP_METRIC_CLIENT_ARGS = "ODP_METRIC_CLIENT_ARGS"

    JOB_TTL_SECONDS = 10

    def __init__(
        self,
        flow: Flow,
        namespace: Optional[str] = None,
        env: Optional[Dict[str, Union[None, str]]] = None,
        service_account_name: Optional[str] = None,
    ) -> None:
        super().__init__(flow)

        self._namespace: str = namespace or os.environ.get(self.ENV_KUBERNETES_NAMESPACE, "prefect")
        self._env = env
        self._service_account_name = service_account_name
        self._storage: Optional[Docker] = None

    def set_storage(self, storage: AbstractStorage):
        if not isinstance(storage, Docker):
            raise ValueError(
                "{} only accepts storage of type {}, but got {}".format(
                    self.__class__.__name__, Docker.__name__, storage.__class__.__name__
                )
            )
        self._storage = storage

    def digest(self) -> KubernetesJob:
        if not self._storage:
            raise ValueError("Kubernetes job storage is not set, but is required.")

        return KubernetesJob(
            image=self._storage.get_name(),
            env=self._get_job_env(),
            labels=self.get_job_labels(),
            name=f"orion-{self._flow.name}-{self._flow.version}",
            namespace=self._namespace,
            finished_job_ttl=self.JOB_TTL_SECONDS,
            customizations=JsonPatch(self.get_customizations()),
            service_account_name=self._service_account_name,
            stream_output=True,
        )

    def _get_job_env(self) -> Dict[str, Union[str, None]]:
        if self._env:
            env = self._env.copy()
        else:
            env = {}

        env.update(
            {
                "ODP__WATERMARK_STORE_CLS": os.environ.get(
                    self.ENV_ODP_WATERMARK_STORE_CLS,
                    "odp.compute.watermark.store.WatermarkRedisStore",
                ),
                "ODP__WATERMARK_STORE_ARGS": os.environ.get(self.ENV_ODP_WATERMARK_STORE_ARGS, "prefect-redis-master"),
                "ODP__METRIC_CLIENT_CLS": os.environ.get(
                    self.ENV_ODP_METRIC_CLIENT_CLS,
                    "odp.compute.metrics.client.MetricPrometheusClient",
                ),
                "ODP__METRIC_CLIENT_ARGS": os.environ.get(
                    self.ENV_ODP_METRIC_CLIENT_ARGS,
                    "prefect-prometheus-pushgateway:9091",
                ),
                "PREFECT_LOGGING_LEVEL": "DEBUG",
            }
        )

        return env

    def get_job_labels(self) -> Dict[str, str]:
        return {
            "prefect.io/flowName": self._flow.name,
            "prefect.io/flowVersion": self._flow.version,
            "prefect.io/taskRunner": self._flow.task_runner.name,
        }

    def get_customizations(self) -> List[Dict[str, Any]]:
        return []
