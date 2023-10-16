# Copyright Louis Paternault 2020
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

"""Test of the shared plugin"""

import unittest

from evariste import utils


class TestDeepDict(unittest.TestCase):
    """Testing :class:`evariste.utils.DeepDict`"""

    # pylint: disable=too-few-public-methods, no-member

    def test_fill_blanks(self):
        """Test that `fill_blanks` method works."""
        one = utils.DeepDict(2)
        one["a"]["a"] = "aa"
        one["a"]["b"] = "ab"
        one["b"]["a"] = "ba"

        two = utils.DeepDict(2)
        two["c"]["a"] = "ca"
        two["a"]["a"] = "WRONG"
        two["b"]["b"] = "bb"

        one.fill_blanks(two)

        self.assertEqual(one["a"]["a"], "aa")
        self.assertEqual(one["a"]["b"], "ab")
        self.assertEqual(one["b"]["a"], "ba")
        self.assertEqual(one["c"]["a"], "ca")
        self.assertEqual(one["b"]["b"], "bb")
