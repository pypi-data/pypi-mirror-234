import click

from odp.auth.prefect import PrefectB2cClient

__all__ = ["authenticate"]


@click.command(help="Test authentication")
@click.option("--api-server", type=str, required=False, help="Prefect API url")
def authenticate(api_server: str):
    client = PrefectB2cClient(api_server=api_server)
    token = client.get_auth_token()

    click.echo("Authenticated with prefect using token '{}...{}'".format(token[:4], token[-4:]))
