import json
import logging
import os
import platform
import sys
from threading import Thread

import logistro.args as args

## New Constants and Globals

DEBUG2 = 5
logging.addLevelName(DEBUG2, "DEBUG2")

output = {
    "time": "%(asctime)s",
    "name": "%(name)s",
    "level": "%(levelname)s",
    "module": "%(module)s",
    "func": "%(funcName)s",
    "task": "%(taskName)s",
    "thread": "%(threadName)s",
    "message": "%(message)s",
}

# async taskName not supported below 3.12
if bool(sys.version_info[:3] < (3, 12)):
    del output["task"]

human_formatter = logging.Formatter(":".join(output.values()))
structured_formatter = logging.Formatter(json.dumps(output))

pipe_output = output.copy()
for s in ["time", "module", "func", "task", "thread"]:
    if s in pipe_output:
        del pipe_output[s]

human_pipe_formatter = logging.Formatter(":".join(output.values()))
structured_pipe_formatter = logging.Formatter(":".join(output.values()))


class LogistroLogger(logging.getLoggerClass()):
    def debug1(self, msg, *args, **kwargs):
        super().log(logging.DEBUG, msg, *args, stacklevel=2, **kwargs)

    def debug2(self, msg, *args, **kwargs):
        super().log(DEBUG2, msg, *args, stacklevel=2, **kwargs)


logging.setLoggerClass(LogistroLogger)


def set_human():
    args.parsed.human = True


def set_structured():
    args.parsed.human = False


def _coerce_logger(logger, formatter=None):
    if not formatter:
        if args.parsed.human:
            formatter = human_formatter
        else:
            formatter = structured_formatter
    for handler in logger.handlers:
        handler.setFormatter(formatter)


def _coerce_pipe_logger(logger, formatter=None):
    if not formatter:
        if args.parsed.human:
            formatter = human_pipe_formatter
        else:
            formatter = structured_pipe_formatter
    for handler in logger.handlers:
        handler.setFormatter(formatter)


def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)

    wrapper.has_run = False
    return wrapper


@run_once
def betterConfig(**kwargs):
    logging.basicConfig(**kwargs)
    _coerce_logger(logging.getLogger())


def getLogger(name):
    betterConfig()
    logger = logging.getLogger(name)
    _coerce_logger(logger)
    return logger


class PipeLoggerFilter:
    def __init__(self, parser):
        self._parser = parser

    def filter(self, record):
        return self._parser(record)


def getPipeLogger(
    name,
    formatter=None,
    parser=None,
    default_level=logging.DEBUG,
    IFS="\n",
):
    logger = logging.getLogger(name)
    _coerce_pipe_logger(logger, formatter)
    if parser:
        logger.addFilter(PipeLoggerFilter(parser))
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
                    logger.log(default_level, raw_buffer)
                    return
            except Exception:
                while raw_buffer:
                    line, m, raw_buffer = raw_buffer.partition(IFS)
                    if not m:
                        if line:
                            logger.log(default_level, line)
                        break
                    logger.log(default_level, line)
                return
            while raw_buffer:
                line, m, raw_buffer = raw_buffer.partition(IFS)
                if not m:
                    raw_buffer = line
                    break
                logger.log(default_level, line)

    pipeReader = Thread(target=readPipe, name=name, args=(r, logger, default_level))
    pipeReader.start()
    return w, logger
