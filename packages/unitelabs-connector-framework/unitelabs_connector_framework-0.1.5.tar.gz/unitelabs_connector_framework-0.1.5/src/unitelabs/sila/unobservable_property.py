from __future__ import annotations

import dataclasses
import inspect
import typing

import sila.server as sila

from . import utils
from .data_types import parser
from .defined_execution_error import DefinedExecutionError


@dataclasses.dataclass
class UnobservableProperty:
    identifier: str = ""
    display_name: str = ""
    description: str = ""
    errors: list[type[DefinedExecutionError]] = dataclasses.field(default_factory=list)

    def __call__(self, function: typing.Callable):
        setattr(function, "__handler", self)
        return function

    def attach(self, feature: sila.Feature, function: typing.Callable):
        name = function.__name__.lower().removeprefix("get_")
        display_name = self.display_name or utils.humanize(name)
        identifier = self.identifier or display_name.replace(" ", "")
        description = self.description or inspect.getdoc(function) or ""

        type_hint = inspect.signature(function).return_annotation

        unobservable_property = sila.UnobservableProperty(
            identifier=identifier,
            display_name=display_name,
            description=description,
            function=function,
            errors=[Error(feature=feature) for Error in self.errors],
            data_type=parser.parse(type_hint, feature),
        )
        feature.add_handler(unobservable_property)

        return unobservable_property
