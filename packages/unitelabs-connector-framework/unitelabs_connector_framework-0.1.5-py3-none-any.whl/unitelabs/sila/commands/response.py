import dataclasses
import inspect
import typing
import warnings

from .. import utils


@dataclasses.dataclass
class Response:
    name: str
    description: str = ""
    annotation: type = dataclasses.field(init=False, default=type(None))

    def __call__(self, function: typing.Callable) -> typing.Callable:
        responses = getattr(function, "_r", [])

        index = len(responses)

        signature = inspect.signature(function)
        annotation = signature.return_annotation

        annotations: typing.Iterable[type] = []
        if annotation is not None:
            annotation = (
                annotation if issubclass(typing.get_origin(annotation) or annotation, tuple) else tuple[annotation]
            )
            annotations = typing.get_args(annotation)

        if index < len(annotations):
            self.annotation = annotations[len(annotations) - index - 1]
        else:
            warnings.warn(f"Found more Response decorators than annotated returns on function {function}")

        if not self.description:
            docs = utils.parse_docs(inspect.getdoc(function) or "").get("return", [])

            if index < len(docs):
                self.description = docs[len(docs) - index - 1].get("default")
            else:
                warnings.warn(f"Found more Response decorators than documented returns on function {function}")

        setattr(function, "_r", [self, *responses])
        return function
