import pickle
from typing import Any, List, Optional, Union

from odp.compute.flow_state.watermark_store import WatermarkStore

__all__ = ["WatermarkFileStore"]


class WatermarkFileStore(WatermarkStore):
    def __init__(self, fname_template: str, create_if_not_exists: Union[str, bool] = True):
        self.fname_template = fname_template
        self.create_if_not_exists = bool(create_if_not_exists)

    def _render_fname(self, key: str) -> str:
        return self.fname_template.format(key=key)

    def get(self, key: str) -> Optional[Any]:
        fname = self._render_fname(key)

        try:
            with open(fname, "rb") as fd:
                return pickle.load(fd)
        except IOError:
            return None

    def set(self, key: str, value: Any):
        fname = self._render_fname(key)

        with open(fname, "w{}b".format("+" if self.create_if_not_exists else "")) as fd:
            pickle.dump(value, fd)

    def list_keys(self, pattern: str) -> List[str]:
        raise NotImplementedError("Listing keys is not supported")
