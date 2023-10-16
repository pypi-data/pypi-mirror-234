# Copyright Louis Paternault 2017-2022
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

"""Cached action. Nothing has changed since last compilation."""

import contextlib
import pathlib

from ...hooks import contexthook
from . import Action, Report


class Cached(Action):
    """Cached action. Nothing has changed since last compilation."""

    keyword = "action.cached"

    def compile(self, path):
        cached = self.shared.tree[path.from_source]["changed"]
        if cached is None:
            targets = [path.from_source]
            depends = set()
        else:
            targets = [
                pathlib.Path(filename).relative_to(path.root.from_fs)
                for filename in cached["targets"]
            ]
            depends = {
                pathlib.Path(depends) for depends in cached["depends"].keys()
            } - set([path.from_fs])
        return Report(
            path,
            targets=targets,
            depends=depends,
            success=True,
            log=self.local.tree[path.from_source],
        )

    @contexthook("File.compile")
    @contextlib.contextmanager
    def cache_log(self, tree):
        """Save the compilation log in the cache."""
        yield
        self.local.tree[tree.from_source] = tree.report.log
