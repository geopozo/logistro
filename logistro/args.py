import argparse
import sys

# Verify arg sanity
if "--logistro_human" in sys.argv and "--logistro_structured" in sys.argv:
    raise ValueError(
        "Using '--logistro_human' or '--logistro_structured' simultaneously is not supported.",
    )

parser_logging = argparse.ArgumentParser(
    add_help=True,
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


# Get the Format
parsed, _ = parser_logging.parse_known_intermixed_args(sys.argv)
