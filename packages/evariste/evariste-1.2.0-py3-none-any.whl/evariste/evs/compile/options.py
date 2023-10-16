# Copyright Louis Paternault 2015-2022
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Command line options"""

import argparse
import logging
import os
import sys
import textwrap

from ... import VERSION

LOGGER = logging.getLogger("evariste")


def _setup_type(name):
    """Check the argument and return its value.

    The argument must be an existing file.
    """
    if not os.path.exists(name):
        raise argparse.ArgumentTypeError(f"File '{name}' does not exist.")
    if not os.path.isfile(name):
        raise argparse.ArgumentTypeError(f"File '{name}' is not a file.")
    return name


class Options(argparse.Namespace):
    """Namespace of command line options.

    Added ability to iterate over option names.
    """

    # pylint: disable=too-few-public-methods

    def __str__(self):
        return str(
            {
                (attr, getattr(self, attr))
                for attr in dir(self)
                if not attr.startswith("_")
            }
        )

    def __iter__(self):
        for attr in dir(self):
            if not attr.startswith("_"):
                yield attr


def commandline_parser():
    """Return a command line parser."""

    parser = argparse.ArgumentParser(
        prog="evariste",
        description=("Recursively compile files in a directory, and render result."),
        epilog=(
            "Note that `evariste ARGS` and `evs compile ARGS` are the same command."
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--version",
        help="Show version",
        action="version",
        version="%(prog)s " + VERSION,
    )

    parser.add_argument(
        "-v", "--verbose", help="Verbose. Repeat for more details.", action="count"
    )

    parser.add_argument(
        "-q",
        "--quiet",
        help="Quiet. Does not print anything to standard output.",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "-j",
        "--jobs",
        help=(
            "Specify the number of jobs to run simultaneously. Default is one "
            "more than the number of CPUs. "
        ),
        action="store",
        default=os.cpu_count() + 1,
        type=int,
    )

    parser.add_argument(
        "-B",
        "--always-compile",
        dest="always_compile",
        help="Unconditionally make all targets",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "setup",
        metavar="SETUP",
        help=textwrap.dedent(
            """
            Setup file to process.
            """
        ),
        type=_setup_type,
    )

    return parser


def get_options():
    """Return the namespace of (processed) command line options."""
    try:
        return commandline_parser().parse_args(namespace=Options())
    except argparse.ArgumentTypeError as error:
        sys.stderr.write(str(error))
        sys.stderr.write("\n")
        sys.exit(2)
