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

"""Test of the setup plugin"""

import os
import unittest

from evariste.plugins import Plugin
from evariste.setup import Setup
from evariste.shared import Shared
from evariste.utils import ChangeDir

################################################################################

DATADIR = os.path.join(os.path.dirname(__file__), "data")


class First(Plugin):
    """Test plugin"""

    # pylint: disable=abstract-method, too-few-public-methods

    plugin_type = "test"
    default_setup = {"foo": 1, "bar": 2}


class Second(First):
    """Another test plugin"""

    # pylint: disable=abstract-method, too-few-public-methods

    keyword = "test.second"
    default_setup = {"foo": 3, "baz": 4}


class TestDefaultSetup(unittest.TestCase):
    """Testing default setup"""

    # pylint: disable=too-few-public-methods

    def test_inheritance(self):
        """Testing default setup inheritance"""
        plugin = Second(
            Shared(setup=Setup({"setup": {"vcs": "vcs.none"}}), builder=None)
        )
        self.assertEqual(plugin.shared.setup["test.second"]["foo"], 3)
        self.assertEqual(plugin.shared.setup["test.second"]["bar"], 2)
        self.assertEqual(plugin.shared.setup["test.second"]["baz"], 4)

        self.assertEqual(plugin.local.setup["foo"], 3)
        self.assertEqual(plugin.local.setup["bar"], 2)
        self.assertEqual(plugin.local.setup["baz"], 4)


################################################################################


class TestEqual(unittest.TestCase):
    """Test equality method of setup objects."""

    def test_empty(self):
        """Test the :meth:`Setup.__eq__` method on empty setup objects."""
        self.assertEqual(Setup({}), Setup({}))

    def test_same_dict(self):
        """Test the :meth:`Setup.__eq__` method on object built with the same dictionary."""
        base = {"first": {"one": 11, "two": 12}, "second": {"one": 21, "two": 22}}
        self.assertEqual(Setup(base), Setup(base))

    def test_default_objects(self):
        """Test the :meth:`Setup.__eq__` method on object having default values."""
        setup1 = Setup(
            {"first": {"one": 11, "two": 12}, "second": {"one": 21, "two": 22}}
        )
        setup2 = Setup(vars(setup1))

        # Creating default objects
        setup1["three"]  # pylint: disable=pointless-statement
        setup1["one"]["three"]  # pylint: disable=pointless-statement
        setup1["four"]["one"]  # pylint: disable=pointless-statement

        self.assertEqual(setup1, setup2)

    def test_different(self):
        """Test the :meth:`Setup.__eq__` method on different objects."""
        setup1 = Setup(
            {"first": {"one": 11, "two": 12}, "second": {"one": 21, "two": 22}}
        )

        with self.subTest():
            setup2 = setup1.copy()
            setup2["first"]["one"] = "foo"
            self.assertNotEqual(setup1, setup2)

        with self.subTest():
            setup3 = setup1.copy()
            setup3["first"]["three"] = "foo"
            self.assertNotEqual(setup1, setup3)

        with self.subTest():
            setup4 = setup1.copy()
            setup4["three"]["one"] = 31
            self.assertNotEqual(setup1, setup4)


################################################################################


class TestUpdate(unittest.TestCase):
    """Testing method :meth:`setup.Setup.update`."""

    def test_update(self):
        """Test the :meth:`Setup.update` method."""
        setup = Setup(
            {"first": {"one": 11, "two": 12}, "second": {"one": 21, "two": 22}}
        )
        setup.update({"first": {"one": "UPDATED", "three": 13}, "three": {"one": 31}})
        self.assertEqual(
            setup,
            Setup(
                {
                    "first": {"one": "UPDATED", "two": 12, "three": 13},
                    "second": {"one": 21, "two": 22},
                    "three": {"one": 31},
                }
            ),
        )


################################################################################


class TestExtends(unittest.TestCase):
    """Test inheritance of setup files."""

    def test_cycle(self):
        """Test that cycles are detected."""
        with ChangeDir(os.path.join(DATADIR, "cycle")):
            setup = Setup.from_file("a.setup")
            self.assertEqual(setup["setup"]["aaa"], "aaa")
            self.assertEqual(setup["setup"]["bbb"], "bbb")
            self.assertEqual(setup["setup"]["ccc"], "ccc")

    def test_absent(self):
        """Test that non-existent "extends = FOO" setup file raises an error."""
        with ChangeDir(os.path.join(DATADIR, "empty")):
            with self.assertRaises(FileNotFoundError):
                Setup({"setup": {"extends": "does/not/exists"}})
