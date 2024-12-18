import json
import logging
import os
import platform
import sys
from threading import Thread

import logistro.args as args

## New Constants and Globals

#: A more verbose version of logging.DEBUG
DEBUG2 = 5

logging.addLevelName(DEBUG2, "DEBUG2")

#: These are useless when logging external process output. See getPipeLogger()
pipe_attr_blacklist = ["filename", "funcName", "threadName", "taskName"]

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

# make human output a little more readable
_output_human = _output.copy()
_output_human["func"] += "()"

# generate format string
human_formatter = logging.Formatter(
    ":".join(_output_human.values()),
    datefmt=_date_string,
)
structured_formatter = logging.Formatter(json.dumps(_output))


# We set this as the logging class just to add a debug1 and debug2 function
class _LogistroLogger(logging.getLoggerClass()):
    def debug1(self, msg, *args, **kwargs):
        super().log(logging.DEBUG, msg, *args, stacklevel=2, **kwargs)

    def debug2(self, msg, *args, **kwargs):
        super().log(DEBUG2, msg, *args, stacklevel=2, **kwargs)


logging.setLoggerClass(_LogistroLogger)


def set_human():
    """set_human() is the same as passing --logistro-human (default)"""
    args.parsed.human = True

    """set_structured() is the same as passing --logistro-structured"""


def set_structured():
    args.parsed.human = False


def coerce_logger(logger, formatter=None):
    """coerce_logger() will loop through all of a logger's formatters and set
    either the formatter specified, or default to human/structured based on flags
    or if a set_* function was called

    :param logger: The logger to coerce
    :param formatter: The logging.Formatter() objecto use- defaults to
        human_formatter or structured_formatter

    """
    if not formatter:
        if args.parsed.human:
            formatter = human_formatter
        else:
            formatter = structured_formatter
    for handler in logger.handlers:
        handler.setFormatter(formatter)


def _run_once(f):
    def betterConfig(*args, **kwargs):
        if not betterConfig.has_run:
            betterConfig.has_run = True
            return f(*args, **kwargs)

    betterConfig.has_run = False
    return betterConfig


@_run_once
def betterConfig(**kwargs):
    """betterConfig is a wrapper over logging.basicConfig which
    provides our defaults (level set by --logistro-level and formatter
    set to human/structured. Currently, it will overwrite any format
    or datefmt arguments passed. It is only ever run once.

    """
    if "level" not in kwargs:
        kwargs["level"] = args.parsed.log.upper()
    logging.basicConfig(**kwargs)
    coerce_logger(logging.getLogger())


def getLogger(name=None):
    """getLogger() is a simple wrapper for logging.getLogger()
    which calls betterConfig() first."""
    betterConfig()
    logger = logging.getLogger(name)
    return logger


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


def getPipeLogger(
    name,
    parser=None,
    default_level=logging.DEBUG,
    IFS="\n",
):
    """getPipeLogger() is a special getLogger which returns a pipe and logger.
    It spins a separate thread that listens on the pipe and outputs everything
    it reads to the logger named. It is used, for example, to redirect Popen()
    stderr to the logs. You should close the pipe `os.close(pipe)` to be sure
    when exiting your program- in case the other side hangs or freezes.
    :param name: the name of the logger (ie logging.getLogger(name))
    :param parser: an optional function which accepts a LogRecord (see logging
        docs) as well as a dictionary of already stripped values.
        The signature of parser should be: fn(record, old). It functions like
        a logging.Filter, and can be used to parse the other processes output
        if it's structured. The argument `old` is a dictionary of metadata
        that we strip from the log record due to irrelevancy, see the
        pipe_attr_blacklist list.
    :param default_level: the default level to pipe these logs to. Can be modified
        with the parser as described above.
    :param IFS: (Internal Field Separate) The character used to delimit between
        process output, defaults to "\n".
    """
    IFS = IFS.encode("utf-8")
    logger = getLogger(name)
    logger.addFilter(_PipeLoggerFilter(parser))
    r, w = os.pipe()

    # needs r, logger, and default_level
    def readPipe(r, logger, default_level):
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
                    if raw_buffer:
                        logger.log(default_level, raw_buffer.decode())
                    return
            except Exception:
                while raw_buffer:
                    line, m, raw_buffer = raw_buffer.partition(IFS)
                    if not m:
                        if line:
                            logger.log(default_level, line.decode())
                        break
                    logger.log(default_level, line.decode())
                return
            while raw_buffer:
                line, m, raw_buffer = raw_buffer.partition(IFS)
                if not m:
                    raw_buffer = line
                    break
                logger.log(default_level, line.decode())

    pipeReader = Thread(
        target=readPipe,
        name=name + "Thread",
        args=(r, logger, default_level),
    )
    pipeReader.start()
    return w, logger
