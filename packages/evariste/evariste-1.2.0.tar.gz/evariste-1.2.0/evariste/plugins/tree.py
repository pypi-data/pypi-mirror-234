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

"""Some features of the `tree.Tree()` class, implemented as hooks."""

import logging
import pathlib

from ..hooks import iterhook
from . import Plugin

LOGGER = logging.getLogger("evariste")


class Tree(Plugin):
    """Some features of the `tree.Tree()` class, implemented as hooks."""

    keyword = "tree"

    @staticmethod
    @iterhook("Tree.prune_before")
    def iter_ignored(tree):
        """Iterate over ignored files."""
        # pylint: disable=too-many-branches
        if tree.is_file():
            for name in ["{}.evsignore", ".{}.evsignore"]:
                if (tree.parent.from_fs / name.format(tree.basename)).exists():
                    yield tree.parent.from_source / name.format(tree.basename)
                    yield tree.from_source
        else:  # Directory
            ignorename = tree.from_fs / ".evsignore"
            if not ignorename.exists():
                return

            yield tree.from_source / ".evsignore"

            with open(ignorename, encoding="utf8") as ignorehandler:
                for line in ignorehandler.readlines():
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith("#"):
                        continue
                    if line.startswith("/"):
                        for file in tree.walk():
                            if (
                                pathlib.Path("/")
                                / file.from_fs.relative_to(tree.from_fs)
                            ).match(line):
                                yield file.from_source
                    else:
                        for file in tree.walk():
                            if file.from_source.match(line):
                                yield file.from_source

    @staticmethod
    @iterhook("Tree.prune_after")
    def iter_depends(tree):
        """Iterate over dependencies."""
        if tree.is_file():
            if tree.report is None:
                # File has not been compiled.
                yield tree.from_source
            else:
                for path in tree.report.depends:
                    yield path.resolve().relative_to(tree.root.from_fs.resolve())
