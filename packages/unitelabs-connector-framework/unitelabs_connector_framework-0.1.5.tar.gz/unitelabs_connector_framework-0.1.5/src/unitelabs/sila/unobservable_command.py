from __future__ import annotations

import dataclasses
import inspect
import typing

import sila.server as sila

from . import utils
from .commands.response import Response
from .data_types import parser
from .defined_execution_error import DefinedExecutionError


@dataclasses.dataclass
class UnobservableCommand:
    identifier: str = ""
    display_name: str = ""
    description: str = ""
    errors: list[type[DefinedExecutionError]] = dataclasses.field(default_factory=list)

    def __call__(self, function: typing.Callable):
        setattr(function, "__handler", self)
        return function

    def attach(self, feature: sila.Feature, function: typing.Callable):
        docs = inspect.getdoc(function) or ""
        docs = utils.parse_docs(inspect.getdoc(function) or "")

        display_name = self.display_name or utils.humanize(function.__name__)
        identifier = self.identifier or str(display_name).replace(" ", "")
        description = self.description or docs.get("default", "")

        parameters = self._infer_parameters_from_signature(feature, function)
        parameter_by_identifier = {parameter.identifier: key for key, parameter in parameters.items()}

        _responses: list[Response] = getattr(function, "_r", [])
        responses = [
            sila.data_types.Structure.Element(
                identifier=responses.name.replace(" ", ""),
                display_name=responses.name,
                description=responses.description,
                data_type=parser.parse(responses.annotation, feature),
            )
            for responses in _responses
        ]

        async def wrapper(**kwargs):
            response = function(**{parameter_by_identifier[key]: value for key, value in kwargs.items()})
            if inspect.isawaitable(response):
                response = await response

            if isinstance(response, type(None)):
                return {}
            values = {}
            for index, response in enumerate([response] if not isinstance(response, tuple) else response):
                key = responses[index]
                values[key.identifier] = response

            return values

        unobservable_command = sila.UnobservableCommand(
            identifier=identifier,
            display_name=display_name,
            description=description,
            function=wrapper,
            errors=[Error(feature=feature) for Error in self.errors],
            parameters=sila.data_types.Structure(elements=list(parameters.values())),
            responses=sila.data_types.Structure(elements=responses),
        )
        feature.add_handler(unobservable_command)

        return unobservable_command

    def _infer_parameters_from_signature(
        self, feature, function: typing.Callable
    ) -> dict[str, sila.data_types.Structure.Element]:
        signature = inspect.signature(function)
        docs = utils.parse_docs(inspect.getdoc(function) or "").get("parameter", [])

        parameters: dict[str, sila.data_types.Structure.Element] = {}
        i = 0
        for name, parameter in signature.parameters.items():
            if parameter.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD and name not in ["self", "cls"]:
                doc = docs[i] if len(docs) > i else {}
                i += 1

                display_name = doc.get("display_name", utils.humanize(parameter.name))
                parameters[name] = sila.data_types.Structure.Element(
                    identifier=doc.get("identifier", display_name.replace(" ", "")),
                    display_name=display_name,
                    description=doc.get("default", ""),
                    data_type=parser.parse(parameter.annotation, feature),
                )

        return parameters
