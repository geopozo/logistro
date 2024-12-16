import inspect
import json
import logging
import time

import logistro.args as args

## New Constants and Globals

DEBUG2 = 5

logging.addLevelName(DEBUG2, "DEBUG2")
human_formatter = logging.Formatter("%(asctime)s - %(message)s")
structured_formatter = logging.Formatter("%(message)s")

## Set Defaults

logger = logging.getLogger(__name__)
logger.info(f"Default logger with name: {__name__}")

default_handler = logging.StreamHandler()
logger.addHandler(default_handler)


def set_human():
    default_handler.setFormatter(human_formatter)


def set_structured():
    default_handler.setFormatter(structured_formatter)


if args.parsed.human:
    set_human()
else:
    set_structured()

# Avoid the log from the ancestor's logger
# Why?
# logger.propagate = False


# Improve the name of the log
def _get_context_info():
    # currentframe() is this function
    # once back is _log_message (a helper function)
    # and back again is the logging function the dev calls
    logistro_log_fn = inspect.currentframe().f_back.f_back

    # python module = python file
    calling_frame = logistro_log_fn.f_back  # calling frame
    module_obj = inspect.getmodule(calling_frame)  # calling module
    calling_package = module_obj.__package__  # calling package
    calling_file = module_obj.__name__  # literally file path

    # The function where logistro is used
    calling_function = (
        calling_frame.f_code.co_name if hasattr(calling_frame, "f_code") else None
    )
    return calling_package, calling_file, calling_function


# This verify the strings of the tags
def _verify_tags(logistro_tags, tags, process):
    # Check None values
    if not logistro_tags:
        return False
    elif logistro_tags and not tags:
        return True

    # Transform lists to sets
    arg_tags = set(logistro_tags)
    user_tags = set(tags)

    # Check tags
    if process == "include":
        return arg_tags.isdisjoint(user_tags)
    if process == "exclude":
        return not arg_tags.isdisjoint(user_tags)


# This print the structured format
def _print_structured(message, tags, level, package, file, module_function):
    log = {
        "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "level": level,
        "package": package,
        "file": file,
        "module_function": module_function,
        "message": message,
        "tags": tags,
    }
    levels = {
        "CRITICAL": 50,
        "ERROR": 40,
        "EXCEPTION": 40,
        "WARNING": 30,
        "INFO": 20,
        "DEBUG1": 10,
        "DEBUG2": 5,
    }
    logger.log(levels[level], json.dumps(log, indent=4))


# Generalized wrap functions
def _log_message(level_func, message, tags=None, *args, **kwargs):
    if _verify_tags(args.parsed.included_tags, tags, "include") or _verify_tags(
        args.parsed.excluded_tags,
        tags,
        "exclude",
    ):
        return

    level, package, file, module_function = _get_context_info()
    if not args.parsed.human:
        _print_structured(message, tags, level, package, file, module_function)
        return

    tags = f" ({tags})" if tags else ""
    logistro_log = (
        f"{level} - {package}:{file}:{module_function}(): {message}{tags}"
        if module_function
        else f"{level} - {package}:{file}: {message}{tags}"
    )
    if level == "DEBUG2":
        logger.log(DEBUG2, logistro_log, *args, **kwargs)
    else:
        level_func(logistro_log, *args, **kwargs)


# Custom debug with custom level
def debug2(message, tags=None, *args, **kwargs):
    _log_message(None, message, tags, *args, **kwargs)


# Wrap function
def debug1(message, tags=None, *args, **kwargs):
    _log_message(logger.debug, message, tags, *args, **kwargs)


# Wrap function
def info(message, tags=None, *args, **kwargs):
    _log_message(logger.info, message, tags, *args, **kwargs)


# Wrap function
def warning(message, tags=None, *args, **kwargs):
    _log_message(logger.warning, message, tags, *args, **kwargs)


# Wrap function
def exception(message, tags=None, *args, **kwargs):
    _log_message(logger.exception, message, tags, *args, **kwargs)


# Wrap function
def error(message, tags=None, *args, **kwargs):
    _log_message(logger.error, message, tags, *args, **kwargs)


# Wrap function
def critical(message, tags=None, *args, **kwargs):
    _log_message(logger.critical, message, tags, *args, **kwargs)
