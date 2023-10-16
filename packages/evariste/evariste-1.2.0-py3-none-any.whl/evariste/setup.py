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

"""Parse setup file."""

import collections
import configparser
import os
import pathlib
import pprint
import shlex

from . import utils
from .errors import EvaristeError


def Options(*args, **kwargs):
    """Return a :class:`collections.defaultdict` object, default being `None`."""
    # pylint: disable=invalid-name
    return collections.defaultdict(lambda: None, *args, **kwargs)


def Sections(dictionary=None):
    """Return a :class:`collections.defaultdict` object, default being `Options`"""
    # pylint: disable=invalid-name
    if dictionary is None:
        dictionary = {}
    return collections.defaultdict(
        Options, {key: Options(value) for (key, value) in dictionary.items()}
    )


def string2config(string):
    """Parse ``string`` as the content of a configuration file."""
    config = configparser.ConfigParser(allow_no_value=True)
    config.read_string(string)
    return config


class Setup:
    """Representation ef Evariste setup.

    Precondition: If this object is built from a file,
    current working directory is the directory of this file.
    """

    def __init__(self, dictionary=None, *, filename=None):
        if dictionary is None:
            dictionary = {}
        self.dict = Sections(dictionary)

        # Load inherited setup files
        if filename is None:
            self._loaded = []
        else:
            self._loaded = [pathlib.Path(filename).resolve()]

        self._inherit()

        if self["setup"]["cachedir"] is None and filename is not None:
            self["setup"]["cachedir"] = f".{os.path.basename(filename)}.cache"

    def _inherit(self):
        for extends in shlex.split(self.get("setup", {}).get("extends", "")):
            # Inherit setup file
            absextends = pathlib.Path(extends).resolve()

            if not absextends.exists():
                # Raise error on non-existent files
                raise FileNotFoundError(extends)

            if absextends in self._loaded:
                # Prevent extends loop
                continue

            # Remove "setup.extends" option, so that it can be set by inherited setup
            del self["setup"]["extends"]

            self._loaded.append(absextends)
            with utils.ChangeDir(absextends.parent.as_posix()):
                with open(absextends.name, encoding="utf8") as file:
                    self.fill_blanks(string2config(file.read()))
                    self._inherit()

    def __iter__(self):
        yield from self.dict

    def __dict__(self):
        return self.dict

    def __getitem__(self, value):
        return self.dict[value]

    def get(self, key, default=None):
        """Alias to `self.dict.get`."""
        return self.dict.get(key, default)

    def __str__(self):
        # pylint: disable=consider-using-f-string
        return "{{{}}}".format(
            ", ".join([f"{key}: {value}" for key, value in self.dict.items()])
        )

    def __eq__(self, other):
        for section in set(self.keys()) | set(other.keys()):
            for option in set(self[section].keys()) | set(other[section].keys()):
                if self[section][option] != other[section][option]:
                    return False
        return True

    def fill_blanks(self, dictionary):
        """Fill unset self options with argument.

        Returns ``self`` for convenience.
        """
        for section in dictionary:
            if section in self.dict:
                for option in dictionary[section]:
                    if option not in self.dict[section]:
                        self.dict[section][option] = dictionary[section][option]
            else:
                self.dict[section] = Options(dictionary[section])
        return self

    def update(self, other, *, extend_list=False):
        """Update setup, with another setup or dict object.

        Similar to :meth:`dict.update`.

        :param boolean extend_list: If `True` and both values are lists,
            extend the first one with the second one.

        Return `self` for convenience.
        """
        for section in other:
            for option in other[section]:
                if (
                    extend_list
                    and isinstance(self.dict[section][option], list)
                    and isinstance(other[section][option], list)
                ):
                    self.dict[section][option].extend(other[section][option])
                else:
                    self.dict[section][option] = other[section][option]
        return self

    @classmethod
    def from_file(cls, filename):
        """Parse configuration file ``filename``."""
        with open(filename, encoding="utf8") as file:
            return cls(string2config(file.read()), filename=filename)

    def keys(self):
        """Return a new view of the setup’s keys"""
        return self.dict.keys()

    def pprint(self):
        """Pretty print of the object."""
        pprint.pprint(self.dict)

    @property
    def __dict__(self):
        """Return self, as a :class:`dict` of :class:`dict`."""
        dictionary = {}
        for section in self:
            dictionary[section] = dict(self[section])
        return dictionary

    def copy(self):
        """Return a copy of this object."""
        return self.__class__(vars(self))

    def items(self):
        """Iterate over (key, value) pairs, as 2-tuples."""
        yield from self.dict.items()


class SetupError(EvaristeError):
    """Error in setup file."""
