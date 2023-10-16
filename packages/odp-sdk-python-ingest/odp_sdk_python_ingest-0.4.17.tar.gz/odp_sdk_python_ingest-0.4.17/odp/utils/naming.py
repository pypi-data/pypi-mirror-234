import os

import inflection


def __get_formatter_cb(convention: str):
    convention = convention or os.getenv("USE_NAMING_CONVENTION") or "snake_case"

    if convention == "camelCase":
        return lambda x: inflection.camelize(x, False)
    elif convention == "CamelCase":
        return lambda x: inflection.camelize(x, True)
    elif convention == "snake_case":
        return inflection.underscore
    else:
        raise RuntimeError("Unvalid naming convention: '{}'".format(convention))


def format_name(x: str, convention: str = None):
    cb = __get_formatter_cb(convention)
    return cb(x)
