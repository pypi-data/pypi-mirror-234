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


"""Plugin base class and plugin loader

Every plugin is a subclass of :class:`Plugin` (see :ref:`write` for more information).

The :class:`Loader` class finds and loads the plugins.

Constants
---------

.. autodata:: MANDATORY_PLUGINS

:class:`Plugin`
---------------

.. autoclass:: Plugin
   :members:

:class:`Loader`
---------------

.. autoclass:: Loader
   :members: get_plugin, iter, values, items, applyiterhook, match

Functions
---------

.. autofunction:: find_plugins

Exceptions
----------

.. autoclass:: NoMatch

"""

import collections
import contextlib
import functools
import itertools
import logging
import os
import shlex
import sys
import typing

from .. import errors, hooks, setup, utils
from ..shared import Shared

LOGGER = logging.getLogger("evariste")

#: Set of mandatory plugins: plugins that are loaded by default, and cannot be disabled.
MANDATORY_PLUGINS = {
    "action.cached",
    "action.directory",
    "action.noplugin",
    "action.raw",
    "changed",
    "logging",
    "tree",
}


class NoMatch(errors.EvaristeError):
    """No plugin found matching ``value``."""

    def __init__(self, value, available):
        super().__init__()
        self.value = value
        self.available = available

    def __str__(self):
        return f"Value '{self.value}' does not match any of {self.available}."


class SameKeyword(errors.EvaristeError):
    """Two plugins have the same keyword."""

    def __init__(self, keyword, plugin1, plugin2):
        super().__init__()
        self.keyword = keyword
        self._plugins = (plugin1, plugin2)

    def __str__(self):
        # pylint: disable=line-too-long
        return f"""Plugins '{self._plugins[0].__name__}' and '{self._plugins[1].__name__}' have the same keyword '{self.keyword}'."""


class NotAPlugin(errors.EvaristeError):
    """Superclass of plugins is not a plugin."""

    def __init__(self, obj):
        super().__init__()
        self.obj = obj

    def __str__(self):
        return (
            """Class '{obj.__module__}.{obj.__name__}' is not a plugin """
            """(it should inherit from """
            """'{superclass.__module__}.{superclass.__name__}')."""
        ).format(obj=self.obj, superclass=Plugin)


class PluginNotFound(errors.EvaristeError):
    """Plugin cannot be found."""

    def __init__(self, keyword):
        super().__init__()
        self.keyword = keyword

    def __str__(self):
        return f"Cannot find plugin '{self.keyword}'."


@functools.total_ordering
class Plugin:
    """Plugin base: all imported plugins must be subclasses of this class.

    See :ref:`write` to see how to write a new plugin.

    :param Shared shared: The object :ref:`shared <shared>` among plugins.
    """

    # pylint: disable=too-few-public-methods

    #: Keyword plugin, used to reference it: it is used
    #: to :ref:`enable plugins in the setup file <plugins>`,
    #: to name its section in the :ref:`setup file <setup>`, etc.
    keyword: typing.Union[None, str] = None

    #: When Évariste has to choose *one* plugin among several one,
    #: it chooses the one with higher priority.
    priority: int = 0

    #: Default value for section ``self.keyword`` in the :ref:`setup file <setup>`.
    #: It may be overwritten by data provided by user in the :ref:`setup file <setup>`.
    #: See :ref:`default_setup`.
    default_setup: typing.Dict[str, str] = {}

    #: Default values for setup file. See :ref:`default_setup`.
    global_default_setup: typing.Dict[str, typing.Dict[str, str]] = {}

    #: Type of the plugin.
    #: Plugins of the same type gather some common behaviour.
    plugin_type: str = ""

    #: Iterable of plugins this plugin depends on.
    #: When this plugin is enabled, those plugins are enabled as well.
    depends: typing.Iterator[str] = ()

    def __init__(self, shared):
        #: Common data shared with every :class:`Tree` and :class:`~evariste.plugins.Plugin`
        #: of this :class:`~evariste.builder.Builder`.
        self.shared: Shared = shared

        #: Same as :attr:`Plugin.shared`, but from this plugin point of view:
        #: see :meth:`evariste.shared.Shared.get_plugin_view` and :ref:`plugin_local`.
        self.local = shared.get_plugin_view(self.keyword)

        self._set_default_setup()

    @classmethod
    def depends_dynamic(cls, shared) -> typing.Iterator[str]:
        """Iterator of plugins this plugin depends on (as an iterator of :class:`str`)

        When this plugin is enabled, those plugins are enabled as well.

        :param Shared shared: Shared object of the current builder.

        Warning: called before everything is settled down
        """
        # pylint: disable=unused-argument
        yield from ()

    def _set_default_setup(self):
        """Set default value for this plugin setup, if necessary."""
        default = setup.Setup()
        for parent in reversed(self.__class__.mro()):  # pylint: disable=no-member
            if hasattr(parent, "global_default_setup"):
                default.update(parent.global_default_setup)
            if hasattr(parent, "default_setup"):
                default.update({self.keyword: parent.default_setup})
        self.shared.setup.fill_blanks(default)

    def match(self, value, *args, **kwargs) -> bool:  # pylint: disable=unused-argument
        """Return ``True`` iff ``value`` matches ``self``.

        Default is keyword match.
        This method can be overloaded by subclasses.
        """
        return value == self.keyword

    def __lt__(self, other):
        priority = self.priority
        if callable(priority):
            priority = priority()  # pylint: disable=not-callable
        other_priority = other.priority
        if callable(other_priority):
            other_priority = other_priority()
        if priority == other_priority:
            return self.keyword < other.keyword
        return priority < other_priority


def find_plugins(
    libdirs: typing.Union[typing.Iterable[str], None] = None
) -> typing.Iterator[Plugin]:
    """Iterate over available plugins.

    :param typing.Iterable[str] libdirs:
        Additional iterable of directories where plugins can be found.
    """
    if libdirs is None:
        libdirs = []

    path = []
    path.extend(
        [
            os.path.join(utils.expand_path(item), "plugins")
            for item in [".evariste", "~/.local/evariste", "~/.evariste"]
        ]
    )
    path.extend([utils.expand_path(item) for item in libdirs])
    path.extend([os.path.join(item, "evariste") for item in sys.path])

    yielded = set()
    for module in utils.iter_modules(path, "evariste."):
        for attr in dir(module):
            if attr.startswith("_"):
                continue
            obj = getattr(module, attr)

            if isinstance(obj, type) and issubclass(obj, Plugin):
                if obj.keyword is None:
                    continue
                if obj in yielded:
                    continue
                yielded.add(obj)
                yield obj


def find_plugins_sorted(libdirs=None):
    """Like :fun:`find_plugins`, but returns a :class:`utils.DeepDict`.

    The returned object is a dictionary of dictionaries:
    - first keys are plugin types;
    - second keys are plugin keywords;
    - values are the only plugin of said type and said keyword.
    """
    plugindict = utils.DeepDict(2)

    for plugin in find_plugins(libdirs):
        if plugin.keyword in plugindict[plugin.plugin_type]:
            raise SameKeyword(
                plugin.keyword,
                plugin,
                plugindict[plugin.plugin_type][plugin.keyword],
            )

        plugindict[plugin.plugin_type][plugin.keyword] = plugin
    return plugindict


def get_libdirs(libdirs):
    """Convert `libdirs` setup option (as a string) to a list of path (as strings)."""
    if not libdirs:
        return []
    if isinstance(libdirs, str):
        return shlex.split(libdirs)
    if isinstance(libdirs, list):
        return libdirs
    return []


class Loader:
    """Load plugins

    :param evariste.shared.Shared shared: The :ref:`shared <shared>` object among plugins.

    The constructor (:meth:`Loader.__init__`):

    - reads the :ref:`setup file <setup>` (looking for the :ref:`libdirs <libdirs>` option);
    - search all plugins (subclasses of :class:`Plugin`);
    - instanciate:

      - the :const:`mandatory plugins <MANDATORY_PLUGINS>`,
      - those enabled in the :ref:`setup file <setup>`,
      - and their dependencies;

    - store them in some attribute, so that they can be accessed later.
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, *, shared):
        # pylint: disable=too-many-branches
        self.shared = shared

        # Load plugins:
        # Given the avaialble plugins, only loads relevant plugins.
        to_load = set()
        self.available = find_plugins_sorted(
            get_libdirs(self.shared.setup["setup"]["libdirs"])
        )

        # Step 0: Convert setup options in a list of keyword
        if self.shared.setup["setup"]["plugins"] is None:
            self.shared.setup["setup"]["plugins"] = []
        else:
            if isinstance(self.shared.setup["setup"]["plugins"], str):
                self.shared.setup["setup"]["plugins"] = shlex.split(
                    self.shared.setup["setup"]["plugins"]
                )
            elif isinstance(self.shared.setup["setup"]["plugins"], list):
                pass
            else:
                raise ValueError(
                    (
                        # pylint: disable=consider-using-f-string, line-too-long
                        "'Setup[setup][plugins]' should be a string or a list (is now {}: '{}')."
                    ).format(
                        type(self.shared.setup["setup"]["plugins"]),
                        self.shared.setup["setup"]["plugins"],
                    )
                )

        # Step 1: Add enabled plugins
        for keyword in self.shared.setup["setup"]["plugins"]:
            try:
                self.available.get_subkey(keyword)
            except KeyError as error:
                raise PluginNotFound(keyword) from error
            to_load.add(keyword)

        # Step 2: Enable/disable plugins according to their "enable" configuration
        for types in self.available.values():
            for plugin in types.values():
                if "enable" in self.shared.setup[plugin.keyword]:
                    if utils.yesno(self.shared.setup[plugin.keyword]["enable"]):
                        to_load.add(plugin.keyword)
                    elif plugin.keyword in MANDATORY_PLUGINS:
                        LOGGER.warning(
                            f"""Attemp to disable mandatory plugin "{plugin.keyword}" ignored."""
                        )
                        continue
                    else:
                        to_load.discard(plugin.keyword)

        # Step 3: Add default plugins
        to_load |= MANDATORY_PLUGINS

        # Step 4: Manage dependencies
        to_process = to_load.copy()
        processed = set()
        while to_process:
            keyword = to_process.pop()

            try:
                # Check if plugin exists
                self.available.get_subkey(keyword)
            except KeyError as error:
                raise PluginNotFound(keyword) from error

            for dependency in itertools.chain(
                self.available.get_subkey(keyword).depends,
                self.available.get_subkey(keyword).depends_dynamic(self.shared),
            ):
                try:
                    # Check if plugin exists
                    self.available.get_subkey(dependency)
                except KeyError as error:
                    raise PluginNotFound(dependency) from error
                if (dependency not in to_load) and (dependency not in processed):
                    to_load.add(dependency)
                    to_process.add(dependency)
            processed.add(keyword)

        # Step 5: Instanciate plugins
        self._plugins = collections.defaultdict(dict)
        self._hooks = collections.defaultdict(lambda: collections.defaultdict(set))
        for keyword in to_load:
            plugin = self.available.get_subkey(keyword)(self.shared)
            self._plugins[plugin.plugin_type][keyword] = plugin
            for hooktype, name, function in hooks.iter_hooks(plugin):
                self._hooks[hooktype][name].add(function)

    def values(
        self, plugin_type: typing.Optional[str] = None
    ) -> typing.Iterable[Plugin]:
        """Iterate over plugins.

        :param typing.Optional[str] plugin_type: See :meth:`Loader.iter`.
        """
        if plugin_type is None:
            for ptype in self._plugins:
                yield from self._plugins[ptype].values()
        else:
            yield from self._plugins[plugin_type].values()

    def applymethodhook(
        self, hookname: str, function: typing.Callable, *args, **kwargs
    ):
        """Apply a :ref:`method hook <methodhook>`.

        That is, run stuff before and after a method call.

        :param str hookname: Name of the hook to apply.
        :param function function: Function to which the hook is to be applied.
        :param list args: List of parameters to pass to hooks and ``function``.
        :param dict kwargs: Dictionary of parameters to pass to hooks and ``function``.
        """
        with contextlib.ExitStack() as stack:
            for hook in sorted(self._hooks["contexthook"][hookname], key=str):
                stack.enter_context(hook(*args, **kwargs))
            for hook in sorted(self._hooks["methodhook"][hookname], key=str):
                function = hook(function)

            return function(*args, **kwargs)

    def applyiterhook(self, hookname: str, *args, **kwargs) -> typing.Iterable:
        """Apply an :ref:`iteration hook <iterhook>`.

        Run every fonction hooked to this name (they should be iterators),
        and iterate over the chain of those iterators.

        :param str hookname: Name of the hook to apply.
        :param list arg: Positional arguments passed to the hooks.
        :param dict kwargs: Named arguments passed to the hooks.
        """
        for hook in sorted(self._hooks["iterhook"][hookname], key=str):
            yield from hook(*args, **kwargs)

    def get_plugin(self, keyword: str) -> Plugin:
        """Return the plugin with the given keyword.

        :raises NoMatch: If no (loaded) plugin was found with this keyword.
        """
        for plugin in self.values():
            if plugin.keyword == keyword:
                return plugin
        raise NoMatch(keyword, sorted(plugin.keyword for plugin in self.values()))

    def items(
        self, plugin_type: typing.Optional[str] = None
    ) -> typing.Iterable[typing.Tuple[str, Plugin]]:
        """Iterate over plugin keywords.

        :param typing.Optional[str] plugin_type: See :meth:`Loader.iter`.
        """
        for plugin in self.values(plugin_type):
            yield plugin.keyword

    def match(self, plugin_type: typing.Optional[str], value) -> Plugin:
        """Return the first plugin matching ``value``.

        A plugin ``Foo`` matches ``value`` if ``Foo.match(value)`` returns ``True``.

        :param typing.Optional[str] plugin_type: See :meth:`Loader.iter`.
        """
        for plugin in sorted(self.values(plugin_type), reverse=True):
            if plugin.match(value):
                return plugin
        raise NoMatch(value, sorted(self.iter(plugin_type)))

    def iter(
        self, plugin_type: typing.Union[str, None] = None
    ) -> typing.Iterable[Plugin]:
        """Iterate over keywords.

        :param typing.Optional[str] plugin_type: Type of the plugins to iterate over.

            - if ``None``, iterate over keywords of every (loaded) plugins;
            - else, iterate over keywords of plugins of this given type only.
        """
        if plugin_type is None:
            for ptype in self._plugins:
                yield from self._plugins[ptype]
        else:
            yield from self._plugins[plugin_type]
