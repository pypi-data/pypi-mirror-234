import re

from fastapi_exception import MissingError, throw_validation_with_exception

from fastapi_validation.custom_errors.value_error import InvalidValueError

PASSWORD_REGEX = r'^(?=.*[A-Z])(?=.*\d)\S{6,}$'


class PasswordValidation(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __get_pydanctic_json_schema__(cls, field_schema):
        field_schema.update(
            pattern=PASSWORD_REGEX,
            examples=['Secret@1234'],
        )

    @classmethod
    def validate(cls, value, values):
        if not isinstance(value, str) or not value:
            throw_validation_with_exception(MissingError(('body', 'password')))

        if not re.search(PASSWORD_REGEX, value):
            throw_validation_with_exception(InvalidValueError('password', ('body', 'password')))

        return cls(value)

    def __repr__(self):
        return f'PasswordValidation({super().__repr__()})'
