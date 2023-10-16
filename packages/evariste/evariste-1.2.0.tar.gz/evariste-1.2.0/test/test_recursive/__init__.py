# Copyright Louis Paternault 2022
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Test of `evs compile`"""

import difflib
import filecmp
import glob
import os
import pathlib
import shutil
import subprocess
import sys
import unittest

from evariste import utils
from evariste.builder import Builder

SETUP = {
    "setup": {
        "vcs": "vcs.git",
        "source": pathlib.Path(__file__).parent / "data",
        "plugins": ["vcs.git"],
    }
}


def get(obj, *keys):
    """Return `obj[keys[0]][keys[1]][…]`, or `None` if there is a KeyError.

    >>> ddict = {"a": {"aa": 1}, "b": {"bb": {"bbb": 2}}}
    >>> print(get(ddict, "a", "aa"))
    1
    >>> print(get(ddict, "b", "bb", "bbb"))
    2
    >>> print(get(ddict, "a", "c"))
    None
    >>> print(get(ddict, "b", "bb", "c"))
    None
    """
    if keys:
        try:
            return get(obj[keys[0]], *keys[1:])
        except KeyError:
            return None
    return obj


class TestRecursive(unittest.TestCase):
    """Test setup.source and setup.recursive options."""

    def test_recursive(self):
        """Test setup.source and setup.recursive options."""
        with utils.ChangeDir(pathlib.Path(__file__).parent / "data"):
            with Builder.from_setupdict(SETUP) as builder:
                builder.compile()  # pylint: disable=no-member
            self.assertEqual(
                {
                    str(path.from_source): path.config["foo"]["bar"]
                    for path in builder.tree.walk()  # pylint: disable=no-member
                },
                {
                    "a/aa/aaa": "a",
                    "b/bb/bbb": "bb",
                    "c/cc": None,
                    "d/dd/ddd": "d",
                    "e/ee": "e-recursive",
                    "f/ff/fff": "f",
                },
            )
