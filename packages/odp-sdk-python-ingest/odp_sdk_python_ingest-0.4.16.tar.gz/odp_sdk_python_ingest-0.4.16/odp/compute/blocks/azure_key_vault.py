import re

from azure.identity import ClientSecretCredential
from azure.keyvault.keys import KeyClient
from azure.keyvault.secrets import SecretClient
from prefect.blocks.core import Block
from pydantic import AnyHttpUrl

from odp.compute.blocks.aad_client_credentials import AadClientCredentials


class AzureKeyVault(Block):
    """Azure Key Vault block that allows users to retrieve secrets from an Azure Key Vault."""

    _block_type_name = "Azure Key Vault"
    _logo_url = "https://stprododpcmscdnendpoint.azureedge.net/assets/icons/azure-storage.png"  # type: ignore

    aad_client_credentials: AadClientCredentials
    key_vault_url: AnyHttpUrl

    def get_key(self, key_name: str):
        """Return key from Azure Key Vault."""
        try:
            tenant_id = re.search(
                "https://login.microsoftonline.com/(.+?)/oauth2/v2.0/token", self.aad_client_credentials.token_url
            ).group(1)
        except AttributeError:
            raise ValueError("Invalid token URL for the AadClientCredentials Block.")
        azure_creds = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=self.aad_client_credentials.client_id.get_secret_value(),
            client_secret=self.aad_client_credentials.client_secret.get_secret_value(),
        )
        client = KeyClient(self.key_vault_url, azure_creds)
        return client.get_key(key_name)

    def get_secret(self, secret_name: str):
        """Return secret from Azure Key Vault."""
        try:
            tenant_id = re.search(
                "https://login.microsoftonline.com/(.+?)/oauth2/v2.0/token", self.aad_client_credentials.token_url
            ).group(1)
        except AttributeError:
            raise ValueError("Invalid token URL for the AadClientCredentials Block.")
        azure_creds = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=self.aad_client_credentials.client_id.get_secret_value(),
            client_secret=self.aad_client_credentials.client_secret.get_secret_value(),
        )
        client = SecretClient(self.key_vault_url, azure_creds)
        return client.get_secret(secret_name)
