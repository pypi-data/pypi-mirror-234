from dataclasses import asdict, dataclass
from typing import Optional

__all__ = ["DaskGatewayConfig"]


@dataclass
class DaskGatewayConfig:
    gateway_address: str
    gateway_token: str
    gateway_proxy_address: Optional[str] = None
    gateway_public_address: Optional[str] = None
    cluster_min_workers: Optional[int] = 0
    cluster_max_workers: Optional[int] = 2

    def dump(self, include_none_values: bool = False):
        return {key: val for key, val in asdict(self).items() if val is not None or include_none_values}

    def set_worker_count(self, min_count: int, max_count: int) -> "DaskGatewayConfig":
        min_count, max_count = min(min_count, max_count), max(min_count, max_count)
        self.cluster_min_workers = min_count
        self.cluster_max_workers = max_count

        return self
