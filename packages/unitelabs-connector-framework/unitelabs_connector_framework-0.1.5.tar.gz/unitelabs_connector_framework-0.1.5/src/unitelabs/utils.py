import asyncio
import functools
import typing


def coroutine(function: typing.Callable) -> typing.Callable:
    """Wraps click cli commands to run asynchronously."""

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        return asyncio.run(function(*args, **kwargs))

    return wrapper
