# we are a shim for logging, so do it
from logging import *  # noqa

from .custom_logging import critical
from .custom_logging import debug1
from .custom_logging import DEBUG2
from .custom_logging import debug2
from .custom_logging import error
from .custom_logging import exception
from .custom_logging import info
from .custom_logging import logger
from .custom_logging import set_human
from .custom_logging import set_structured
from .custom_logging import warning

__all__ = [
    "DEBUG2",
    "set_human",
    "set_structured",
    "logger",
    "debug1",
    "debug2",
    "info",
    "warning",
    "exception",
    "error",
    "critical",
]
