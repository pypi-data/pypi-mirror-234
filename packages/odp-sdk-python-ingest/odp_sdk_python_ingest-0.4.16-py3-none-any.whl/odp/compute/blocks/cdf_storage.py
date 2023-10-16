from typing import Any, Dict, List, Optional

from cognite.client import ClientConfig, CogniteClient, global_config
from cognite.client.credentials import OAuthClientCredentials
from prefect.blocks.core import Block
from pydantic import Field, SecretStr

# Disable pypi check
global_config.disable_pypi_version_check = True


class CdfStorage(Block):
    """CDF (Cognite Data Fusion) storage block to create OAuth connection configurations and a cognite client.

    Connection configurations are restricted to OAuth Client configurations. Refer:
    https://cognite-sdk-python.readthedocs-hosted.com/en/latest/cognite.html#cognite.client.config.ClientConfig
    to get the list of expected arguments.

    Examples:
        ```python
        from odp.compute.blocks.cdf_storage import CdfStorage

        cdf_storage_block = CdfStorage.load("block-name")
        ```
    """

    _block_type_name: str = "CDF Storage"
    _block_type_slug: str = "cdf_storage"
    _logo_url: str = "https://stprododpcmscdnendpoint.azureedge.net/assets/icons/cdf.png"

    base_url: str = Field(description="CDF cluster base url")
    cdf_project: str = Field(description="CDF project name")
    token_url: str = Field(description="OAuth token url")
    client_id: str = Field(description="Application client id")
    client_secret: SecretStr = Field(description="Application client secret")
    scopes: List[str] = Field(description="List of scopes")
    client_name: Optional[str] = Field(description="Cognite client name", default="odp_client")
    token_custom_args: Optional[Dict[str, Any]] = Field(
        description="Additional arguments to pass as query parameters to the token fetch request.", default={}
    )

    def get_connection_config(self) -> ClientConfig:
        """Get a OAuth client connection config using the user configurations.

        Args:
            None

        Returns:
            ClientConfig: Cognite client connection configurations.
        """
        # Instantiate OAuthClientCredentials & return a connection config.
        oauth_provider = OAuthClientCredentials(
            token_url=self.token_url,
            client_id=self.client_id,
            client_secret=self.client_secret.get_secret_value(),
            scopes=self.scopes,
            token_custom_args=self.token_custom_args,
        )
        return ClientConfig(
            client_name=self.client_name, base_url=self.base_url, project=self.cdf_project, credentials=oauth_provider
        )

    def get_cognite_client(self) -> CogniteClient:
        """Get a cognite client using the user configurations.

        Args:
            None

        Returns:
            CogniteClient: Cognite client.
        """
        # Get connection configurations
        client_config = self.get_connection_config()

        # Return a cognite client
        return CogniteClient(client_config)
