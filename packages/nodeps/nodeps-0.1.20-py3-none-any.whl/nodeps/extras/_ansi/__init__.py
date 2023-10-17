"""NoDeps Extras Ansi Module."""
__all__ = (
    "getstdout",
    "strip",
)

import contextlib
import io
from collections.abc import Callable, Iterable
from typing import Any

try:
    # nodeps[ansi] extras
    import strip_ansi  # type: ignore[attr-defined]
except ModuleNotFoundError:
    strip_ansi = None


def getstdout(func: Callable, *args: Any, ansi: bool = False, new: bool = True, **kwargs: Any) -> str | Iterable[str]:
    """Redirect stdout for func output and remove ansi and/or new line.

    Args:
        func: callable.
        *args: args to callable.
        ansi: strip ansi.
        new: strip new line.
        **kwargs: kwargs to callable.

    Returns:
        str | Iterable[str, str]:
    """
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        func(*args, **kwargs)
    return strip(buffer.getvalue(), ansi=ansi, new=new) if ansi or new else buffer.getvalue()


def strip(obj: str | Iterable[str], ansi: bool = False, new: bool = True) -> str | Iterable[str]:
    r"""Strips ``\n`` And/Or Ansi from string or Iterable.

    Args:
        obj: object or None for redirect stdout
        ansi: ansi (default: False)
        new: newline (default: True)

    Returns:
        Same type with NEWLINE removed.
    """

    def rv(x):
        if isinstance(x, str):
            x = x.removesuffix("\n") if new else x
            x = strip_ansi.strip_ansi(x) if ansi else x
        if isinstance(x, bytes):
            x = x.removesuffix(b"\n") if new else x
        return x

    if strip_ansi is None:
        msg = "strip_ansi is not installed: installed with 'pip install nodeps[ansi]'"
        raise ImportError(msg)

    cls = type(obj)
    if isinstance(obj, str):
        return rv(obj)
    return cls(rv(i) for i in obj)
