from typing import TypedDict, Callable

from typing_extensions import NotRequired

ColumnType = int | str | None


class CustomCondition(TypedDict):
    column: str
    value: ColumnType | Callable
    exclude: NotRequired[bool]
