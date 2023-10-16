.. _write_action:

Write action plugins
====================

.. currentmodule:: evariste.plugins.action

An action plugin is a subclass of :class:`Action`, that must interpret its :func:`abstract methods <abc.abstractmethod>`.

Selection
---------

An action plugin has an :meth:`~Action.match` method and a :attr:`~evariste.plugins.Plugin.priority` attribute.
To choose which action plugin it should use to compile a :file:`foo` :class:`file <evariste.tree.File>`, Évariste looks for the action plugin with the highest priority, that matches the file (that is: ``myplugin.match(foo)`` returns True).
The algorithms looks like the following:

.. code-block:: python
   :caption: Algorithm to choose the action plugin used to compile a :file:`foo` file.

   # Plugins are sorted by their priority attribute
   for plugin in sorted(LIST_OF_ACTION_PLUGINS, reverse=True):
       if plugin.match(foo):
           return plugin

Threads
-------

The :meth:`~Action.compile` action must be thread safe. If not, a :class:`~threading.Lock` is shared by every action plugin (as attribute :attr:`~Action.lock`).

.. code-block:: python
   :caption: Example of usage of :attr:`~Action.lock`

   def compile(self, path):
       # Thread safe part
       foo()

       with self.lock:
           # Non thread-safe part
           bar()

       # Thread safe part
       baz()

