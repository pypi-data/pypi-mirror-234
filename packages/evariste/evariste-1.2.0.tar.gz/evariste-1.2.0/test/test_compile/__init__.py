# Copyright Louis Paternault 2020-2022
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
import shutil
import subprocess
import sys
import unittest

from evariste import utils
from evariste.builder import Builder
from evariste.setup import Setup

SETUP = "evariste.setup"


class DynamicTest(type):
    """Metaclass that creates on-the-fly test methods.

    It creates a test method for each directory in `data`.
    """

    def __init__(cls, name, bases, nmspc):
        # pylint: disable=no-value-for-parameter
        super().__init__(name, bases, nmspc)
        for methodname, testmethod in cls._iter_testmethods():
            setattr(cls, methodname, testmethod)

    def _iter_testmethods(cls):
        """Iterate over dynamically generated test methods."""
        raise NotImplementedError()


class TestCompilation(unittest.TestCase, metaclass=DynamicTest):
    """Test that `evs compile` works, by comparing created files."""

    @classmethod
    def _iter_testmethods(cls):
        """Iterate over dynamically generated test methods"""
        for source in sorted(
            glob.glob(
                os.path.join(
                    os.path.dirname(__file__),
                    "data",
                    "*",
                )
            )
        ):
            if not os.path.exists(cls._setupfile(source)):
                continue
            yield (
                f"test_compile_{os.path.basename(source)}",
                cls._create_compile_test(source),
            )

    @staticmethod
    def _setupfile(source):
        return os.path.join(source, SETUP)

    @classmethod
    def _create_compile_test(cls, source):
        """Create and return the test method for test directory `source`."""

        def test_compile(self):
            """Test `source` directory.

            That is, in `source`:
            - run `evs compile evariste.setup`;
            - check that created directory `dest` is equal to `expected`.
            """
            with utils.ChangeDir(source):
                # Remove old destination directory and cache
                shutil.rmtree("dest", ignore_errors=True)
                shutil.rmtree(f".{SETUP}.cache", ignore_errors=True)
                os.makedirs("dest", exist_ok=True)

                # Run compilation
                with Builder.from_setupname(SETUP) as builder:
                    builder.compile()  # pylint: disable=no-member

                # Compare expected output to actual output
                self.assertTreeEqual("dest", "expected")

        with open(os.path.join(source, "description.txt"), encoding="utf8") as desc:
            test_compile.__doc__ = desc.read()

        return test_compile

    @staticmethod
    def _walk(directory):
        for root, __, files in os.walk(directory):
            for file in files:
                yield os.path.join(root, file)[len(directory) + 1 :]

    def assertTreeEqual(self, left, right):  # pylint: disable=invalid-name
        """Assert that directories `left` and `right` are equal.

        That is:
        - they contain the same files;
        - files are equal.

        Empty directories are ignored.
        """
        leftcontent = set(self._walk(left))
        rightcontent = set(self._walk(right))

        if leftcontent - rightcontent:
            filecmp.dircmp(left, right).report_full_closure()
            raise AssertionError(
                "Some files if first directory are missing in second directory."
            )
        if rightcontent - leftcontent:
            filecmp.dircmp(left, right).report_full_closure()
            raise AssertionError(
                "Some files in second directory are missing in first directory."
            )

        # If we got to this point, then leftcontent == rightcontent
        for name in leftcontent:
            if not filecmp.cmp(
                os.path.join(left, name), os.path.join(right, name), shallow=False
            ):
                filecmp.dircmp(left, right).report_full_closure()
                leftname = os.path.join(left, name)
                rightname = os.path.join(right, name)
                with open(leftname, encoding="utf8") as leftfile, open(
                    rightname, encoding="utf8"
                ) as rightfile:
                    sys.stdout.writelines(
                        difflib.unified_diff(
                            leftfile.readlines(),
                            rightfile.readlines(),
                            fromfile=leftname,
                            tofile=rightname,
                        )
                    )
                raise AssertionError(f"""File "{name}" differ in directories.""")
