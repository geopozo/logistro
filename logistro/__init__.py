from logging import * #noqa

from .custom_logging import (
    DEBUG2,
    customize_parser,
    customize_pytest_addoption,
    logger,
    debug1,
    debug2,
    info,
    warning,
    exception,
    error,
    critical,
)

__all__ = [
    "DEBUG2",
    "customize_parser",
    "customize_pytest_addoption",
    "logger",
    "debug1",
    "debug2",
    "info",
    "warning",
    "exception",
    "error",
    "critical",
]
