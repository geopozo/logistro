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

pipe_attr_blacklist = ["filename", "funcName", "threadName"]

output = {
    "time": "%(asctime)s",
    "name": "%(name)s",
    "level": "%(levelname)s",
    "file": "%(filename)s",
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


def coerce_logger(logger, formatter=None):
    if not formatter:
        if args.parsed.human:
            formatter = human_formatter
        else:
            formatter = structured_formatter
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
    coerce_logger(logging.getLogger())


def getLogger(name=None):
    betterConfig()
    logger = logging.getLogger(name)
    return logger


class PipeLoggerFilter:
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
    IFS = IFS.encode("utf-8")
    logger = getLogger(name)
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
