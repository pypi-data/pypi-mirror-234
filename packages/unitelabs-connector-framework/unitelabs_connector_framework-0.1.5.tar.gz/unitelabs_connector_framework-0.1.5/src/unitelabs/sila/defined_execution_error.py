from __future__ import annotations

import dataclasses
import inspect

import sila.server as sila

from . import utils


@dataclasses.dataclass
class DefinedExecutionError(sila.errors.DefinedExecutionError):
    def __init__(self, *args, identifier: str = "", display_name: str = "", description: str = "", **kwargs):
        display_name = display_name or utils.to_display_name(self.__class__.__name__)
        identifier = identifier or display_name.replace(" ", "")
        description = description or inspect.getdoc(self) or ""

        super().__init__(*args, identifier=identifier, display_name=display_name, description=description, **kwargs)
