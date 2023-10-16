from typing import Callable, Literal

from pydantic import model_validator


class ModelValidator:
    def __init__(self, mode: Literal['wrap', 'before', 'after'] = 'after'):
        self.mode = mode

    def __call__(self, validator: Callable):
        return model_validator(mode=self.mode)(validator)
