from typing import Any, Optional

from fastapi_exception import ValidationErrorDetail


class InvalidValueError(ValidationErrorDetail):
    error_type = 'invalid_value_error'

    def __init__(
        self,
        property: str,
        loc: tuple[int | str, ...],
        ctx: Optional[dict[str, dict[str, Any]]] = {},
        input: dict[str, Any] = {},
    ):
        ctx = ctx or {'property': property}
        super().__init__(self.error_type, loc, '', input, ctx)
