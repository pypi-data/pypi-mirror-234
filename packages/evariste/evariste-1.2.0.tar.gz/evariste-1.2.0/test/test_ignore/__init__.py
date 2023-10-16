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
        "source": pathlib.Path(__file__).parent / "data" / "tree",
        "plugins": ["vcs.git"],
    },
    "logging": {
        "logger": "quiet",
    },
}


class TestIgnore(unittest.TestCase):
    """Test that path are correctly ignored."""

    def test_ignore(self):
        """Test that path are correctly ignored."""
        with utils.ChangeDir(pathlib.Path(__file__).parent / "data"):
            with Builder.from_setupdict(SETUP) as builder:
                builder.compile()  # pylint: disable=no-member
            self.assertEqual(
                set(
                    str(path.from_source)
                    for path in builder.tree.walk()  # pylint: disable=no-member
                ),
                set(
                    (
                        "a/b/tagada.md",
                        "baz",
                        "c/tata.txt",
                        "c/titi.txt",
                        "c/toto.txt",
                        "d/d/d/d/d/tata.txt",
                        "d/d/d/d/d/titi.txt",
                        "d/d/d/d/d/toto.txt",
                        "d/d/d/d/titi.txt",
                        "d/d/d/d/toto.txt",
                        "d/d/d/tata.txt",
                        "d/d/d/toto.txt",
                        "d/d/tata.txt",
                        "d/d/titi.txt",
                    )
                ),
            )
