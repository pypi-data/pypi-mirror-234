# Copyright Louis Paternault 2016-2022
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

"""Directory representation and compilation.

A :class:`Tree` is an abstract class representing a directory structure
(a directory with files and nested directories).
Its implementations are:

    - :class:`File`: a file;
    - :class:`Directory`: a directory;
    - :class:`Root`: the root directory being processed.

:class:`Tree`
-------------

.. autoclass:: Tree
   :members:

:class:`File`
-------------

.. autoclass:: File
   :members:

:class:`Directory`
------------------

.. autoclass:: Directory
   :members:
   :special-members: __iter__, __contains__, __getitem__, __delitem__

:class:`Root`
-------------

.. autoclass:: Root
   :members:

"""

# Can be removed starting with python3.11
from __future__ import annotations

import abc
import datetime
import functools
import itertools
import logging
import os
import pathlib
import shlex
import tarfile
import traceback
import typing
from concurrent.futures import ThreadPoolExecutor

from . import errors, plugins, utils
from .hooks import setmethodhook
from .plugins.action import DirectoryAction

if typing.TYPE_CHECKING:
    from .shared import Shared

LOGGER = logging.getLogger(__name__)


def get_tree_plugins(self, *args, **kwargs):
    """Given the argument of :method:`Tree.__init__`, return a :class:`Loader` instance."""
    # pylint: disable=unused-argument
    if isinstance(self, Root):
        root = self
    else:
        root = kwargs["parent"]
        while root.parent is not None:
            root = root.parent
    return root.shared.builder.plugins


@functools.total_ordering
class Tree(metaclass=abc.ABCMeta):
    """A file system tree.

    A directory, that contains files and has subdirectories.

    :param pathlib.Path path: Relative path (relative to the root of this tree).
    :param typing.Optional[Directory] parent: Directory containing this file or directory.

    """

    # pylint: disable=too-many-instance-attributes

    @setmethodhook(getter=get_tree_plugins)
    def __init__(
        self, path: pathlib.Path, *, parent: typing.Optional[Directory] = None
    ):
        #: Once the file has been :meth:`compiled <File.compile>`,
        #: the report (compilation log, if any) is saved here.
        self.report: typing.Union[plugins.action.Report, None] = None

        #: Parent directory (copied from constructor argument).
        self.parent: typing.Union[Tree, None] = parent

        #: Computed configuration for this file. See :ref:`evsconfig`.
        #: Note: This attribute is :class:`None` until :meth:`Tree.set_config` has been called.
        self.config: typing.Union[utils.DeepDict, None] = None

        if parent is not None:
            #: Name of the tree (path, relative to its :attr:`Tree.parent`).
            self.basename: pathlib.Path = pathlib.Path(path)

            #: Absolute path
            self.from_fs: pathlib.Path = parent.from_fs / self.basename

            #: Path, relative to the :class:`Root`.
            self.from_source: pathlib.Path = parent.from_source / self.basename

            #: VCS plugin
            self.vcs: plugins.vcs.VCS = self.parent.vcs

            #: Common data shared with every :class:`Tree` and :class:`~evariste.plugins.Plugin`
            #: of this :class:`~evariste.builder.Builder`.
            self.shared: Shared = self.parent.shared

        #: Same as :attr:`Tree.shared`, but from a tree point of view:
        #: see :meth:`~evariste.shared.Shared.get_tree_view`.
        self.local = self.shared.get_tree_view(path)

    def __hash__(self):
        return hash((hash(self.parent), self.from_fs))

    @property
    def relativename(self) -> pathlib.Path:
        """Return a *relative* name.

        * For root, return path relative to file system (or directory of setup file).
        * For non-root, return path relative to parent (i.e. basename of path).
        """
        if isinstance(self, Root):
            return self.from_fs
        return self.basename

    @staticmethod
    def is_root():
        """Return ``True`` iff ``self`` is the root."""
        return False

    @property
    def depth(self) -> int:
        """Return the depth of the path.

        The root has depth 0, and depth of each path is one more than the depth
        of its parent.
        """
        if isinstance(self, Root):
            return 0
        return 1 + self.parent.depth

    @property
    def root(self) -> Root:
        """Return the root of the tree."""
        if self.is_root():
            return self
        return self.parent.root

    def find(
        self, path: typing.Union[str, pathlib.Path, typing.Tuple[str]]
    ) -> typing.Union[Tree, False]:
        """Return the tree object corresponding to ``path`` if it exists; False otherwise.

        Argument can be:

        - a string (:class:`str`);
        - a :class:`pathlib.Path` object;
        - a tuple of strings, as a list of directories and (optional) final file.
        """
        if isinstance(path, str):
            pathtuple = [path]
        elif isinstance(path, pathlib.Path):
            pathtuple = path.parts
        else:
            pathtuple = path

        if not pathtuple:
            return self
        if pathtuple[0] in self:
            return self[pathtuple[0]].find(pathtuple[1:])
        return False

    def __str__(self):
        return self.from_fs.as_posix()

    def __eq__(self, other):
        return self.from_source == other.from_source

    def __lt__(self, other):
        if isinstance(self, Directory) and not isinstance(other, Directory):
            return True
        if not isinstance(self, Directory) and isinstance(other, Directory):
            return False
        return self.from_source < other.from_source

    def is_dir(self) -> bool:
        """Return `True` iff `self` is a directory."""
        return issubclass(self.__class__, Directory)

    def is_file(self) -> bool:
        """Return `True` iff `self` is a file."""
        return issubclass(self.__class__, File)

    def walk(self, dirs: bool = False, files: bool = True) -> typing.Iterable[Tree]:
        """Iterator over itself."""
        #  pylint: disable=unused-argument
        if files and self.is_file():
            yield self

    def count(self, dirs: bool = False, files: bool = True) -> int:
        """Count the number of files or directories in this tree."""
        return sum(1 for _ in self.walk(dirs, files))

    def prune(self, path: typing.Union[pathlib.Path, str, typing.Tuple[str]]):
        """Remove a file.

        Argument can be either:

        - a :class:`pathlib.Path`,
        - a :class:`tuple`,
        - or a :class:`str` (which would be converted to a :class:`pathlib.Path`.

        If called with a non-existing path, does nothing.
        """
        if isinstance(path, str):
            path = pathlib.Path(path)
        if isinstance(path, tuple):
            parts = path
        elif isinstance(path, pathlib.Path):
            parts = path.parts
        else:
            raise TypeError

        # Does path exist?
        if parts[0] not in self:
            return

        # Remove (existing) path
        if len(parts) == 1:
            del self[parts[0]]
        else:
            self[parts[0]].prune(parts[1:])

    def format(self, string: str) -> str:
        """Format given string, with several variables related to ``self``.

        Here are the replacements (with example :file:`/home/louis/repo/foo/bar.txt`):

        - ``{dirname}`` (:file:`/home/louis/repo/foo`): the name of the directory.
          Note that most of the time, this is useless, since when compiling a file,
          the working directory is the directory of this file (i.e. ``{dirname}``).
        - ``{filename}`` (:file:`bar.txt`): The file name (without directory).
        - ``{fullname}`` (:file:`/home/louis/repo/foo/bar.txt`): The file name (with directory).
        - ``{extension}`` (:file:`txt`): The extension (without the dot).
          If the file has several extensions (e.g. :file:`foo.tar.gz`),
          this is only the last one ``gz``.
        - ``{basename}`` (:file:`bar`): The file name, without directory and extension.
        """
        suffix = self.from_source.suffix
        if suffix.startswith("."):
            suffix = suffix[1:]
        return string.format(
            dirname=self.parent.from_fs.as_posix(),
            filename=self.basename,
            fullname=self.from_fs.as_posix(),
            extension=suffix,
            basename=self.basename.stem,
        )

    @abc.abstractmethod
    def full_depends(self) -> typing.Iterable[pathlib.Path]:
        """Iterate over all dependencies of this tree (recursively for directories)."""
        raise NotImplementedError()


class Directory(Tree):
    """Directory"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._subpath = {}

    def add_subpath(self, sub: typing.List[pathlib.Path]):
        """Add a path to the tree (relative to ``self``)."""
        if len(sub.parts) > 1:
            self[sub.parts[0]].add_subpath(pathlib.Path(*sub.parts[1:]))
        else:
            self[sub.parts[0]]  # pylint: disable=pointless-statement

    def __iter__(self) -> typing.Iterable[str]:
        """Iterate over subpaths (this function is not recursive)."""
        return iter(self._subpath)

    def keys(self) -> typing.Iterable[str]:
        """Iterator over subpaths (as :class:`str` objects)."""
        yield from self._subpath.keys()

    def values(self) -> typing.Iterable[Tree]:
        """Iterator over subpaths (as :class:`Tree` objects)."""
        yield from self._subpath.values()

    def __contains__(self, key: str) -> bool:
        """Return ``True`` if key (a single file name or directory) is in this directory."""
        return key in self._subpath

    def __getitem__(self, key: str) -> Tree:
        """Return subfile or subdirectory ``self.from_fs / key``.

        If it does not exist, it is created first.
        """
        if key not in self:
            if (self.from_fs / key).is_dir():
                path_type = Directory
            else:
                path_type = File
            self._subpath[key] = path_type(key, parent=self)
        return self._subpath[key]

    def __delitem__(self, item: str):
        """Remove a subfile or subdirectory.

        If, after deletion, ``self`` is an empty directory (and is not root),
        ``self`` is remove from its parent.
        """
        pathitem = pathlib.Path(item)
        if len(pathitem.parts) != 1:
            raise errors.EvaristeBug(
                "Argument '{}' should be a single directory or file, "
                "not a 'directory/directory' or directory/file'."
            )
        if str(pathitem) in self:
            del self._subpath[str(pathitem)]
            if (not self._subpath) and self.is_dir() and self.parent is not None:
                del self.parent[self.basename]

    def walk(self, dirs: bool = False, files: bool = True) -> typing.Iterable[Tree]:
        """Iterator over files or directories  of ``self``.

        :param bool dirs: If `False`, do not yield directories.
        :param bool files: If `False`, do not yield files.

        Directories are yielded *before* subfiles and subdirectories.
        """
        if dirs and self.is_dir():
            yield self
        for sub in sorted(self):
            yield from self[sub].walk(dirs, files)

    def compile(self):
        """Compile directory."""
        self.report = DirectoryAction(self.shared).compile(self)

    def full_depends(self) -> typing.Iterable[pathlib.Path]:
        for sub in self:
            yield from self[sub].full_depends()


class File(Tree):
    """A file"""

    @setmethodhook()
    def compile(self):
        """Compile file."""
        # pylint: disable=too-many-branches

        # Find a plugin to compile the file
        # pylint: disable=unsubscriptable-object
        try:
            if not self.shared.builder.plugins.get_plugin("changed").compile(self):
                # Nothing has changed: it is useless to compile this again.
                compiler = self.shared.builder.plugins.get_plugin("action.cached")
            elif self.config["action"]["plugin"] is not None:
                compiler = self.shared.builder.plugins.get_plugin(
                    f"""action.{self.config["action"]["plugin"]}"""
                )
            else:
                compiler = self.shared.builder.plugins.match("action", self)
        except plugins.NoMatch:
            compiler = self.shared.builder.plugins.get_plugin("action.noplugin")

        # Actual compilation
        try:
            self.report = compiler.compile(self)
        except Exception as error:  # pylint: disable=broad-except
            if isinstance(error, errors.EvaristeError):
                message = str(error)
            else:
                message = "Error: Evariste internal error\n\n" + traceback.format_exc()
            LOGGER.error(message)
            self.report = plugins.action.Report(
                self,
                success=False,
                log=message,
            )

        # Add (optional) dependencies to the file
        # pylint: disable=unsubscriptable-object
        for regexp in itertools.chain(
            shlex.split(self.config[compiler.keyword].get("depends", "")),
            shlex.split(self.config["action"].get("depends", "")),
        ):
            for name in self.parent.from_fs.glob(regexp):
                if name.resolve() != self.from_fs.resolve():
                    if name in self.vcs:
                        self.report.depends.add(name)

    @setmethodhook()
    def make_archive(self, destdir: pathlib.Path) -> pathlib.Path:
        """Make an archive of ``self`` and its dependency.

        Steps are:

        - build the archive;
        - copy it to ``destdir``;
        - return the path of the archive, relative to ``destdir``.

        If ``self`` has no dependencies, consider the file as an archive.

        It can be called several times: the archive will be built only once.
        """

        def common_root(files):
            """Look for the common root of files given in argument.

            Returns a tuple of `(root, relative_files)`, where
            `relative_files` is a list of `files`, relative to the root.
            """
            files = [
                file.resolve()
                for file in files
                if file.resolve()
                .as_posix()
                .startswith(self.root.from_fs.resolve().as_posix())
            ]
            root = pathlib.Path()
            while True:
                prefixes = [path.parts[0] for path in files]
                if len(set(prefixes)) != 1:
                    break
                prefix = prefixes[0]
                files = [file.relative_to(prefix) for file in files]
                root /= prefix
            return root.relative_to(self.root.from_fs.resolve()), files

        if (
            # Compilation was successful
            self.report.success
            # File has not been compiled again
            and not self.shared.builder.plugins.get_plugin("changed").compile(self)
            # Archive has already been generated
            and "archivepath" in self.shared.tree[self.from_source]["changed"]
        ):
            return self.shared.tree[self.from_source]["changed"]["archivepath"]

        if len(self.report.full_depends) == 1:
            utils.copy(self.from_fs.as_posix(), (destdir / self.from_source).as_posix())
            return self.from_source
        archivepath = self.from_source.with_suffix(f"{self.from_source.suffix}.tar.gz")
        os.makedirs(os.path.dirname((destdir / archivepath).as_posix()), exist_ok=True)

        archive_root, full_depends = common_root(self.report.full_depends)
        with tarfile.open((destdir / archivepath).as_posix(), mode="w:gz") as archive:
            for file in full_depends:
                archive.add(
                    (self.root.from_fs / archive_root / file).as_posix(),
                    file.as_posix(),
                )
        return archivepath

    def last_modified(self) -> datetime.datetime:
        """Return the last modified date and time of ``self``."""
        return self.vcs.last_modified(self.from_fs)

    def full_depends(self) -> typing.Iterable[pathlib.Path]:
        yield from self.report.full_depends

    def depends(self) -> typing.Iterable[pathlib.Path]:
        """Iterator over dependencies of this file (but not the file itself)."""
        yield from self.report.depends


class Root(Directory):
    """Root object (directory with no parents)."""

    def __init__(self, path, *, vcs=None, shared=None):
        self.vcs = vcs
        self.shared = shared
        self.from_fs = pathlib.Path.cwd() / path
        self.from_source = pathlib.Path(".")
        self.basename = pathlib.Path(".")
        super().__init__(path)

    @staticmethod
    def _config2file(config):
        """Given a config (with a name ending in '.evsconfig', return the corresponding tree.

        If no such file is found, raise ValueError.
        """
        if str(config.basename) == ".evsconfig":
            # Directory
            return config.parent

        # File
        # First try: `config` is SOMETHING.evsconfig and SOMETHING is in the tree
        if tree := config.parent.find(str(config.basename)[: -len(".evsignore")]):
            return tree
        # Second try: `config` is .SOMETHING.evsconfig and SOMETHING is in the tree
        if tree := config.parent.find(str(config.basename)[1 : -len(".evsignore")]):
            return tree

        raise ValueError()

    def _find_config(self):
        """Iterate over configuration files for directories"""
        for config in self.walk():
            if str(config).endswith("evsconfig"):
                content = utils.read_config(config.from_fs, allow_no_value=True)
                source = content.get("setup", "source", fallback=None)
                if source is None:
                    try:
                        tree = self._config2file(config)
                    except ValueError:
                        logging.warning(
                            f"Found a configuration file '{config}' with no related file. Processing it as a normal file."  # pylint: disable=line-too-long
                        )
                        continue
                else:
                    tree = self.find((config.parent.from_source / source))
                    if not tree:
                        logging.warning(
                            f"Configuration file '{config}' refer to a non-existent source '{source}'."  # pylint: disable=line-too-long
                        )
                        continue
                yield tree, config, content

    def set_config(self):
        """Compute the configuration of each file of the tree.

        That is:

        - look for the file that configure it
          (typically ``foo.evsconfig`` is the configuration for file ``foo``),
        - load it,
        - and complete it using the recursive configuration of parent directories.
        """
        recursive = {}

        # Assign configuration to files
        for tree, configname, configcontent in list(self._find_config()):
            if utils.yesno(configcontent.get("setup", "recursive", fallback=False)):
                recursive[tree] = configcontent
                self.prune(configname.from_source)
                continue

            tree = self.find(tree.from_source)
            if tree.config is not None:
                LOGGER.warning(  # pylint: disable=logging-fstring-interpolation
                    f"""Configuration file "{configname}" has been ignored for "{tree.from_fs}": another configuration file already applies."""  # pylint: disable=line-too-long
                )
                continue

            self.prune(configname.from_source)
            tree.config = utils.DeepDict.from_configparser(configcontent)

        # Propagate recursive configuration from directories
        for directory, config in sorted(recursive.items(), reverse=True):
            for tree in self.find(directory.from_source).walk(dirs=True, files=True):
                if tree.config is None:
                    tree.config = utils.DeepDict.from_configparser(config)
                else:
                    tree.config.fill_blanks(config)

        # Set a default (empty) configuration to trees without any.
        for tree in self.walk(dirs=True, files=True):
            if tree.config is None:
                tree.config = utils.DeepDict(2)

    @staticmethod
    def is_root() -> bool:
        return True

    def root_compile(self):
        """Recursively compile files.."""
        # Set and remove configuration files
        self.set_config()

        # Prune files that are no longer needed.
        for file in list(
            itertools.chain.from_iterable(
                self.shared.builder.plugins.applyiterhook("Tree.prune_before", tree)
                for tree in self.walk(dirs=True, files=True)
            )
        ):
            self.prune(file)

        # Compile files
        with ThreadPoolExecutor(
            max_workers=self.shared.setup["arguments"]["jobs"]
        ) as pool:
            for path in self.walk(dirs=False, files=True):
                pool.submit(path.compile)

        # Prune files that are no longer needed.
        for file in list(
            itertools.chain.from_iterable(
                self.shared.builder.plugins.applyiterhook("Tree.prune_after", tree)
                for tree in self.walk(dirs=True, files=True)
            )
        ):
            self.prune(file)

        # "Compile" directories
        for path in reversed(list(self.walk(dirs=True, files=False))):
            path.compile()

    @classmethod
    def from_vcs(cls, repository: plugins.vcs.VCS) -> Root:
        """Return a directory, fully set."""
        tree = cls(repository.source, vcs=repository, shared=repository.shared)
        for path in repository.walk():
            tree.add_subpath(path)
        return tree
