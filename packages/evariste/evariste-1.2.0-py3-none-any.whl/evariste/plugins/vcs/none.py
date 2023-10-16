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

"""Dummy, do-nothing vcs. Used for tests.

.. autoclass:: NoneVCS
   :members:
   :special-members: __contains__
"""

import pathlib

from . import VCS


class NoneVCS(VCS):
    """Dummy vcs: Does not access any file."""

    keyword = "vcs.none"

    def walk(self):
        yield from []

    def __contains__(self, path: pathlib.Path) -> bool:
        return False

    @property
    def workdir(self) -> pathlib.Path:
        return pathlib.Path.cwd()
