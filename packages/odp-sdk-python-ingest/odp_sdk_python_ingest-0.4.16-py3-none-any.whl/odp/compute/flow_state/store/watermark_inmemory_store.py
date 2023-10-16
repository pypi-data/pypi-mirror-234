from typing import Any, List, Optional

from odp.compute.flow_state.watermark_store import WatermarkStore

__all__ = ["WatermarkInmemoryStore"]


class WatermarkInmemoryStore(WatermarkStore, dict):
    def __init__(self, seq=None, **kwargs):
        if seq is None:
            dict.__init__(self, **kwargs)
        else:
            dict.__init__(self, seq, **kwargs)

    def get(self, key: str) -> Optional[Any]:
        return dict.get(self, key)

    def set(self, key: str, value: Any):
        self[key] = value

    def list_keys(self, pattern: str) -> List[str]:
        raise NotImplementedError("Listing keys is not supported")
