from dataclasses import Field, MISSING
from typing import Any, Dict


def remove_none_from_dict(obj: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in obj.items() if v is not None}


def get_default(field: Field, default=None) -> Any:
    if field.default_factory and field.default_factory != MISSING:
        return field.default_factory()
    if field.default and field.default != MISSING:
        return field.default
    return default
