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

"""Cache

Implements a caching mechanism, to be able to store data between successive
runs of Évariste.
"""
import abc
import os
import pickle

from .errors import EvaristeError
from .shared import Shared, SharedDeepDict
from .utils import expand_path


class CacheError(EvaristeError):
    """Exception related to cache."""


class AbstractCache(metaclass=abc.ABCMeta):
    """Parent class of all cache classes."""

    #: Version of cache format. If the version read from cache is different
    #: from this, the cache is discarded.
    version = 4

    def __init__(self, *, setup, builder, **data):
        self.shared = Shared(setup=setup, builder=builder, **data)

    @abc.abstractmethod
    def close(self):
        """Close cache."""
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def clear(cls, cachedir):
        """Delete cache.

        :arg str cachedir: Cache directory.

        This is a class method, so that it can be called without the class
        being instanciated; i.e. cache can be deleted even if it is corrupted
        and cannot be loaded.
        """
        raise NotImplementedError


class NoCache(AbstractCache):
    """Fake cache: can be used if no cache is used."""

    def close(self):
        pass

    @classmethod
    def clear(cls, cachedir=None):
        pass


class Cache(AbstractCache):
    """Read cache."""

    dataname = ["tree", "plugin"]

    def __init__(self, cachedir, *, setup=None, builder=None):
        self.cachedir = expand_path(cachedir)
        os.makedirs(self.cachedir, exist_ok=True)

        data = {}

        if self._read_cache_version() == self.version:
            for base in self.dataname:
                data[base] = self._read_data(base)

        super().__init__(setup=setup, builder=builder, **data)

    def _read_cache_version(self):
        """Return cache version. Return 0 if an error occured."""
        try:
            with open(
                self._data_filename("version"), mode="r", encoding="utf8"
            ) as file:
                return int(file.read())
        except (ValueError, FileNotFoundError):
            return 0

    def close(self):
        """Close cache: write data"""
        for base in self.dataname:
            self._write_data(base, getattr(self.shared, base))
        with open(self._data_filename("version"), mode="w", encoding="utf8") as file:
            file.write(str(self.version))

    def _data_filename(self, base):
        """Return the filename corresponding to data ``base``."""
        return os.path.join(self.cachedir, f"{base}.data")

    def _read_data(self, base):
        """Read data ``base``, and return its content.

        If data could not be read, return a default value.
        """
        try:
            with open(self._data_filename(base), "rb") as file:
                return SharedDeepDict.from_attr(base, pickle.load(file))
        except (FileNotFoundError, ValueError, EOFError, pickle.PickleError):
            # File does not exist, or data is corrupted: provide default data.
            return SharedDeepDict.from_attr(base)

    def _write_data(self, base, data):
        """Write data `base`."""
        with open(self._data_filename(base), "wb") as file:
            pickle.dump(vars(data), file)

    @classmethod
    def clear(cls, cachedir):
        data = [
            os.path.join(cachedir, f"{base}.data")
            for base in ["version", "plugin", "tree"]
        ]
        try:
            for path in data:
                try:
                    os.remove(path)
                except FileNotFoundError:
                    pass
            try:
                os.rmdir(cachedir)
            except FileNotFoundError:
                pass
        except OSError as error:
            raise CacheError(f"Unable to delete '{error.filename}': {error}") from error


def open_cache(cachedir, setup, builder):
    """Return a cache object, possibly fake if `cachedir` is None."""
    if cachedir is None:
        return NoCache(setup=setup, builder=builder)
    return Cache(cachedir, setup=setup, builder=builder)
