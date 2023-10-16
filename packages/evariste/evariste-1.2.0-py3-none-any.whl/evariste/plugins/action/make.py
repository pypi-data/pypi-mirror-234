# Copyright Louis Paternault 2015-2021
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

"""Compilation using `make` binary"""

import shlex
import sys

from .command import Command

if sys.version_info >= (3, 8, 0):
    join = shlex.join
else:

    def join(split_command):
        """Backport of :func:`shlex.join` command.

        May be removed when support for python3.7 is dropped.
        """
        return " ".join(shlex.quote(item) for item in split_command)


class MakeCmd(Command):
    """Compilation using `make` binary"""

    keyword = "action.make"
    priority = 50
    default_setup = {"bin": "make", "options": ""}

    def command(self, path):
        # pylint:disable=consider-using-f-string
        return "{bin} {options} {targets}".format(
            bin=self.local.setup["bin"],
            options=self.local.setup["options"],
            targets=join(
                str(path.relative_to(path.parent)) for path in self.get_targets(path)
            ),
        )
