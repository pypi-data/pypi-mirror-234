from typing import *
from uuid import uuid4

from jinja2 import Template
from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module

Vector: TypeAlias = List[float]


class TemplateModel(BaseModel):
    """
    ID: {{ id }}
	You are a helpful assistant.
    """
    id: str = Field(default_factory=lambda: str(uuid4()))

    @property
    def prompt(self) -> str:
        assert isinstance(self.__doc__, str), f"{self.__class__.__name__}.__doc__ must be a string."
        return Template(self.__doc__).render(**self.dict())

    def __str__(self) -> str:
        return self.prompt

    def __repr__(self) -> str:
        return self.prompt
