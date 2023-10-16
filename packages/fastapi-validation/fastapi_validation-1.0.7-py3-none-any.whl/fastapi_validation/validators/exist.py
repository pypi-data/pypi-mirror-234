from inspect import isfunction
from typing import Any, Optional

from fastapi_exception import EntityNotFoundException
from fastapi_global_variable import GlobalVariable
from pydantic import ValidationInfo
from sqlalchemy import text

from ..constants.validator_constant import VALIDATOR_EXISTS
from ..types.custom_condition_type import CustomCondition
from .base import BaseValidator


class Exists(BaseValidator):
    __name__ = VALIDATOR_EXISTS

    def __init__(
        self,
        table,
        column: Any,
        case_insensitive: bool = False,
        customs: Optional[list[CustomCondition]] = [],
    ):
        self.table = table
        self.column = column
        self.case_insensitive = case_insensitive
        self.customs = customs

    def validate(self, *criterion):
        return GlobalVariable.get_or_fail('run_with_global_session')(
            lambda session: session.query(self.table).with_entities(self.table.id).filter(*criterion).first()
        )

    def __call__(self, values: Optional[Any] | list[Optional[Any]], info: ValidationInfo) -> Optional[Any]:
        if not values:
            return values

        is_list = isinstance(values, list)
        if not is_list:
            values = [values]

        for value in values:
            criterion = self.init_criterion(self.case_insensitive, self.table.__tablename__, self.column, value)
            self.build_custom_criterion(criterion, self.table.__tablename__, info.data, self.customs)

            if not self.validate(*criterion):
                raise EntityNotFoundException(self.table)

        return values if is_list else values[0]

    def init_criterion(self, case_insensitive: bool, table_name: str, column: str, value):
        if case_insensitive:
            return {text(f'"{table_name}".{column} ILIKE :value').bindparams(value=value)}

        return {text(f'"{table_name}".{column} = :value').bindparams(value=value)}

    def build_custom_criterion(
        self, criterion, table_name: str, values: dict[str, Any], customs: list[CustomCondition] = []
    ):  # noqa
        for custom in customs:
            custom['exclude'] = False if 'exclude' not in custom else custom.get('exclude')
            custom_column = custom['column']
            custom_value = custom.get('value')(values) if isfunction(custom.get('value')) else custom.get('value')

            sub_criterion = set()
            if custom['exclude']:
                if not custom_value or custom_value is None:
                    sub_criterion.add(text(f'"{table_name}.{custom_column} IS NOT NULL'))
                else:
                    sub_criterion.add(
                        text(f'"{table_name}".{custom_column} != :custom_value').bindparams(custom_value=custom_value)
                    )
            else:
                if not custom_value or custom_value is None:
                    sub_criterion.add(text(f'"{table_name}".{custom_column} IS NULL'))
                else:
                    sub_criterion.add(
                        text(f'"{table_name}".{custom_column} = :custom_value').bindparams(custom_value=custom_value)
                    )

            criterion.add(*sub_criterion)
