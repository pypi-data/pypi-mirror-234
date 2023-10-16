from datetime import timedelta
from typing import Dict, List, Optional

from cognite.experimental import CogniteClient

__all__ = ["FederatedCogniteClient"]

from .cdf_token_handler import CdfTokenHandler


class FederatedCogniteClient(CogniteClient):
    """CogniteClient wrapper which handles federated Azure B2C tokens"""

    def __init__(
        self,
        api_key: str = None,
        project: str = None,
        client_name: str = None,
        base_url: str = None,
        max_workers: int = None,
        headers: Dict[str, str] = None,
        timeout: int = None,
        disable_pypi_version_check: Optional[bool] = None,
        debug: bool = False,
        server=None,
        token_client_id: Optional[str] = None,
        token_username: Optional[str] = None,
        token_password: Optional[str] = None,
        token_scopes: Optional[List[str]] = None,
        login_url: Optional[str] = None,
        token_expiry_leeway: Optional[timedelta] = None,
        **kwargs,
    ):
        token_handler = CdfTokenHandler(
            client_id=token_client_id,
            username=token_username,
            password=token_password,
            cdf_cluster=server,
            scopes=token_scopes,
            login_url=login_url,
            token_expiry_leeway=token_expiry_leeway,
        )

        super().__init__(
            api_key=api_key,
            project=project,
            client_name=client_name,
            base_url=base_url,
            max_workers=max_workers,
            headers=headers,
            timeout=timeout,
            disable_pypi_version_check=disable_pypi_version_check,
            debug=debug,
            server=token_handler.cluster,
            token=token_handler,
            **kwargs,
        )
