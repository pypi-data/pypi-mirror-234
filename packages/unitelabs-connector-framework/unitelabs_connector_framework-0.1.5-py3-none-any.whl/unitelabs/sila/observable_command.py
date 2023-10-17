from __future__ import annotations

import dataclasses
import inspect
import typing

import sila.server as sila
from sila.commands import CommandExecution

from . import utils
from .commands.intermediate import Intermediate
from .commands.intermediate_response import IntermediateResponse
from .commands.response import Response
from .commands.status import Status
from .data_types import parser
from .defined_execution_error import DefinedExecutionError


@dataclasses.dataclass
class ObservableCommand:
    name: str = ""
    description: str = ""
    errors: list[type[DefinedExecutionError]] = dataclasses.field(default_factory=list)

    def __call__(self, function: typing.Callable):
        setattr(function, "__handler", self)
        return function

    def attach(self, feature: sila.Feature, function: typing.Callable):
        docs = inspect.getdoc(function) or ""
        docs = utils.parse_docs(inspect.getdoc(function) or "")

        display_name = self.name or utils.humanize(function.__name__)
        identifier = display_name.replace(" ", "")
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

        _intermediate_responses: list[IntermediateResponse] = getattr(function, "_i", [])
        intermediate_responses = [
            sila.data_types.Structure.Element(
                identifier=intermediate_response.name.replace(" ", ""),
                display_name=intermediate_response.name,
                description=intermediate_response.description,
                data_type=parser.parse(intermediate_response.annotation, feature),
            )
            for intermediate_response in _intermediate_responses
        ]

        async def wrapper(command_execution: CommandExecution, **kwargs):
            args: dict = {
                "status": Status(command_execution=command_execution),
            }
            if len(intermediate_responses):
                args["intermediate"] = Intermediate(command_execution=command_execution)

            response = function(
                **{parameter_by_identifier[key]: value for key, value in kwargs.items()},
                **args,
            )
            if inspect.isawaitable(response):
                response = await response

            if isinstance(response, type(None)):
                return {}
            values = {}
            for index, response in enumerate([response] if not isinstance(response, tuple) else response):
                key = responses[index]
                values[key.identifier] = response

            return values

        observable_command = sila.ObservableCommand(
            identifier=identifier,
            display_name=display_name,
            description=description,
            function=wrapper,
            errors=[Error(feature=feature) for Error in self.errors],
            parameters=sila.data_types.Structure(elements=list(parameters.values())),
            responses=sila.data_types.Structure(elements=responses),
            intermediate_responses=sila.data_types.Structure(elements=intermediate_responses),
        )
        feature.add_handler(observable_command)

        return observable_command

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
