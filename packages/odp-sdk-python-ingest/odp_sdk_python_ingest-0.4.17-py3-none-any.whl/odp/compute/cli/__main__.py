import click
from dotenv import load_dotenv

from .authenticate import authenticate as _authenticate
from .block import block as _block
from .deploy import deploy as _deploy
from .parameters import parameters as _parameters
from .run import run as _run


@click.group()
def cli():
    pass


cli.add_command(_authenticate)
cli.add_command(_block)
cli.add_command(_deploy)
cli.add_command(_parameters)
cli.add_command(_run)

if __name__ == "__main__":
    load_dotenv()
    cli()
