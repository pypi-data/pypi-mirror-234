import pickle
from typing import Any, List, Optional

import redis

from odp.compute.flow_state.watermark_store import WatermarkStore

__all__ = ["WatermarkRedisStore"]


class WatermarkRedisStore(WatermarkStore):
    def __init__(self, *args, **kwargs):
        self.client = redis.Redis(*args, **kwargs)

    def get(self, key: str) -> Optional[Any]:
        ret = self.client.get(key.encode("utf-8"))
        if ret:
            ret = pickle.loads(ret)
        return ret

    def set(self, key: str, value: Any):
        self.client.set(key.encode("utf-8"), pickle.dumps(value))

    def list_keys(self, pattern: str) -> List[str]:
        ret = self.client.keys(pattern)
        return [key.decode("utf-8") for key in ret]
