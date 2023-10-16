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

"""Build process: gather files, and compile them.

.. autoclass:: Builder
   :members:
"""

# Can be removed starting with python3.11
from __future__ import annotations

import contextlib
import logging
import typing

from . import errors, plugins
from .cache import open_cache
from .hooks import setmethodhook
from .plugins import Loader
from .setup import Setup, SetupError
from .tree import Root

LOGGER = logging.getLogger("evariste")


class Builder(contextlib.AbstractContextManager):
    """Takes care of build process. Can be used as a context.

    .. attribute:: shared
       :type: evariste.shared.Shared

       Object that is shared and accessible by every
       :class:`evariste.plugins.Plugin` and :class:`evariste.tree.Tree`.
       See :ref:`shared`.

    .. attribute:: cache
       :type: evariste.cache.Cache

       Data that is cached between compilations.
       Plugin developpers won't manipulate this attribute directly (see :ref:`shared`).

    .. attribute:: plugins
       :type: evariste.plugins.Loader

       Plugin loader: loaded plugins are gathered there.
    """

    # pylint: disable=no-member

    def __init__(self, setup):
        self.cache = open_cache(setup["setup"]["cachedir"], setup, self)
        self.shared = self.cache.shared
        self.plugins = Loader(shared=self.shared)

        LOGGER.info("Building directory tree…")
        try:
            vcs = list(self.plugins.values(plugin_type="vcs"))
            if len(vcs) != 1:
                raise errors.EvaristeError(
                    # pylint: disable=consider-using-f-string
                    "Exactly one vcs plugin must be enabled (right now: {}).".format(
                        ", ".join([plugin.keyword for plugin in vcs])
                    )
                )
            self.tree = Root.from_vcs(vcs[0])
        except plugins.NoMatch as error:
            raise SetupError(
                # pylint: disable=consider-using-f-string
                "Setup error: Value '{}' is not a valid vcs (available ones are: {}).".format(
                    error.value,
                    ", ".join([f"'{item}'" for item in error.available]),
                )
            ) from error

    @setmethodhook()
    def compile(self):
        """Compile files handled by this builder."""
        LOGGER.info("Compiling…")
        self.tree.root_compile()

    @setmethodhook()
    def close(self):
        """Perform close operations.

        Mainly used as a :ref:`methodhook`.
        """
        self.cache.close()

    @classmethod
    def from_setupname(cls, name: str) -> Builder:
        """Factory that returns a builder, given the name of a :ref:`setup file <setup>`."""
        LOGGER.info("Reading setup…")
        return cls(Setup.from_file(name))

    @classmethod
    def from_setupdict(
        cls, dictionary: typing.Dict[str, typing.Dict[str, str]]
    ) -> Builder:
        """Factory that returns a builder, given a setup dictionary.

        A *setup dictionary* is a dict that mimics :mod:`configparser` structure.
        """
        LOGGER.info("Reading setup…")
        return cls(Setup(dictionary))

    def __enter__(self, *args, **kwargs):
        # pylint: disable=useless-super-delegation
        return super().__enter__(*args, **kwargs)

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.close()
        return super().__exit__(exc_type, exc_value, traceback)
