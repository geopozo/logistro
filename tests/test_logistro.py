import argparse
import sys
import logistro



def test_customize_parser():
    parser_logging = logistro.customize_parser()
    parser = argparse.ArgumentParser(parents=[parser_logging])
    args, _ = parser.parse_known_intermixed_args(sys.argv)
    assert  hasattr(args, "human")
    assert  hasattr(args, "included_tags")
    assert  hasattr(args, "excluded_tags")

def test_customize_pytest_addoption(human):
    assert  human or not human


def test_logs(caplog):
    # Structured logs
    logistro.set_structured()
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


    # Human logs
    logistro.set_human()
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

    for record in caplog.records:
        assert "Hello world, this is Logistro!" in record

