import json
import logging
import os
import platform
import sys
from threading import Thread

from logistro import _args as cli_args

## New Constants and Globals

DEBUG2 = 5
"""A more verbose version of `logging.DEBUG`"""

logging.addLevelName(DEBUG2, "DEBUG2")

pipe_attr_blacklist = ["filename", "funcName", "threadName", "taskName"]
"""List of attributes to ignore in getPipeLogger()"""

# Our basic formatting list
_output = {
    "time": "%(asctime)s",
    "name": "%(name)s",
    "level": "%(levelname)s",
    "file": "%(filename)s",
    "func": "%(funcName)s",
    "task": "%(taskName)s",
    "thread": "%(threadName)s",
    "message": "%(message)s",
}

# A more readable, human readable string
_date_string = "%a, %d-%b %H:%M:%S"

# async taskName not supported below 3.12, remove it
if bool(sys.version_info[:3] < (3, 12)):
    del _output["task"]

# Make human output a little more readable
_output_human = _output.copy()
_output_human["func"] += "()"

# Generate formatters
human_formatter = logging.Formatter(
    ":".join(_output_human.values()),
    datefmt=_date_string,
)
"""A `logging.Formatter()` to print output nicely."""

structured_formatter = logging.Formatter(json.dumps(_output))
"""A `logging.Formatter()` to print output as JSON for machine consumption."""


# We set this as the logging class just to add a debug1 and debug2 function
class _LogistroLogger(logging.getLoggerClass()):
    def debug1(self, msg, *args, **kwargs):
        super().log(logging.DEBUG, msg, *args, stacklevel=2, **kwargs)

    def debug2(self, msg, *args, **kwargs):
        super().log(DEBUG2, msg, *args, stacklevel=2, **kwargs)


logging.setLoggerClass(_LogistroLogger)


def set_human():
    """Set `--logistro-human` (default)."""
    cli_args.parsed.human = True


def set_structured():
    """Set `--logistro-structured`."""
    cli_args.parsed.human = False


def coerce_logger(logger, formatter=None):
    """
    Set all a logger's formatters to the formatter specified or default.

    Args:
        logger: The logger to coerce
        formatter: The `logging.Formatter()` object to use- defaults to
            human_formatter or structured_formatter.

    """
    if not formatter:
        formatter = human_formatter if cli_args.parsed.human else structured_formatter
    for handler in logger.handlers:
        handler.setFormatter(formatter)


def _run_once(f):
    def betterConfig(*args, **kwargs):  # noqa: N802 camel-case like logging
        if not betterConfig.has_run:
            betterConfig.has_run = True
            f(*args, **kwargs)

    betterConfig.has_run = False
    return betterConfig


@_run_once
def betterConfig(**kwargs):  # noqa: N802 camel-case like logging
    """
    Call `logging.basicConfig()` with our defaults.

    It will overwrite any `format` or `datefmt` arguments passed.
    It is only ever run once.
    """
    if "level" not in kwargs:
        kwargs["level"] = cli_args.parsed.log.upper()
    logging.basicConfig(**kwargs)
    coerce_logger(logging.getLogger())


def getLogger(name=None):  # noqa: N802 camel-case like logging
    """Call `logging.getLogger()` but check `betterConfig()` first."""
    betterConfig()
    return logging.getLogger(name)


class _PipeLoggerFilter:
    def __init__(self, parser):
        self._parser = parser

    def filter(self, record):
        old_info = {}
        for attr in pipe_attr_blacklist:
            if hasattr(record, attr):
                old_info[attr] = getattr(record, attr)
                setattr(record, attr, "")
        if self._parser:
            return self._parser(record, old_info)
        return True


def getPipeLogger(  # noqa: N802 camel-case like logging
    name,
    parser=None,
    default_level=logging.DEBUG,
    ifs="\n",
):
    r"""
    Is a special `getLogger()` which returns a pipe and logger.

    It spins a separate thread to feed the pipe into the logger.
    Common usage would be to pass the pipe to `Popen(stderr=...)`.
    You should close the pipe `os.close(pipe)` in case the other process
    freezes.

    Args:
        name: the name of the logger (á la `logging.getLogger(name)`)
        parser: a function whose first parameter is a `LogRecord` to modify it.
            If it doesn't return `True`, the whole record is ignored.
            The second parameter is a dictionary of already filtered info.
            See `pipe_attr_blacklist` in `custom_logging.py`.
        default_level: the default level for the logger.
        ifs: The character used as delimiter for pipe reads, defaults:"\n".

    Returns:
        A tuple: (pipe, logger)

    """
    ifs = ifs.encode("utf-8")
    logger = getLogger(name)
    logger.addFilter(_PipeLoggerFilter(parser))
    r, w = os.pipe()

    # needs r, logger, and default_level
    def read_pipe(r, logger, default_level):
        if bool(sys.version_info[:3] >= (3, 12) or platform.system() != "Windows"):
            os.set_blocking(r, True)
        raw_buffer = b""
        while True:
            try:
                last_size = len(raw_buffer)
                raw_buffer += os.read(
                    r,
                    1000,
                )
                if last_size == len(raw_buffer):
                    # Just move us to exception mode
                    raise Exception("")  # noqa: TRY002,TRY301
            # Catch any exception, its all weird OS stuff, the game is up
            except Exception:  # noqa: BLE001
                while raw_buffer:
                    line, _, raw_buffer = raw_buffer.partition(ifs)
                    if line:
                        logger.log(default_level, line.decode())
                return
            while raw_buffer:
                line, m, raw_buffer = raw_buffer.partition(ifs)
                if not m:
                    raw_buffer = line
                    break
                logger.log(default_level, line.decode())

    pipe_reader = Thread(
        target=read_pipe,
        name=name + "Thread",
        args=(r, logger, default_level),
    )
    pipe_reader.start()
    return w, logger
