import argparse
import sys
import logistro
import logging


def test_customize_parser():
    parser_logging = logistro.customize_parser()
    parser = argparse.ArgumentParser(parents=[parser_logging])
    args, _ = parser.parse_known_intermixed_args(sys.argv)
    assert hasattr(args, "human")
    assert hasattr(args, "included_tags")
    assert hasattr(args, "excluded_tags")


def test_customize_pytest_addoption(human):
    assert human or not human


def test_level_debug2():
    assert logging.getLevelName(5) == "DEBUG2"


def test_structured_logs(caplog):
    # Structured logs
    logistro.set_structured()
    assert logistro.custom_logging.arg_logging.human is False
    logistro.set_level(logistro.DEBUG2)
    logistro.debug2("Hello world, this is Logistro!")
    logistro.debug1("Hello world, this is Logistro!")
    logistro.info("Hello world, this is Logistro!")
    logistro.warning("Hello world, this is Logistro!")
    try:
        raise ValueError("Exception")
    except ValueError:
        logistro.exception("Hello world, this is Logistro!")
    logistro.error("Hello world, this is Logistro!")
    logistro.critical("Hello world, this is Logistro!")

    for record in caplog.records:  # TODO: improve this assert
        assert "Hello world, this is Logistro!" in record.message


def test_human_logs(caplog):
    # Human logs
    logistro.set_human()
    assert logistro.custom_logging.arg_logging.human is True
    logistro.set_level(logistro.DEBUG2)
    logistro.debug2("Hello world, this is Logistro!")
    logistro.debug1("Hello world, this is Logistro!")
    logistro.info("Hello world, this is Logistro!")
    logistro.warning("Hello world, this is Logistro!")
    try:
        raise ValueError("Exception")
    except ValueError:
        logistro.exception("Hello world, this is Logistro!")
    logistro.error("Hello world, this is Logistro!")
    logistro.critical("Hello world, this is Logistro!")

    for record in caplog.records:  # TODO: improve this assert
        assert "Hello world, this is Logistro!" in record.message
