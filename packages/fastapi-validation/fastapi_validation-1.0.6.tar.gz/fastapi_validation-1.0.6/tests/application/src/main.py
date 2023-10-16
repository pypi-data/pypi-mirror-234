from typing import Optional

from fastapi import FastAPI
from fastapi_exception import FastApiException
from fastapi_exception.config import GlobalVariable
from pydantic import BaseModel
from pydantic.types import UUID4

from fastapi_validation import Exists, FieldValidator, ModelValidator, PasswordValidation

from ..config.i18n import i18n_service

app = FastAPI(title="Test App")
GlobalVariable.set('app', app)

FastApiException.config(i18n_service)


class ChangePasswordDto(BaseModel):
    new_password: PasswordValidation


@app.post("/password")
def create_cars(dto: ChangePasswordDto):
    return True


def required_phone_number_and_code_pair(cls, values):
    phone_code, phone_number = values.phone_code, values.phone_number

    is_missing_only_phone_number = phone_code is not None and phone_number is None
    is_missing_only_phone_code = phone_number is not None and phone_code is None

    if is_missing_only_phone_number or is_missing_only_phone_code:
        raise ValueError()

    return values


class CheckPhoneTokenDto(BaseModel):
    phone_code: Optional[str] = None
    phone_number: Optional[str] = None

    _phone_number_and_code_validation = ModelValidator()(required_phone_number_and_code_pair)


@app.post("/phone")
def phone(dto: CheckPhoneTokenDto):
    return True


class ReportDto(BaseModel):
    post_id: UUID4

    _exist_post_id = FieldValidator('post_id')(Exists(table='PostEntity', column='id'))


@app.post("/report")
def report(dto: ReportDto):
    return True
