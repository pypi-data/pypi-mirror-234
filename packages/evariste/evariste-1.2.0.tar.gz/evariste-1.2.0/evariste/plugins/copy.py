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

"""Plugin to copy files at the end of compilation and rendering."""

import contextlib
import glob
import logging
import shutil

from ..hooks import contexthook
from . import Plugin

LOGGER = logging.getLogger("evariste.plugins.copy")


class Copy(Plugin):
    """Copy files at the end of compilation."""

    # pylint: disable=too-few-public-methods

    keyword = "copy"

    @contexthook("Builder.close")
    @contextlib.contextmanager
    def copy(self, builder):
        """Copy files (as configured in the configuration file) at the end of compilation."""
        # pylint: disable=unused-argument

        yield

        for key in self.local.setup:
            if key.startswith("copy"):
                if isinstance(self.local.setup[key], str):
                    arguments = self.local.setup[key].split()
                else:
                    arguments = self.local.setup[key]
                if len(arguments) <= 1:
                    raise ValueError(
                        f"""[copy] Option "{key}" should be "SOURCE [SOURCE] DEST"."""
                    )
                try:
                    sources = arguments[0:-1]
                    dest = arguments[-1]
                except (ValueError, TypeError) as error:
                    raise ValueError(
                        f"""[copy] Option "{key}" should be "SOURCE [SOURCE] DEST"."""
                    ) from error
                LOGGER.info(f"""Copying '{" ".join(sources)}' to '{dest}'.""")
                for source in sources:
                    for path in glob.iglob(source):
                        shutil.copytree(path, dest, dirs_exist_ok=True)
