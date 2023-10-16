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

"""Access to VCS (git, etc.) versionned files.

Every path processed here is a :class:`pathlib.Path` object.

.. autoclass:: VCS
   :members:
   :special-members: __contains__

"""

import abc
import os
import pathlib
import typing
from datetime import datetime

from ...errors import EvaristeError
from ...tree import Root
from .. import Plugin


class NoRepositoryError(EvaristeError):
    """No repository contains the given path."""

    def __init__(self, vcstype, directory):
        super().__init__()
        self.directory = directory
        self.vcstype = vcstype

    def __str__(self):
        # pylint: disable=line-too-long
        return f"Could not find any {self.vcstype} repository containing directory '{self.directory}'."


class VCS(Plugin, metaclass=abc.ABCMeta):
    """Generic class to access to versionned files.

    To write a new VCS plugin, one has to subclass this class, and implement every abstract method
    (see for instance the implementation of :class:`evariste.plugin.vcs.git.Git`).
    """

    plugin_type = "vcs"
    global_default_setup = {"setup": {"source": "."}}

    @property
    def source(self) -> pathlib.Path:
        """Return an absolute version of source setup option."""
        return pathlib.Path(self.shared.setup["setup"]["source"]).resolve()

    @abc.abstractmethod
    def walk(self) -> typing.Iterable[pathlib.Path]:
        """Iterate versionned files, descendants of source (as defined by setup file)."""
        raise NotImplementedError()

    @abc.abstractmethod
    def __contains__(self, path: pathlib.Path) -> bool:
        """Return ``True`` iff ``path`` is versionned."""
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def workdir(self) -> pathlib.Path:
        """Return path of the root of the repository."""
        raise NotImplementedError()

    def from_repo(self, path: pathlib.Path) -> pathlib.Path:
        """Return ``path``, relative to the repository root."""
        return path.resolve().relative_to(self.workdir)

    def last_modified(self, path: pathlib.Path) -> datetime:
        """Return the datetime of last modification."""
        return datetime.fromtimestamp(os.path.getmtime(path.as_posix()))
