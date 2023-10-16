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

"""A rag-bag of utility functions that did not fit anywhere else.

.. autoclass:: DeepDict
   :members:

.. autofunction:: smart_open

.. autofunction:: yesno

.. autofunction:: expand_path

.. autoclass:: ChangeDir

.. autofunction:: cached_iterator

"""

# Can be removed starting with python3.11
from __future__ import annotations

import configparser
import contextlib
import functools
import importlib
import io
import logging
import os
import pkgutil
import re
import shutil
import sys
import typing
from collections import defaultdict

RE_BRACKETS = re.compile("{[^{]*}")
LOGGER = logging.getLogger(__name__)


def copy(source, destination):
    """Copy ``source`` to ``destination``, creating directories if necessary."""
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    shutil.copy2(source, destination)


def partial_format(string, *args, **kwargs):
    """Format string, leaving unfilled fields untouched.

    >>> partial_format("To {verb} or {negation} to {verb}", negation="not")
    'To {verb} or not to {verb}'
    """
    dictionary = {field[1:-1]: field for field in re.findall(RE_BRACKETS, string)}

    dictionary.update(kwargs)
    return string.format(*args, **dictionary)


@contextlib.contextmanager
def smart_open(filename, mode="w", encoding="utf8"):
    """Open filename, standard output, or nothing.


    :param str filename: If ``filename`` is:

        * ``""`` (the empty string): return a fake file object,
            which is empty if file is open for reading,
            and can be written in if file is open for writing (but content is then discarded);
        * ``"-"`` (a dash):
            read from standard input, or write to standard output (depending on mode);
        * any other: open the given file.
    :param str mode: Same as the ``mode`` parameter of :func:`open`.
    :param str encoding: Same as the ``encoding`` parameter of :func:`open`.
    """
    if (not filename) or (not filename.strip()):
        with io.StringIO() as file:
            yield file
    elif filename.strip() == "-":
        if "w" in mode:
            yield sys.stdout
        elif "r" in mode:
            yield sys.stdin
    else:
        with open(filename, mode, encoding=encoding) as file:
            yield file


def yesno(arg: typing.Union[bool, str, int, None]) -> bool:
    """Interpret some (mostly :class:`str`) variable as a boolean.

    >>> yesno("y")
    True
    >>> yesno("0")
    False
    >>> yesno("1")
    True
    >>> yesno("Yes")
    True
    >>> yesno("True")
    True
    >>> yesno("something senseless")
    False
    >>> yesno(None)
    False
    """
    if isinstance(arg, bool):
        return arg
    try:
        return bool(int(arg))
    except (ValueError, TypeError):
        pass
    if isinstance(arg, str):
        return arg.lower() in ["y", "yes", "true"]
    return bool(arg)


class ChangeDir(contextlib.AbstractContextManager):
    """Context manager to change and restore current directory."""

    # pylint: disable=too-few-public-methods

    def __init__(self, directory):
        if not directory:
            directory = "."
        self._newdir = directory
        self._olddir = os.getcwd()

    def __enter__(self, *args, **kwargs):
        self._olddir = os.getcwd()
        os.chdir(self._newdir)
        return super().__enter__(*args, **kwargs)

    def __exit__(self, *args, **kwargs):
        os.chdir(self._olddir)
        return super().__exit__(*args, **kwargs)


def expand_path(path):
    """Return ``path`` where environment variables and user directory have been expanded."""
    return os.path.expanduser(os.path.expandvars(path))


class DeepDict(defaultdict):
    """Dictionary of dictionary of ... of dictionaries.

    All the dictionaries (expeted the last one) are :class:`collections.defaultdict` objects.
    """

    def __init__(self, depth, dictionary=None):
        if dictionary is None:
            dictionary = {}

        self.depth = depth
        if depth == 1:
            # pylint: disable=unnecessary-lambda-assignment
            factory = lambda: None
        else:
            factory = functools.partial(self.__class__, depth - 1)

        super().__init__(factory)
        for key, value in dictionary.items():
            self[key].update(value)

    @classmethod
    def from_configparser(cls, config: configparser.ConfigParser) -> DeepDict:
        """Create a :class:`DeepDict` object from a :class:`configparser.ConfigParser` object."""
        dictionary = cls(2)
        for section in config.sections():
            for option in config.options(section):
                dictionary[section][option] = config.get(section, option)
        return dictionary

    def get_subkey(self, subkey):
        """Return the first ``self[ANY][subkey]``, when ``ANY`` is any dictionary key."""
        for key in sorted(self):
            if subkey in self[key]:
                return self[key][subkey]
        raise KeyError(subkey)

    @property
    def __dict__(self):
        """Convert self to regular :type:`dict`."""
        if self.depth == 1:
            return dict(self)
        return {key: vars(value) for (key, value) in self.items()}

    def fill_blanks(self, other: dict):
        """Recursively copy values of ``other`` into ``self``.

        The values are copied only if those of ``self`` are not defined.
        """
        if self.depth == 1:
            for key in other:
                if key not in self:
                    self[key] = other[key]
        else:
            for key in other:
                self[key].fill_blanks(other[key])

    def copy(self):
        """Return a copy of ``self``."""
        new = self.__class__(depth=self.depth)
        if self.depth == 1:
            for key in self:
                new[key] = self[key]
        else:
            for key in self:
                new[key] = self[key].copy()
        return new


def iter_modules(path, prefix):
    """Iterate over modules.

    :arg list path: List of paths to look for modules in.
    :arg str prefix: String to output on the front of every module name on output.
    """
    for module_finder, name, __is_pkg in pkgutil.walk_packages(path, prefix):
        if name in sys.modules:
            module = sys.modules[name]
        else:
            try:
                # I don't fully understand the following lines.
                # They are copied from the Python documentation:
                # https://docs.python.org/3.10/library/importlib.html#importing-a-source-file-directly
                spec = module_finder.find_spec(name)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                sys.modules[name] = module
            except ImportError as error:
                LOGGER.debug(f"[plugins] Could not load module {name}: {error}")
                continue
            except Exception as error:  #  pylint: disable=broad-except
                LOGGER.debug(f"[plugins] Ignoring module {name}: {error}")
                continue
        yield module


def read_config(filename, *args, **kwargs):
    """Open filename, and parse it as a :module:`configparser` configuration file."""
    config = configparser.ConfigParser(*args, **kwargs)
    with open(filename, encoding="utf8") as file:
        config.read_file(file, source=filename)
    return config


def cached_iterator(func):
    """Like :func:`functools.cache`, but for iterators.

    That is, the first time the function is run, the returned iterable is stored (as a tuple),
    and next calls to the function return this tuple.
    """

    @functools.wraps(func)
    @functools.lru_cache()  # Can be replaced by @functools.cache once python3.8 is obsolete
    def wrapped(*args, **kwargs):
        return tuple(func(*args, **kwargs))

    return wrapped
