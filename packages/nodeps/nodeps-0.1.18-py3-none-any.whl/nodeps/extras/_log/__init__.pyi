__all__ = (
    "LOGGER_DEFAULT_FMT",
    "logger",
)

from loguru import Logger

loguru_logger: Logger | None

LOGGER_DEFAULT_FMT: str = ...


def logger(fmt: str = ...) -> Logger: ...
