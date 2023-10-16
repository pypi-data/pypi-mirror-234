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

import os

from evariste.plugins import PluginNotFound

from . import TestLoadedPlugins

DEPENDSDIR = os.path.join(os.path.dirname(__file__), "depends")


def string2set(string):
    """Turn a string into a set of stripped non-empty lines"""
    return {line.strip() for line in string.split("\n") if line.strip()}


class TestDefaultSetup(TestLoadedPlugins):
    """Testing default setup"""

    # pylint: disable=too-few-public-methods

    def test_noplugins(self):
        """Test default and required plugins."""
        self.assertSetEqual(
            self._loaded_plugins({"setup": {"libdirs": DEPENDSDIR}}),
            self.mandatory_plugins,
        )

    def test_disable_default(self):
        """Disabling a default plugin is ignored"""
        self.assertSetEqual(
            self._loaded_plugins(
                {
                    "setup": {
                        "libdirs": DEPENDSDIR,
                    },
                    "action.row": {
                        "enable": False,
                    },
                }
            ),
            self.mandatory_plugins,
        )

    def test_non_existent_plugin(self):
        """Test exception when trying to enable a non-existent plugin."""
        with self.subTest():
            with self.assertRaises(PluginNotFound):
                self._loaded_plugins(
                    {
                        "setup": {
                            "libdirs": DEPENDSDIR,
                            "plugins": ["nonexistent"],
                        }
                    }
                )

        with self.subTest():
            with self.assertRaises(PluginNotFound):
                self._loaded_plugins(
                    {
                        "setup": {
                            "libdirs": DEPENDSDIR,
                            "plugins": ["nonexistentdependency"],
                        }
                    }
                )

    def test_depends_simple(self):
        """Test simple dependencies"""
        with self.subTest():
            self.assertSetEqual(
                self._loaded_plugins(
                    {
                        "setup": {
                            "libdirs": DEPENDSDIR,
                            "plugins": ["dependsfoo"],
                        }
                    }
                ),
                set(["dependsfoo", "foo"]) | self.mandatory_plugins,
            )

        with self.subTest():
            self.assertSetEqual(
                self._loaded_plugins(
                    {
                        "setup": {
                            "libdirs": DEPENDSDIR,
                        },
                        "dependsfoo": {
                            "enable": "True",
                        },
                    }
                ),
                set(["dependsfoo", "foo"]) | self.mandatory_plugins,
            )

    def test_depends_recursive(self):
        """Test recursive dependencies"""
        self.assertSetEqual(
            self._loaded_plugins(
                {
                    "setup": {
                        "libdirs": DEPENDSDIR,
                        "plugins": ["dependsfoo2"],
                    }
                }
            ),
            set(
                [
                    "dependsfoo1",
                    "dependsfoo2",
                    "foo",
                ]
            )
            | self.mandatory_plugins,
        )

    def test_depends_enable(self):
        """Test precedence of "enable=True" over "plugins"."""

        self.assertSetEqual(
            self._loaded_plugins(
                {
                    "setup": {
                        "libdirs": DEPENDSDIR,
                        "plugins": ["foo"],
                    },
                    "foo": {
                        "enable": "False",
                    },
                }
            ),
            self.mandatory_plugins,
        )

    def test_circular_dependency(self):
        """Test circular dependency."""

        self.assertSetEqual(
            self._loaded_plugins(
                {
                    "setup": {
                        "libdirs": DEPENDSDIR,
                        "plugins": ["circular1"],
                    },
                    "foo": {
                        "enable": "False",
                    },
                }
            ),
            {"circular1", "circular2"} | self.mandatory_plugins,
        )
