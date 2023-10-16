"""NoDeps Extras Log Module."""
__all__ = (
    "LOGGER_DEFAULT_FMT",
    "logger",
)

import copy
import sys

try:
    # nodeps[log] extras
    from loguru import logger as loguru_logger  # type: ignore[attr-defined]
except ModuleNotFoundError:
    loguru_logger = None

LOGGER_DEFAULT_FMT = (
    "<level>{level: <8}</level> <red>|</red> "
    "<cyan>{name}</cyan> <red>|</red> <red>|</red> "
    "<level>{message}</level>"
)


def logger(fmt=LOGGER_DEFAULT_FMT):
    """Returns a new logger.

    Examples:
        >>> from nodeps import logger
        >>>
        >>> l = logger("<level>{level: <8}</level> <red>|</red> "
        ...     "<cyan>{name}</cyan> <red>|</red> "
        ...     "<blue><level>{message}</level></blue><red>:</red> "
        ...     "<level>{extra[source]}</level> <red>-></red> "
        ...     "<level>{extra[destination]}</level>")
        >>> l.info("test", source="source", destination="destination")
    """
    if loguru_logger is None:
        msg = "loguru is not installed: installed with 'pip install nodeps[log]'"
        raise ImportError(msg)

    for item in loguru_logger._core.handlers:
        loguru_logger.remove(item)
    log = copy.deepcopy(loguru_logger)
    if fmt:
        log.configure(handlers=[{"sink": sys.stderr, "format": fmt}])
    return log
