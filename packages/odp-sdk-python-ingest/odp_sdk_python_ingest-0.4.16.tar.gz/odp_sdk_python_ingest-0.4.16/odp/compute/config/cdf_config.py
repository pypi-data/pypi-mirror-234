from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Union

__all__ = ["CdfConfig"]


@dataclass
class CdfConfig:
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
    server = None
