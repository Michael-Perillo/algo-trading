from enum import Enum

from pydantic import BaseModel


def model_fields_enum(model_cls: type[BaseModel]) -> Enum:
    # Support both class and instance input
    enum_name = (
        f'{model_cls.__name__}Field'
        if hasattr(model_cls, '__name__')
        else f'{model_cls.__class__.__name__}Field'
    )
    return Enum(enum_name, {name: name for name in model_cls.__fields__})
