from __future__ import annotations

import importlib
import importlib.util
import logging
import os

import click

from unitelabs import Connector, create_logger, utils


def default_app():
    """Compose"""
    src_dir = os.path.join(os.getcwd(), "src")
    package_name = next((entry.name for entry in os.scandir(src_dir) if entry.is_dir()), None)

    return f"{package_name}:create_app"


@click.group()
def connector() -> None:
    """Base cli"""


@connector.command()
@click.option(
    "--app",
    type=str,
    metavar="IMPORT",
    default=default_app,
    help="The application factory function to load, in the form 'module:name'.",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Increase the verbosity of to debug.",
)
@utils.coroutine
async def start(app, verbose: int):
    """Application Entrypoint"""
    log_level = logging.DEBUG if verbose > 0 else logging.INFO
    create_logger("sila", log_level)
    create_logger("unitelabs", log_level)

    app = await load_app(app)
    if app:
        await app.start()


async def load_app(location: str) -> Connector | None:
    """Dynamically import application factory"""
    module_name, _, factory_name = location.partition(":")

    try:
        module = importlib.import_module(module_name)
        factory = getattr(module, factory_name)
        app = await factory()

        return app
    except ImportError as exc:
        print(exc)
    except AttributeError as exc:
        print(exc)

    return None


if __name__ == "__main__":
    connector()
