import asyncio
import inspect
from functools import wraps
from tempfile import NamedTemporaryFile
from typing import Any, Awaitable, Callable, Coroutine, TypeVar, Union

import jinja2
import tiktoken
from jinja2 import meta
from pydub import AudioSegment  # type: ignore
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)
from typing_extensions import ParamSpec

from .typedefs import AudioFormat

P = ParamSpec("P")
T = TypeVar("T")
R = TypeVar("R")

TIKTOKEN_ENCODING_NAME = "cl100k_base"
RETRY_EXCEPTIONS = (asyncio.TimeoutError, ConnectionError, OSError, Exception)


def prompt(func: Callable[P, Union[T, Coroutine[T, Any, Any]]]):
    """Wrap a Python function into a Jinja2-templated prompt.

    :param func: The function to wrap.
    :return: The wrapped function.
    """

    @wraps(func)
    async def async_wrapper(*args: P.args, **kwargs: P.kwargs):
        """Wrapper function.

        :param args: Positional arguments to the function.
        :param kwargs: Keyword arguments to the function.
        :return: The Jinja2-templated docstring.
        :raises ValueError: If a variable in the docstring
                is not passed into the function.
        """
        assert func.__doc__ is not None, "Function must have a docstring"
        docstring = func.__doc__
        signature = inspect.signature(func)
        kwargs = signature.bind(*args, **kwargs).arguments  # type: ignore
        env = jinja2.Environment()
        parsed_content = env.parse(docstring)
        variables = meta.find_undeclared_variables(parsed_content)
        for var in variables:
            if var not in kwargs:
                raise ValueError(f"Variable '{var}' was not passed into the function")
        template = jinja2.Template(docstring, enable_async=True)
        return await template.render_async(**kwargs)

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs):
        """Wrapper function.

        :param args: Positional arguments to the function.
        :param kwargs: Keyword arguments to the function.
        :return: The Jinja2-templated docstring.
        :raises ValueError: If a variable in the docstring
                is not passed into the function.
        """
        assert func.__doc__ is not None, "Function must have a docstring"
        docstring = func.__doc__
        signature = inspect.signature(func)
        kwargs = signature.bind(*args, **kwargs).arguments  # type: ignore
        env = jinja2.Environment()
        parsed_content = env.parse(docstring)
        variables = meta.find_undeclared_variables(parsed_content)
        for var in variables:
            if var not in kwargs:
                raise ValueError(f"Variable '{var}' was not passed into the function")
        template = jinja2.Template(docstring)
        return template.render(**kwargs)

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return wrapper


def count_tokens(string: str, endcoding_name: str = TIKTOKEN_ENCODING_NAME) -> int:
    """Counts the number of tokens in a string."""
    encoding = tiktoken.get_encoding(endcoding_name)
    return len(encoding.encode(string))


def get_duration(audio: bytes, fmt: AudioFormat = "mp3") -> int:
    """Gets the duration of an audio file in milliseconds."""
    with NamedTemporaryFile("wb", suffix=f".{fmt}") as f:
        f.write(audio)
        f.flush()
        audio_: bytes = AudioSegment.from_file(f.name, fmt)  # type: ignore
        length_ms = len(audio_)  # type: ignore
        return length_ms * 1000


def exponential_backoff(
    retries: int = 10, wait: int = 1, max_wait: int = 60
) -> Callable[[Callable[P, Coroutine[T, Any, R]]], Callable[P, Coroutine[T, Any, R]]]:
    """Wrap an async function with exponential backoff."""

    def decorator(
        func: Callable[P, Coroutine[T, Any, R]]
    ) -> Callable[P, Coroutine[T, Any, R]]:
        @wraps(func)
        @retry(
            stop=stop_after_attempt(retries),
            wait=wait_exponential(multiplier=wait, max=max_wait),
            retry=retry_if_exception_type(RETRY_EXCEPTIONS),
            reraise=True,
        )
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            return await func(*args, **kwargs)  # type: ignore

        return wrapper

    return decorator
