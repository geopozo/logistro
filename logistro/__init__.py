# the forbidden import
from logging import *  # noqa

from .custom_logging import betterConfig
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
    betterConfig,  # config function
    set_human,  # config function
    set_structured,  # config function
    logger,  # default/root logger
    DEBUG2,  # level
    debug1,  # helper
    debug2,  # helper
    info,  # helper
    warning,  # helper
    exception,  # helper
    error,  # helper
    critical,  # helper
]
