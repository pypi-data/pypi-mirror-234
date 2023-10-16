from fastapi import Query
from fastapi_exception import throw_validation


def parse_integer_values(values: list[str]):
    parsed_values = []
    for value in values:
        value = value.strip()
        if value.isnumeric():
            parsed_values.append(int(value))
    return parsed_values


def validate_query_integer_values(enum_values: list[int], query_values: list[str], key: str):
    parsed_values = parse_integer_values(query_values)

    is_invalid_type = len(query_values) != len(parsed_values)
    is_not_include_type = not set(parsed_values).issubset(set(enum_values))

    if is_invalid_type or is_not_include_type:
        throw_validation(type='enum_query.invalid', loc=('query', 'key'))

    return parsed_values


def validate_int_enum_query(enum_values: list[int], key: str):
    def validator(value=Query(default=None, alias=key)):
        if value is None:
            return None

        value_list = value.split(',')
        return validate_query_integer_values(enum_values, value_list, key)

    return validator
