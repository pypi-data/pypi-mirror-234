from urllib.parse import urlparse

import asyncpg
import psycopg2
import psycopg2.extensions
from prefect.blocks.core import Block
from pydantic.fields import Field
from pydantic.types import SecretStr


class Postgres(Block):
    """Postgres block which allows users to create postgres connections"""

    _block_type_name = "Postgres"
    _logo_url = "https://stprododpcmscdnendpoint.azureedge.net/assets/icons/postgres.png"  # type: ignore

    connection_string: SecretStr = Field(description="Database connection string")
    validate_connection: bool = Field(
        description="If true, connection will be validated when the block is initialized",
        default=True,
    )

    DEFAULT_PORT = 5432

    def block_initialization(self) -> None:
        parsed = urlparse(self.connection_string.get_secret_value())
        path_segments = parsed.path.strip("/").split("/")

        # Validate input

        if not parsed.hostname:
            raise ValueError("Missing database hostname")
        if not parsed.username:
            raise ValueError("Missing database username")
        if not parsed.password:
            raise ValueError("Missing database password")
        if len(path_segments) == 0:
            raise ValueError("Missing database name")
        if len(path_segments) > 1:
            raise ValueError(
                "A database connection string expects the path to be the database name, "
                "so can only have a single part/segment"
            )

        connection = self.create_connection()
        try:
            with connection.cursor() as cur:
                cur.execute("select 1;")
                cur.fetchall()
        finally:
            connection.close()

    async def create_async_connection(self) -> asyncpg.connection.Connection:
        return await asyncpg.connect(self.connection_string)

    def create_connection(self) -> psycopg2.extensions.connection:
        parsed = urlparse(self.connection_string.get_secret_value())

        db_host = parsed.hostname
        db_port = parsed.port or self.DEFAULT_PORT
        db_name = parsed.path.strip("/")
        db_user = parsed.username
        db_passwd = parsed.password

        return psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_passwd,
        )
