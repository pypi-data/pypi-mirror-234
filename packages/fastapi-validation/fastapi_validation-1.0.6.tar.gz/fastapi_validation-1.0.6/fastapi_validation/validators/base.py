from abc import abstractmethod
from typing import Any, Optional


class BaseValidator:
    @abstractmethod
    def validate(self, value: Optional[Any], values: dict[str, Any], *criterion):
        pass
