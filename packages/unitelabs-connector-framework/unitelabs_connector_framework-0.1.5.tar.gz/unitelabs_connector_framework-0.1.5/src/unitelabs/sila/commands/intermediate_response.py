import dataclasses
import inspect
import typing
import warnings

from .. import utils


@dataclasses.dataclass
class IntermediateResponse:
    name: str
    description: str = ""
    annotation: type = dataclasses.field(init=False, default=type(None))

    def __call__(self, function: typing.Callable) -> typing.Callable:
        intermediate_responses = getattr(function, "_i", [])

        index = len(intermediate_responses)

        signature = inspect.signature(function)
        if parameter := signature.parameters.get("intermediate", None):
            annotations = typing.get_args(parameter.annotation)
            self.annotation = annotations[len(annotations) - index - 1]

        if not self.description:
            docs = utils.parse_docs(inspect.getdoc(function) or "").get("yield", [])

            if index < len(docs):
                self.description = docs[len(docs) - index - 1].get("default")
            else:
                warnings.warn(
                    f"Found more Intermediate Response decorators than documented yields on function {function}"
                )

        setattr(function, "_i", [self, *intermediate_responses])
        return function
