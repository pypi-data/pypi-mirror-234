.. _write:

Write your own plugin
=====================

.. currentmodule:: evariste.plugins

Minimum example
---------------


A plugin is a subclass of :class:`Plugin`.
Define such a class in a python file located in :ref:`the right directory <libdirs>`.

.. code-block:: python

   from evariste import plugins

   class Foo(plugins.Plugin):
       """Example plugin"""

       keyword = "foo"

The only mandatory attribute or method is the :attr:`keyword` attribute, which must be unique. It will be used to enable your plugin in the setup file.

That's it! You can now enable it in the :ref:`setup file <setup>`:

.. code-block:: ini

   [setup]
   plugins = foo

You are now a proud owner of a plugin that does… nothing.
To interact with Évariste, you can:

- implement some :ref:`hooks <hooks>`;
- for some plugin types, implement some methods (see for instance :ref:`plugin_vcs` or :ref:`plugin_action`).

Of cours, your plugin can do everything listed above, at once.

Attributes
----------

Several useful attributes are defined for every :class:`~Plugin` instance; they are defined in the class documentation. The most complex one are :attr:`Plugin.shared` and :attr:`Plugin.local`.

.. _shared:

:attr:`Plugin.shared`
"""""""""""""""""""""

This attribute is a :class:`~evariste.shared.Shared` instance, shared among every :class:`Plugin` and :class:`~evariste.tree.Tree` object. It has three attributes, which are all :class:`~evariste.shared.DeepDict` instances (in the following examples, ``shared`` is an instance of :class:`~evariste.shared.Shared`):

- :attr:`~evariste.shared.Shared.setup` is a representation of the :ref:`setup file <setup>`. For instance, option ``bar`` of section ``foo`` can be read (and set) as ``shared.setup["foo"]["bar"]``.
- :attr:`~evariste.shared.Shared.plugin` is a :class:`~evariste.shared.DeepDict` where each plugin can store data that is cached, and accessible from other plugins. Plugin ``foo`` can set ``shared.plugin["foo"]`` at whatever value it wants. Technically, you can get and set values for other plugins, but think twice before doing so: do the other plugin expect you to get and set its data?
- :attr:`~evariste.shared.Shared.tree` is a :class:`~evariste.shared.DeepDict` where each plugin can store data about tree instances that is cached, and accessible from other plugins. Plugin ``foo`` can set whatever information its want about :class:`~evariste.tree.Tree` instance ``tree`` in ``shared.tree[tree]["foo"]``.

Data that is set in :class:`~evariste.shared.Shared` attributes :attr:`~evariste.shared.Shared.plugin` and :attr:`~evariste.shared.Shared.tree` is :mod:`pickled <pickle>` so make sure data you save there are *picklable*.

.. _plugin_local:

:attr:`Plugin.local`
""""""""""""""""""""

Most of the time, your plugin will only access its own section in the :ref:`setup file <setup>`, or in the other attributes of the :ref:`shared` attribute. To make things easier, the very same data is also available in :attr:`Plugin.local`. Let's consider an instance ``foo`` of a plugin ``foo``

- ``foo.local.setup`` is a dictionary of the options of ``foo`` in the :ref:`setup file <setup>`: ``foo.local.setup`` is a shortcut for ``foo.shared.setup["foo"]``.
- ``foo.local.plugin`` is a shortcut for ``foo.shared.plugin["foo"]`` (cached data for this plugin).
- Given a :class:`~evariste.tree.Tree` object ``mytree``, then ``foo.local.tree[mytree]`` is a shortcut for ``foo.shared.tree[mytree]["foo"]``.

.. _default_setup:

:attr:`Plugin.default_setup` and :attr:`Plugin.global_default_setup`
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

For any plugin, attributes :attr:`Plugin.default_setup` is default setup of the section :attr:`Plugin.keyword`, while :attr:`Plugin.global_default_setup` is the whole default setup (for all sections).

When reading the setup file, options that are not set are filled with options of :attr:`Plugin.default_setup`, and sections that are not set are filled with sections of :attr:`Plugin.global_default_setup`.

For instance, consider the following plugin:

.. code-block:: python

   class Foo(Plugin):
       keyword = "foo"
       default_setup = {
           "foo1": "default1",
           "foo2": "default2",
           }
       global_default_setup = {
           "bar": {
               "bar1": "global1",
               "bar2": "global2",
               },
           "foo": {
               "foo1": "global1",
               "foo3": "global3",
               },
           }

Now, this plugin is loaded with the following :ref:`setup file <setup>`:

.. code-block:: ini

   [setup]
   plugins = foo

   [foo]
   foo2 = setup2
   foo4 = setup4

   [bar]
   bar1 = setup1
   bar3 = setup3

Then, once the setup file, and both :attr:`Plugin.default_setup` and :attr:`Plugin.global_default_setup` has been taken into account, the resulting setup is equivalent to:

.. code-block:: ini

   [setup]
   plugins = foo

   [foo]
   foo1 = default1
   foo2 = setup2
   foo4 = setup4

   [bar]
   bar1 = setup1
   bar2 = global2
   bar3 = setup3

Notice that:

- whatever have been set in the setup file is kept;
- options of :attr:`Plugin.default_setup` and :attr:`Plugin.global_default_setup` may be overwritten by the setup file;
- whole sections of :attr:`Plugin.global_default_setup` may be overwritten by the section of :attr:`Plugin.default_setup`.


        

Current working directory
-------------------------

Note that as early as possible, the working directory is changed to the directory of the setup file given in argument to :ref:`evariste <evariste>`.

Interacting with Évariste
-------------------------

.. toctree::
   :maxdepth: 2

   write/hooks
   write/action
   write/renderer
   write/vcs

Note that it is also possible to write :ref:`evs plugins <write_evs>`.
