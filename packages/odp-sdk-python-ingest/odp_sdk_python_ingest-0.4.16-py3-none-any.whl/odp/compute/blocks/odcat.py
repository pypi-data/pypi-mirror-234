from .aad_client_credentials import AadClientCredentials


class OdCat(AadClientCredentials):
    """Authenticate with the ODCAT API using Azure Active Directory (AAD) client credentials."""

    _block_type_name = "Azure AD Client Credentials"
    _logo_url = "https://stprododpcmscdnendpoint.azureedge.net/assets/ocat/odcat%20icon.png"  # type: ignore
