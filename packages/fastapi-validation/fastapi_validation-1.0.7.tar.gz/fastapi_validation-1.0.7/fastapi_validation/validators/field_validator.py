from typing import Any, Callable

from pydantic import field_validator
from pydantic.functional_validators import FieldValidatorModes


class FieldValidator:
    def __init__(
        self,
        field: str,
        mode: FieldValidatorModes = 'after',
        check_fields: bool | None = True,
    ):
        self.field = field
        self.mode = mode
        self.check_fields = check_fields

    def __call__(self, validator: Callable[..., Any]):
        return field_validator(__field=self.field, mode=self.mode, check_fields=self.check_fields)(validator)
