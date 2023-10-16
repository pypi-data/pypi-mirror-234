from typing import Type

import click
from prefect.utilities.importtools import import_object


class TypeParamType(click.ParamType):
    name = "type"

    def convert(self, value: str, param: click.Parameter, ctx: click.Context) -> Type:
        if not isinstance(value, str):
            self.fail(f"'{value}' is not a valid import-path")

        try:
            return import_object(value)
        except (ValueError, ImportError) as e:
            self.fail(f"'{value}' is not a valid import-path. Err={e}")
