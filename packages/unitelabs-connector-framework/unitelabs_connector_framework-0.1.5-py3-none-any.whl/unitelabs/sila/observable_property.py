from __future__ import annotations

import dataclasses
import inspect
import typing
from collections.abc import AsyncIterator

import sila.server as sila

from . import utils
from .data_types import parser
from .defined_execution_error import DefinedExecutionError

T = typing.TypeVar("T")
Stream = AsyncIterator[T]


@dataclasses.dataclass
class ObservableProperty:
    identifier: str = ""
    display_name: str = ""
    description: str = ""
    errors: list[type[DefinedExecutionError]] = dataclasses.field(default_factory=list)

    def __call__(self, function: typing.Callable):
        setattr(function, "__handler", self)
        return function

    def attach(self, feature: sila.Feature, function: typing.Callable):
        name = function.__name__.lower().removeprefix("subscribe_")
        display_name = self.display_name or utils.humanize(name)
        identifier = self.identifier or display_name.replace(" ", "")
        description = self.description or inspect.getdoc(function) or ""

        type_hint = inspect.signature(function).return_annotation
        type_hint = typing.get_args(type_hint)[0]

        observable_property = sila.ObservableProperty(
            identifier=identifier,
            display_name=display_name,
            description=description,
            function=function,
            errors=[Error(feature=feature) for Error in self.errors],
            data_type=parser.parse(type_hint, feature),
        )
        feature.add_handler(observable_property)

        return observable_property
