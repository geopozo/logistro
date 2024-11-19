import sys
import json
import time
import logging
import inspect
import argparse


# new constant
DEBUG2 = 5

# Create the logging
basicConfig = logging.basicConfig
logging.addLevelName(DEBUG2, "DEBUG2")

# Set logger
logger = logging.getLogger(__name__)

# Create handler
handler = logging.StreamHandler(stream=sys.stderr)


# Customize parser
def customize_parser(add_help=True):
    parser_logging = argparse.ArgumentParser(add_help=add_help)
    parser_logging.add_argument(
        "--human",
        action="store_true",
        dest="human",
        default=True,
        help="Format the logs for humans",
    )
    parser_logging.add_argument(
        "--structured",
        action="store_false",
        dest="human",
        help="Format the logs as JSON",
    )
    return parser_logging


# parser
parser_logging = customize_parser()

# Get the Format
try:
    arg_logging, unknow_args = parser_logging.parse_known_intermixed_args(sys.argv)
    if unknow_args:
        logging.warning(f"Verify the arguments {unknow_args}")
except SystemExit as e:
    raise SystemExit(f"Verify the arguments {e}")

# Create Formatter
if arg_logging.human:
    formatter = logging.Formatter("%(asctime)s - %(message)s")  # TODO

# Customize logger
if arg_logging.human:
    handler.setFormatter(formatter)
logger.addHandler(handler)

# Avoid the log from the ancestor's logger
logger.propagate = False


# Improve the name
def _get_name():
    level = inspect.currentframe().f_back.f_back.f_code.co_name
    upper_frame = inspect.currentframe().f_back.f_back.f_back
    module_frame = inspect.getmodule(upper_frame) or inspect.getmodule(
        upper_frame.f_back
    )
    package = module_frame.__package__
    file = module_frame.__name__
    module_function = (
        upper_frame.f_code.co_name if hasattr(upper_frame, "f_code") else None
    )
    if arg_logging.human:
        if module_frame:
            return f"{level.upper()} - {package}:{file}:{module_function}()"
        return f"{level.upper()} - {package}:{file}"
    else:
        return level.upper(), package, file, module_function


# This print the structured format
def _print_structured(message, tag, level, package, file, module_function):
    log = {
        "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "level": level,
        "package": package,
        "file": file,
        "module_function": module_function,
        "message": message,
        "tag": tag,
    }
    print(json.dumps(log, indent=4))


# Generalized wrap functions
def _log_message(level_func, message, tag=None):
    if not arg_logging.human:
        level, package, file, module_function = _get_name()
        _print_structured(message, tag, level, package, file, module_function)
        return
    tag = f" ({tag})" if tag else ""
    level_func(f"{_get_name()}: {message}{tag}")


# Custom debug with custom level
def debug2(message, tag=None):
    if not arg_logging.human:
        level, package, file, module_function = _get_name()
        _print_structured(message, tag, level, package, file, module_function)
        return
    tag = f" ({tag})" if tag else ""
    logger.log(DEBUG2, f"{_get_name()}: {message}{tag}")


# Wrap function
def debug1(message, tag=None):
    _log_message(logger.debug, message, tag)


# Wrap function
def info(message, tag=None):
    _log_message(logger.info, message, tag)


# Wrap function
def warning(message, tag=None):
    _log_message(logger.warning, message, tag)


# Wrap function
def exception(message, tag=None):
    _log_message(logger.exception, message, tag)


# Wrap function
def error(message, tag=None):
    _log_message(logger.error, message, tag)


# Wrap function
def critical(message, tag=None):
    _log_message(logger.critical, message, tag)
