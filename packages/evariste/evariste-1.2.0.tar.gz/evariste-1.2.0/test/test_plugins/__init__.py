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

"""Test of the plugin dependencies"""

import unittest

from evariste.builder import Builder
from evariste.plugins import MANDATORY_PLUGINS
from evariste.setup import Setup


class TestLoadedPlugins(unittest.TestCase):
    """Load plugins"""

    mandatory_plugins = MANDATORY_PLUGINS | {"vcs.none", "logging.quiet"}

    @staticmethod
    def _loaded_plugins(local):
        """Create a builder, from a dummy setup file.

        Return a set a loaded plugins.
        """
        setup = Setup(
            {
                "setup": {
                    "vcs": "vcs.none",
                    "source": ".",
                    "plugins": ["vcs.none"],
                },
                "logging": {
                    "logger": "quiet",
                },
            }
        )
        setup.update(local, extend_list=True)

        with Builder.from_setupdict(setup) as builder:
            return set(builder.plugins.items())  # pylint: disable=no-member
