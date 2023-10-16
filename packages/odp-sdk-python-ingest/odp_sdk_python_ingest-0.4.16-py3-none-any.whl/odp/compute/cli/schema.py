import inspect
from dataclasses import dataclass
from typing import Type


def arguments_to_dataclass(cls: Type) -> Type:
    signature = inspect.signature(cls.__init__)

    annotations = {}
    annotations_with_defaults = {}
    properties = {}

    for param in signature.parameters.values():
        if param.name in ("self", "kwargs", "args"):
            continue

        if param.annotation is not param.empty:
            if param.default is not param.empty:
                annotations_with_defaults[param.name] = param.annotation
            else:
                annotations[param.name] = param.annotation

        if param.default is not param.empty:
            properties[param.name] = param.default

        print(param.name, " | ", param.annotation, " | ", param.default)

    cls = type(
        cls.__name__ + "Schema",
        (object,),
        {
            "__annotations__": dict(**annotations, **annotations_with_defaults),
            **properties,
        },
    )

    return dataclass(cls)
