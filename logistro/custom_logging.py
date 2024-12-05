import argparse
import inspect
import logging
import json
import sys
import time


# new constant
DEBUG2 = 5

# Create the logging
basicConfig = logging.basicConfig
logging.addLevelName(DEBUG2, "DEBUG2")

# Set logger
logger = logging.getLogger(__name__)

# Create handler
handler = logging.StreamHandler(stream=sys.stderr)


# Split the list of strings
def verify_string(arg):
    if arg.startswith("[") and arg.endswith("]"):
        return arg.split(",")
    else:
        raise ValueError("You must use a list like '[a, b, c]'")


# Customize parser
def customize_parser(add_help=False):
    parser_logging = argparse.ArgumentParser(add_help=add_help)
    parser_logging.add_argument(
        "--logistro_human",
        action="store_true",
        dest="human",
        default=True,
        help="Format the logs for humans",
    )
    parser_logging.add_argument(
        "--logistro_structured",
        action="store_false",
        dest="human",
        help="Format the logs as JSON",
    )
    parser_logging.add_argument(
        "--logistro_tags",
        type=verify_string,
        dest="tags",
        default=None,
        help="Tags to filter the logs",
    )
    return parser_logging


# parser
parser_logging = customize_parser(add_help=True)

# Get the Format
arg_logging, unknown_args = parser_logging.parse_known_intermixed_args(sys.argv)
if "--logistro_human" in sys.argv and "--logistro_structured" in sys.argv:
    raise ValueError(
        "You must use just one flag: '--logistro_human' or '--logistro_structured'. You must not use both flags."
    )
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

# Create Formatter
if arg_logging.human:
    formatter = logging.Formatter("%(asctime)s - %(message)s")  # TODO
    handler.setFormatter(formatter)  # Customize logger

# Add handler
logger.addHandler(handler)

# Avoid the log from the ancestor's logger
logger.propagate = False


# Improve the name of the log
def _get_context_info():
    # In logistro
    logistro_wrap_fn = (
        inspect.currentframe().f_back.f_back
    )  # This gets the frame of the wrap function
    level = (
        logistro_wrap_fn.f_code.co_name
    )  # This gets the name of the wrap function: debug2, debug1, warning, etc

    # In the module where logistro is used
    module_fn_frame = logistro_wrap_fn.f_back  # This gets the frame of the module
    module_obj = inspect.getmodule(module_fn_frame) or inspect.getmodule(
        module_fn_frame.f_back
    )  # This gets the module object with the info where logistro is used
    package = module_obj.__package__
    file = module_obj.__name__

    # The function where logistro is used
    module_function = (
        module_fn_frame.f_code.co_name if hasattr(module_fn_frame, "f_code") else None
    )  # This gets the name of the function
    return level.upper(), package, file, module_function


# This verify the strings of the tags
def _verify_tags(arg, tags):
    arg_tags = set(arg.tags) if arg.tags is not None else None
    user_tags = set(tags) if tags is not None else None
    if arg_tags and user_tags:
        intersection = tags.issubset(user_tags)
        if not intersection:
            return False
        return True
    elif arg_tags and not user_tags:
        return False
    return True


# This print the structured format
def _print_structured(
    message, tags, stream_output, level, package, file, module_function
):
    log = {
        "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "level": level,
        "package": package,
        "file": file,
        "module_function": module_function,
        "message": message,
        "tags": tags,
    }
    print(json.dumps(log, indent=4), file=stream_output)


# Generalized wrap functions
def _log_message(level_func, message, tags=None, stream_output=sys.stderr):
    if not _verify_tags(arg_logging, tags):
        return
    level, package, file, module_function = _get_context_info()
    if not arg_logging.human:
        names = [handler.stream.name for handler in logger.handlers]
        if stream_output.name not in names:
            raise ValueError(
                f"Verify the handlers, the stream_output is {stream_output.name} and the handlers are {names}"
            )
        _print_structured(
            message, tags, stream_output, level, package, file, module_function
        )
        return

    tags = f" ({tags})" if tags else ""
    logistro_log = (
        f"{level} - {package}:{file}:{module_function}(): {message}{tags}"
        if module_function
        else f"{level} - {package}:{file}: {message}{tags}"
    )
    if level == "DEBUG2":
        logger.log(DEBUG2, logistro_log)
    else:
        level_func(logistro_log)


# Custom debug with custom level
def debug2(message, tags=None, stream_output=sys.stderr):
    _log_message(None, message, tags, stream_output)


# Wrap function
def debug1(message, tags=None, stream_output=sys.stderr):
    _log_message(logger.debug, message, tags, stream_output)


# Wrap function
def info(message, tags=None, stream_output=sys.stderr):
    _log_message(logger.info, message, tags, stream_output)


# Wrap function
def warning(message, tags=None, stream_output=sys.stderr):
    _log_message(logger.warning, message, tags, stream_output)


# Wrap function
def exception(message, tags=None, stream_output=sys.stderr):
    _log_message(logger.exception, message, tags, stream_output)


# Wrap function
def error(message, tags=None, stream_output=sys.stderr):
    _log_message(logger.error, message, tags, stream_output)


# Wrap function
def critical(message, tags=None, stream_output=sys.stderr):
    _log_message(logger.critical, message, tags, stream_output)
