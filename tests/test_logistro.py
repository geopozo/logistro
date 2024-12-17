import os
import time

import logistro


def write_to_pipe(pipe):
    os.write(pipe, "TEST_PIPE\n".encode("utf-8"))
    os.close(pipe)


def write_to_logger(logger):
    logger.debug2("TEST_DEBUG2")
    logger.debug1("TEST_DEBUG1")
    logger.info("TEST_INFO")
    logger.warning("TEST_WARNING")
    logger.error("TEST_ERROR")
    logger.critical("TEST_CRITICAL")
    try:
        raise ValueError("")
    except ValueError:
        logger.exception("TEST_EXCEPTION")


def test_all_logs(caplog):
    logistro.set_human()
    human = logistro.getLogger("human")
    write_to_logger(human)
    print(caplog.text)
    print("".center(50, "%"))
    caplog.clear()

    w, pipelogger = logistro.getPipeLogger("human-pipe")
    pipelogger.setLevel(logistro.DEBUG2)
    write_to_pipe(w)
    time.sleep(0.5)  # indeterminstic but should be fine
    print(caplog.text)
    print("".center(50, "%"))
    caplog.clear()

    logistro.set_structured()
    structured = logistro.getLogger("structured")
    write_to_logger(structured)
    print(caplog.text)
    print("".center(50, "%"))
    caplog.clear()

    logistro.set_structured()
    changling = logistro.getLogger("changling")
    write_to_logger(changling)
    print(caplog.text)
    print("".center(50, "%"))
    caplog.clear()

    logistro.set_human()
    changling = logistro.getLogger("changling")
    write_to_logger(changling)
    print(caplog.text)
    print("".center(50, "%"))
    caplog.clear()
