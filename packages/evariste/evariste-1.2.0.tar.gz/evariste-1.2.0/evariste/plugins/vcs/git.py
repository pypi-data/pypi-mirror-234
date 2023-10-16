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

"""Access to git-versionned files.

.. autoclass:: Git
   :members:
   :special-members: __contains__
"""

import datetime
import logging
import os
import pathlib
import typing
from datetime import datetime

import git

from . import VCS, NoRepositoryError

LOGGER = logging.getLogger(__name__)


class Git(VCS):
    """Access git-versionned files"""

    # pylint: disable=no-member

    keyword = "vcs.git"

    def __init__(self, shared):
        super().__init__(shared)
        try:
            self.repository = git.Repo(
                self.source.as_posix(), search_parent_directories=True
            )
        except git.InvalidGitRepositoryError as error:
            raise NoRepositoryError(self.keyword, self.source) from error

        self._last_modified = self._read_modification_date()

    def _read_modification_date(self):
        """Return a dictionary of versionned files and their last modification time."""
        # Thanks to Marian https://stackoverflow.com/a/35464230
        LOGGER.info("Reading git commit dates…")
        last_modified = {}
        for blob in self.repository.tree():
            if not os.path.isfile(blob.path):
                continue
            commit = next(self.repository.iter_commits(paths=blob.path, max_count=1))
            last_modified[pathlib.Path(blob.path)] = datetime.fromtimestamp(
                commit.committed_date
            )
        # Files not committed yet
        for blob in self.repository.index.iter_blobs():
            if blob[1].path not in last_modified:
                last_modified[pathlib.Path(blob[1].path)] = super().last_modified(
                    self.workdir / blob[1].path
                )
        LOGGER.info("Done")
        return last_modified

    def walk(self) -> typing.Iterable[pathlib.Path]:
        for entry in self._last_modified:
            try:
                yield (self.workdir / entry).relative_to(self.source)
            except ValueError:
                # `self.source` is not a subpath of `path`
                continue

    def __contains__(self, path: pathlib.Path) -> bool:
        try:
            return self.from_repo(path) in self._last_modified
        except ValueError:
            # ``path`` is not a subpath of ``self.workdir``
            return False

    @property
    def workdir(self) -> pathlib.Path:
        return pathlib.Path(self.repository.working_dir)

    def last_modified(self, path: pathlib.Path) -> datetime:
        if path not in self:
            return super().last_modified(path)

        return self._last_modified[self.from_repo(path)]
