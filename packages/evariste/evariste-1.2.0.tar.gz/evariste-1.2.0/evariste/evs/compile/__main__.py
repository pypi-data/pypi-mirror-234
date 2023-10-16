# Copyright Louis Paternault 2017-2022
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

"""Command line client to :mod:`evariste`"""

import logging
import os
import sys

from ... import errors
from ...builder import Builder
from ...evs.compile.options import get_options
from ...setup import Setup
from ...utils import ChangeDir

LOGGER = logging.getLogger("evariste")

DEFAULT_SETUP = {"changed": {"time": "fs"}}


def main():
    """Main function"""
    arguments = get_options()
    try:
        # pylint: disable=no-member
        with ChangeDir(os.path.dirname(arguments.setup)):
            # Command lines arguments are available in setup
            setup = Setup.from_file(os.path.basename(arguments.setup))
            setup.fill_blanks({"arguments": vars(arguments)})
            setup.fill_blanks(DEFAULT_SETUP)
            with Builder(setup) as builder:
                builder.compile()
    except errors.EvaristeError as error:
        LOGGER.error("Error: %s.", error)
        sys.exit(1)
    except errors.EvaristeBug as bug:
        LOGGER.error("Error: %s.", bug)
        LOGGER.error(
            "You should not see this: you just discovered a bug. Please copy "
            "the full error message and report a bug."
        )
        sys.exit(2)
    except KeyboardInterrupt:
        LOGGER.error("Aborted.")
        sys.exit(1)


if __name__ == "__main__":
    main()
