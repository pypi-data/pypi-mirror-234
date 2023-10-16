import os
import random
import string
import warnings
from typing import Dict, Optional, Union

from dask import distributed
from dask_kubernetes.classic import KubeCluster, make_pod_spec
from prefect.flows import Flow
from prefect_dask import DaskTaskRunner

from .kubernetes_tiered_resource import KubernetesTieredResource


class _DaskTaskRunnerWrapper(DaskTaskRunner):
    @property
    def name(self):
        return "ephemeralDask"

    def __getstate__(self):
        data = self.__dict__.copy()
        data.update({k: None for k in {"_client", "_cluster", "_connect_to"}})

        openapi_types = data["cluster_kwargs"]["pod_template"].spec.openapi_types.copy()
        openapi_types.pop("host_users", None)

        data["cluster_kwargs"]["pod_template"].spec.openapi_types = openapi_types
        return data

    def __setstate__(self, state: dict):
        self.__dict__.update(state)
        try:
            self._client = distributed.get_client()
        except ValueError:
            self._client = None


class KubernetesDask(KubernetesTieredResource):
    ENV_DASK_GATEWAY_ADDRESS = "DASK_GATEWAY_ADDRESS"
    ENV_K8S_SERVICE_ACCOUNT = "K8S_SERVICE_ACCOUNT"

    def __init__(
        self,
        flow: Flow,
        tier: Optional[str] = None,
        cluster_tier: Optional[str] = None,
        min_workers: int = 1,
        max_workers: int = 2,
        namespace: Optional[str] = None,
        env: Optional[Dict[str, Union[None, str]]] = None,
        service_account: Optional[str] = None,
    ):
        warnings.warn("The KubernetesDask runtime is currently not supported")
        super().__init__(flow, tier, namespace, env)

        self._service_account = service_account or os.environ.get(self.ENV_K8S_SERVICE_ACCOUNT, "dask-gateway")

        # Cluster nodes defaults to the same tier as the flow
        self._cluster_tier = cluster_tier or self._tier
        self._min_workers = min_workers
        self._max_workers = max_workers

    def apply_flow_options(self, flow: Flow):
        flow_version = flow.version or "DIRTY"

        resources = self.TIERS[self._cluster_tier]

        # extra_labels = {"prefect.io/flow": self._flow.name, "hubocean.io/clusterTier": self._cluster_tier}
        # extra_annotations = {"prefect.io/flow": self._flow.name, "hubocean.io/clusterTier": self._cluster_tier}

        flow.task_runner = _DaskTaskRunnerWrapper(
            cluster_class=KubeCluster,
            cluster_kwargs={
                "pod_template": make_pod_spec(
                    image=self._storage.get_name(),
                    memory_limit=resources.mem,
                    cpu_limit=resources.cpu,
                    labels={
                        "dask.org/ephemeral": "true",
                        "dask.org/owner": "prefect",
                        "prefect.io/flow-name": flow.name,
                        "prefect.io/flow-version": flow_version,
                    },
                ),
                "name": f"dask-{flow.name}-" + "".join(random.sample(string.ascii_lowercase, 6)),
                "namespace": self._namespace,
                "env": {
                    "ODP__WATERMARK_STORE_CLS": os.environ.get(
                        self.ENV_ODP_WATERMARK_STORE_CLS,
                        "odp.compute.watermark.store.WatermarkRedisStore",
                    ),
                    "ODP__WATERMARK_STORE_ARGS": os.environ.get(
                        self.ENV_ODP_WATERMARK_STORE_ARGS, "prefect-redis-master"
                    ),
                    "ODP__METRIC_CLIENT_CLS": os.environ.get(
                        self.ENV_ODP_METRIC_CLIENT_CLS,
                        "odp.compute.metrics.client.MetricPrometheusClient",
                    ),
                    "ODP__METRIC_CLIENT_ARGS": os.environ.get(
                        self.ENV_ODP_METRIC_CLIENT_ARGS,
                        "prefect-prometheus-pushgateway:9091",
                    ),
                    "EXTRA_PIP_PACKAGES": "bokeh<3",
                },
            },
            adapt_kwargs={
                "minimum": self._min_workers,
                "maximum": self._max_workers,
            },
            client_kwargs={"set_as_default": True},
        )

    # def get_customizations(self) -> List[Dict[str, Any]]:
    #     customizations = super().get_customizations()

    #     return customizations + [
    #         {
    #             "op": "add",
    #             "path": "/spec/template/spec/serviceAccountName",
    #             "value": self._service_account,
    #         }
    #     ]
