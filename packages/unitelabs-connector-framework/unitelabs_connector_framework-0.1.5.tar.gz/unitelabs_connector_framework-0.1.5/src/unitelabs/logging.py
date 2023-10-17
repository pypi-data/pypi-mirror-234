from __future__ import annotations

import logging


def create_logger(name: str = __package__, level: logging._Level = logging.INFO) -> logging.Logger:
    """
    Get the app's logger and configure it if needed.
    """

    logger = logging.getLogger(name)
    handlers = [handler for handler in logger.handlers if not isinstance(handler, logging.NullHandler)]

    if not handlers:
        formatter = logging.Formatter("{asctime} [{levelname!s:<8}] {message!s}", style="{")

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        logger.setLevel(level)
        logger.addHandler(stream_handler)

    return logger
