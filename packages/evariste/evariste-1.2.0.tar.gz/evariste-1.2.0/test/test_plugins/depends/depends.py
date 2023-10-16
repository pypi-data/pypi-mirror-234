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

"""Set of plugins testing plugin dependency, and enabling/disabling plugins.

Does nothing, but printing stuff to standard output.
"""

import os
import pathlib
from datetime import datetime

from evariste import plugins


class TestPlugin(plugins.Plugin):
    """Generic test plugin"""


################################################################################
# Dummy plugins


class Foo(TestPlugin):
    keyword = "foo"


class Bar(TestPlugin):
    keyword = "bar"


################################################################################
# Dependencies : First simple plugins


class DependsFoo(TestPlugin):
    keyword = "dependsfoo"
    depends = ["foo"]


class DependsBar(TestPlugin):
    keyword = "dependsbar"
    depends = ["bar"]


class DependsBoth(TestPlugin):
    keyword = "dependsboth"
    depends = ["foo", "bar"]


################################################################################
# Dependecies : Non-existent dependency


class NonExistentDependency(TestPlugin):
    keyword = "nonexistentdependency"
    depends = ["nonexistent"]


################################################################################
# Dependecies : Recursive dependency


class DependsFoo2(TestPlugin):
    keyword = "dependsfoo2"
    depends = ["dependsfoo1"]


class DependsFoo1(TestPlugin):
    keyword = "dependsfoo1"
    depends = ["foo"]


################################################################################
# Circular dependency


class Circular1(TestPlugin):
    keyword = "circular1"
    depends = ["circular2"]


class Circular2(TestPlugin):
    keyword = "circular2"
    depends = ["circular1"]
