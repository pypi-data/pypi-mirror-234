from collections import namedtuple
from typing import Any, Dict, List, Optional, Union

from prefect.flows import Flow

from .kubernetes import Kubernetes

K8sPodresourceSpec = namedtuple("K8sPodresourceSpec", ("cpu", "mem"))


class KubernetesTieredResource(Kubernetes):
    TIERS = {
        "default": K8sPodresourceSpec("1", "2Gi"),
        "minimal": K8sPodresourceSpec("1", "2Gi"),
        "small": K8sPodresourceSpec("2", "7Gi"),
        "medium": K8sPodresourceSpec("4", "14Gi"),
        "large": K8sPodresourceSpec("8", "28Gi"),
        "huge": K8sPodresourceSpec("14", "50Gi"),
    }

    TIER_LABEL = "oceandata.earth/tier"

    def __init__(
        self,
        flow: Flow,
        tier: Optional[str] = None,
        namespace: Optional[str] = None,
        env: Optional[Dict[str, Union[None, str]]] = None,
    ):
        super().__init__(flow=flow, namespace=namespace, env=env)

        self._tier = tier or "default"

        if self._tier not in self.TIERS:
            raise ValueError(f"Invalid tier: '{self._tier}'")

    def get_job_labels(self) -> Dict[str, str]:
        labels = super().get_job_labels()
        labels.update({self.TIER_LABEL: self._tier})

        return labels

    def get_customizations(self) -> List[Dict[str, Any]]:
        customizations = super().get_customizations()

        tier = self.TIERS[self._tier]

        return customizations + [
            {
                "op": "add",
                "path": "/spec/template/spec/containers/0/resources",
                "value": {
                    "requests": {"cpu": tier.cpu, "memory": tier.mem},
                    "limits": {"cpu": tier.cpu, "memory": tier.mem},
                },
            }
        ]
