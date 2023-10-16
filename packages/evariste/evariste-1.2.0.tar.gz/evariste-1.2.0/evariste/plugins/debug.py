# Copyright Louis Paternault 2022
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

"""Some plugins to assist Évariste development."""

import contextlib

from ..hooks import contexthook, iterhook
from . import Plugin


class DebugHooks(Plugin):
    """Print hook calls"""

    # pylint: disable=missing-function-docstring

    keyword = "debug.hooks"

    def __init__(self, *args, **kwargs):
        print(f"Calling __init__({self}, {args}, {kwargs})")
        super().__init__(*args, **kwargs)

    @contexthook("Builder.compile")
    @contextlib.contextmanager
    def builder_compile(self, *args, **kwargs):
        print(f'Entering hook "Builder.compile": {self}, {args}, {kwargs}')
        yield
        print(f'Leaving hook "Builder.compile": {self}, {args}, {kwargs}')

    @contexthook("Builder.close")
    @contextlib.contextmanager
    def builder_close(self, *args, **kwargs):
        print(f'Entering hook "Builder.close": {self}, {args}, {kwargs}')
        yield
        print(f'Leaving hook "Builder.close": {self}, {args}, {kwargs}')

    @contexthook("Tree")
    @contextlib.contextmanager
    def tree(self, *args, **kwargs):
        print(f'Entering hook "Tree": {self}, {args}, {kwargs}')
        yield
        print(f'Leaving hook "Tree": {self}, {args}, {kwargs}')

    @contexthook("File.compile")
    @contextlib.contextmanager
    def file_compile(self, *args, **kwargs):
        print(f'Entering hook "File.compile": {self}, {args}, {kwargs}')
        yield
        print(f'Leaving hook "File.compile": {self}, {args}, {kwargs}')

    @contexthook("File.make_archive")
    @contextlib.contextmanager
    def file_make_archive(self, *args, **kwargs):
        print(f'Entering hook "File.make_archive": {self}, {args}, {kwargs}')
        yield
        print(f'Leaving hook "File.make_archive": {self}, {args}, {kwargs}')

    @iterhook("Tree.prune_before")
    def tree_prune_before(self, *args, **kwargs):
        print(f"""Calling hook "Tree.prune_before": {self}, {args}, {kwargs}""")
        yield from ()

    @iterhook("Tree.prune_after")
    def tree_prune_after(self, *args, **kwargs):
        print(f"""Calling hook "Tree.prune_after": {self}, {args}, {kwargs}""")
        yield from ()
