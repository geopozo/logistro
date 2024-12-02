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
def customize_parser(add_help=False):
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
parser_logging = customize_parser(add_help=True)

# Get the Format
try:
    arg_logging, unknown_args = parser_logging.parse_known_intermixed_args(sys.argv)
    if unknown_args:
        # Just for the warning
        temp_handler = logging.StreamHandler(sys.stderr)

        # Set the formatter
        temp_formatter = logging.Formatter("%(levelname)s: %(message)s")
        temp_handler.setFormatter(temp_formatter)
        temp_logger = logging.getLogger("temp_logger")
        temp_logger.addHandler(temp_handler)

        # Print the warning
        temp_logger.warning("Verify the arguments %s", unknown_args)

        # Remove the handler
        temp_logger.removeHandler(temp_handler)
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
def _print_structured(
    message, tag, stream_output, level, package, file, module_function
):
    log = {
        "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "level": level,
        "package": package,
        "file": file,
        "module_function": module_function,
        "message": message,
        "tag": tag,
    }
    print(json.dumps(log, indent=4), file=stream_output)


# Generalized wrap functions
def _log_message(level_func, message, tag=None, stream_output=sys.stderr):
    if not arg_logging.human:
        names = [handler.stream.name for handler in logger.handlers]
        if stream_output.name not in names:
            raise ValueError(
                f"Verify the handlers, the stream_output is {stream_output.name} and the handlers are {names}"
            )
        level, package, file, module_function = _get_name()
        _print_structured(
            message, tag, stream_output, level, package, file, module_function
        )
        return
    tag = f" ({tag})" if tag else ""
    level_func(f"{_get_name()}: {message}{tag}")


# Custom debug with custom level
def debug2(message, tag=None, stream_output=sys.stderr):
    if not arg_logging.human:
        level, package, file, module_function = _get_name()
        _print_structured(
            message, tag, stream_output, level, package, file, module_function
        )
        return
    tag = f" ({tag})" if tag else ""
    logger.log(DEBUG2, f"{_get_name()}: {message}{tag}")


# Wrap function
def debug1(message, tag=None, stream_output=sys.stderr):
    _log_message(logger.debug, message, tag, stream_output)


# Wrap function
def info(message, tag=None, stream_output=sys.stderr):
    _log_message(logger.info, message, tag, stream_output)


# Wrap function
def warning(message, tag=None, stream_output=sys.stderr):
    _log_message(logger.warning, message, tag, stream_output)


# Wrap function
def exception(message, tag=None, stream_output=sys.stderr):
    _log_message(logger.exception, message, tag, stream_output)


# Wrap function
def error(message, tag=None, stream_output=sys.stderr):
    _log_message(logger.error, message, tag, stream_output)


# Wrap function
def critical(message, tag=None, stream_output=sys.stderr):
    _log_message(logger.critical, message, tag, stream_output)
