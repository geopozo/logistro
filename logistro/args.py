import argparse
import sys

# Verify arg sanity
if "--logistro-human" in sys.argv and "--logistro-structured" in sys.argv:
    raise ValueError(
        "Using '--logistro-human' or '--logistro-structured' simultaneously is not supported.",
    )

parser = argparse.ArgumentParser(
    add_help=True,
)
parser.add_argument(
    "--logistro-human",
    action="store_true",
    dest="human",
    default=True,
    help="Format the logs for humans",
)
parser.add_argument(
    "--logistro-structured",
    action="store_false",
    dest="human",
    help="Format the logs as JSON",
)

parser.add_argument(
    "--logistro-level",
    default="WARNING",
    dest="log",
    help="Set the logging level",
)

# Get the Format
parsed, _ = parser.parse_known_intermixed_args(sys.argv)
