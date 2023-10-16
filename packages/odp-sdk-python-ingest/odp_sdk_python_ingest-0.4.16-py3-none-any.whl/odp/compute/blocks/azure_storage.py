from typing import Optional, Tuple, Union, cast

from azure.storage.blob import BlobClient, BlobProperties, ContainerClient
from prefect.blocks.core import Block
from pydantic.fields import Field
from pydantic.types import SecretStr


class AzureStorage(Block):
    """Azure storage block which allows users to create container and blob clients.

    Support multiple argument combination:
    - `account_url` and `container_name`
    - `connection_string` and `container_name`
    - `container_url`

    In addition, `sas_token` or `access_key` can be set, but this is optional.

    See [Azure Docs]
    (https://learn.microsoft.com/en-us/python/api/azure-storage-blob/azure.storage.blob.containerclient?view=azure-python)
    for more details.
    """

    _block_type_name = "Azure Storage"
    _logo_url = "https://stprododpcmscdnendpoint.azureedge.net/assets/icons/azure-storage.png"  # type: ignore

    account_url: Optional[str] = Field(
        description="Storage account URI",
    )

    container_name: Optional[str] = Field(description="Azure storage container name")

    connection_string: Optional[SecretStr] = Field(
        description="Storage account connection string",
    )

    container_url: Optional[SecretStr] = Field(
        description="Full endpoint URL to container, including SAS token if used.",
    )

    sas_token: Optional[SecretStr] = Field(description="Shared access token")

    acces_key: Optional[SecretStr] = Field(
        description="Storage account access key",
    )

    assert_exists: bool = Field(
        description="If true, the block initialization will check whether the container exists, "
        "and raise and assertion error if it doesn't",
        default=True,
    )

    def block_initialization(self) -> None:
        """Validate the container setup"""
        try:
            client = self.container_client()
        except ValueError as e:
            raise AssertionError("Failed to validate container client") from e

        if self.assert_exists and not client.exists():
            raise AssertionError("The container '{}' does not exist".format(client.container_name))

    def container_client(self) -> ContainerClient:
        """Create a container client based on secrets stored within

        Returns:
            New `ContainerClient` based on secrets within

        Raises:
            ValueError: Not enough arguments set for the container client
        """

        credential: Optional[str] = None

        if self.sas_token:
            credential = self.sas_token.get_secret_value()
        elif self.acces_key:
            credential = self.acces_key.get_secret_value()

        if self.account_url and self.container_name:
            return ContainerClient(
                account_url=self.account_url,
                container_name=self.container_name,
                credential=credential,
            )

        if self.connection_string and self.container_name:
            return ContainerClient.from_connection_string(
                conn_str=self.connection_string.get_secret_value(),
                container_name=self.container_name,
                credential=credential,
            )

        if self.container_url:
            return ContainerClient.from_container_url(
                container_url=self.container_url.get_secret_value(),
                credential=credential,
            )

        raise ValueError("Not enough arguments set for the container client")

    def blob_client(
        self,
        blob: Optional[Union[str, BlobProperties]] = None,
        snapshot: Optional[str] = None,
        connection_string: Optional[str] = None,
        blob_url: Optional[str] = None,
    ) -> BlobClient:
        """Createa a blob client based on secrets stored within

        Args:
            blob: Blob name or `BlobProperties`-object. Blob does not need to exist
            snapshot: Blob snapshot
            connection_string: Storage account connection string
            blob_url: Full endpoint to the Blob, including sas_token and snapshot if used

        Returns:
            `BlobClient` for `blob`. The blob does not have to exist.

        Raises:
            ValueError: Not enough arguments set for the blob client or the blob name
                        could not be obtained from the `BlobProperties`-object
        """

        if self.account_url and self.container_name and blob:
            blob, snapshot = self._resolve_blob_name_and_snapshot(blob, snapshot)

        if not connection_string and self.connection_string:
            connection_string = self.connection_string.get_secret_value()

        if connection_string and self.container_name and blob:
            blob, snapshot = self._resolve_blob_name_and_snapshot(blob, snapshot)

            return BlobClient.from_connection_string(
                conn_str=connection_string,
                container_name=self.container_name,
                blob_name=cast(str, blob),
                snapshot=snapshot,
            )

        if blob_url:
            return BlobClient.from_blob_url(blob_url=blob_url, credential=self._get_credential(), snapshot=snapshot)

        if blob:
            container_client = self.container_client()
            return container_client.get_blob_client(blob)

        raise ValueError("Not enough arguments set for the blob client")

    def _get_credential(self) -> Optional[str]:
        if self.sas_token:
            return self.sas_token.get_secret_value()
        elif self.acces_key:
            return self.acces_key.get_secret_value()

        return None

    def _resolve_blob_name_and_snapshot(
        self, blob: Union[str, BlobProperties], snapshot: Optional[str]
    ) -> Tuple[str, Optional[str]]:
        if isinstance(blob, str):
            return blob, snapshot

        snapshot = snapshot or blob.snapshot
        blob_name = blob.name

        if not blob_name:
            raise ValueError("Blob name not set in BlobProperties-object")

        return blob_name, snapshot
