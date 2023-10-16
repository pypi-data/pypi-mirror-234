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

"""Compilation using commands depending on mimetype or file extensions"""

import glob
import mimetypes
import operator
import pathlib
import re
import shlex

from .command import Command, MissingOption


class AutoCommand(Command):
    """Compilation using rules based on mimetypes and extensions"""

    keyword = "action.autocommand"
    priority = 50

    def get_all_config(self, path):
        """Parse config and return the setup dictionary"""
        config = {}

        # Populate using global setup
        path.config.fill_blanks(
            {
                key: value
                for key, value in self.shared.setup.items()
                if (key.startswith(self.keyword) and key != self.keyword)
            }
        )

        # Analyse config
        for key, setup in path.config.items():
            if key == self.keyword or (not key.startswith(self.keyword)):
                continue

            config[key] = setup.copy()
            if setup["command"] is None:
                raise MissingOption(self.keyword, "command")

            if setup["priority"] is None:
                config[key]["priority"] = (1, key)
            else:
                config[key]["priority"] = (0, int(setup["priority"]))

            if config[key]["extensions"] is None:
                config[key]["extensions"] = ""

            config[key]["mimetypes"] = [
                re.compile(regexp)
                for regexp in shlex.split(config[key].get("mimetypes", ""))
            ]
            config[key]["extensions"] = [
                "." + ext for ext in shlex.split(config[key].get("extensions", ""))
            ]
            if (not config[key]["mimetypes"]) and (not config[key]["extensions"]):
                config[key]["extensions"] = [key[len(self.keyword) :]]

        return config

    def get_matched_config(self, path):
        """Return the configuration associated with the given file.

        May return ``None`` if no command is associated with it.
        """
        for setup in sorted(
            self.get_all_config(path).values(), key=operator.itemgetter("priority")
        ):
            if path.from_fs.suffix in setup["extensions"]:
                return setup
            for regexp in setup["mimetypes"]:
                mime = mimetypes.guess_type(path.from_fs)[0]
                if isinstance(mime, str):
                    if regexp.match(mime):
                        return setup
        return None

    def get_targets(self, path):
        targets = []
        for item in shlex.split(path.format(self.get_matched_config(path)["targets"])):
            for target in glob.glob(
                str(path.parent.from_fs.as_posix() / pathlib.Path(item))
            ):
                targets.append(pathlib.Path(target).relative_to(path.root.from_fs))
        return targets

    def command(self, path):
        return self.get_matched_config(path)["command"]

    def match(self, value):
        return self.get_matched_config(value) is not None
