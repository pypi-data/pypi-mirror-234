# Copyright 2015-2021 Louis Paternault
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

"""Tests"""

import doctest
import importlib
import pkgutil

import evariste


def iter_modules(package):
    """Itérateur sur tous les sous-modules de celui donné en argument, récursivement."""
    yield package
    for __finder, name, ispkg in pkgutil.iter_modules(
        package.__path__, package.__name__ + "."
    ):
        newpackage = importlib.import_module(name)
        yield newpackage
        if ispkg:
            yield from iter_modules(newpackage)


def load_tests(__loader, tests, __ignore):
    """Load tests (doctests)."""
    # Loading doctests
    for module in iter_modules(evariste):
        tests.addTests(doctest.DocTestSuite(module))
    return tests
