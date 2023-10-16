from typing import Any

from fastapi import Depends

from ..validators.query_list_integer_enum import validate_int_enum_query


def list_int_enum_query_param(values: Any, key: str):
    enum_values = list(map(int, values))

    return Depends(validate_int_enum_query(enum_values, key))
