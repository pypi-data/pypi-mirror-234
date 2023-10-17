from importlib.metadata import version

from .config import Config
from .connector import Connector
from .logging import create_logger

__version__ = version("unitelabs_connector_framework")
__all__ = ["__version__", "Connector", "Config", "create_logger"]
