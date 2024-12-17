import argparse
import sys

# Verify arg sanity
if "--logistro_human" in sys.argv and "--logistro_structured" in sys.argv:
    raise ValueError(
        "Using '--logistro_human' or '--logistro_structured' simultaneously is not supported.",
    )


# Customize parser
def customize_parser(add_help=False):
    parser_logging = argparse.ArgumentParser(
        add_help=add_help,
    )
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
    return parser_logging


# Customize parser in pytest_addoption()
def customize_pytest_addoption(parser):  # TODO why does this exist
    parser.addoption(
        "--logistro_human",
        action="store_true",
        dest="human",
        default=True,
        help="Format the logs for humans",
    )
    parser.addoption(
        "--logistro_structured",
        action="store_false",
        dest="human",
        help="Format the logs as JSON",
    )


# parser
parser_logging = customize_parser(add_help=True)

# Get the Format
parsed, _ = parser_logging.parse_known_intermixed_args(sys.argv)
