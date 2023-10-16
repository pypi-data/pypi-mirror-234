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

"""Actions performed to compile files.

The result of an :class:`action <Action>`
(Was it sucessful? Which files were used? What is the log? etc.)
is stored as a :class:`report <Report>`.

If you plan to write your own action plugin, see :ref:`write_action`.

:class:`Action`
---------------

.. autoclass:: Action
   :members:

:class:`Report`
---------------

.. autoclass:: Report
   :members:
"""

# Can be removed starting with python3.11
from __future__ import annotations

import abc
import contextlib
import io
import logging
import os
import pathlib
import threading
import typing

from ... import errors, plugins
from ...hooks import contexthook

if typing.TYPE_CHECKING:
    from ...tree import Tree

LOGGER = logging.getLogger(__name__)


################################################################################
# Actions


class Action(plugins.Plugin, metaclass=abc.ABCMeta):
    """Generic action

    Subclass this to create a new action (see :ref:`write_action`).
    """

    # pylint: disable=too-many-instance-attributes, too-few-public-methods

    plugin_type = "action"

    #: A lock shared by every action.
    #: Can be used for parts of the compilation which are not thread-safe.
    lock: threading.Lock = threading.Lock()

    @abc.abstractmethod
    def compile(self, path: Tree) -> Report:
        """Compile ``path``.

        This function *must* be thread-safe.
        It can use :attr:`Action.lock` if necessary.
        """
        raise NotImplementedError()

    def match(self, value: Tree) -> bool:
        """Return ``True`` if ``value`` can be compiled by this action."""
        # pylint: disable=unused-argument
        return False


class DirectoryAction(Action):
    """Fake action on directories."""

    # pylint: disable=abstract-method, too-few-public-methods

    keyword = "action.directory"

    def compile(self, path):
        success = self._success(path)
        if success:
            message = ""
        else:
            message = "At least one file in this directory failed."
        return Report(path, success=success, log=message, targets=[])

    @staticmethod
    def _success(path):
        """Return ``True`` if compilation of all subpath succeeded."""
        for sub in path:
            if not path[sub].report.success:
                return False
        return True

    def match(self, dummy):
        return False


################################################################################
# Reports


class Report:
    """Report of an action. Mainly a namespace with very few methods."""

    def __init__(self, path, targets=None, success=False, log=None, depends=None):
        # pylint: disable=too-many-arguments

        self.depends = depends
        if self.depends is None:
            self.depends = set()

        if log is None:
            self.log = ""
        else:
            self.log = log

        self.path = path
        if targets is None:
            self.targets = []
        else:
            self.targets = targets
        self._success = success

    @property
    def full_depends(self) -> typing.Set[pathlib.Path]:
        """Set of files this action depends on, including ``self.path``."""
        return self.depends | set([self.path.from_fs])

    @property
    def success(self) -> bool:
        """Was compilation sucessful?"""
        return self._success

    @success.setter
    def success(self, value):
        """Success setter."""
        self._success = value
