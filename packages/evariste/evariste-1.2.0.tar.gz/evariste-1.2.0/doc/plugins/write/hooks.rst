.. _hooks:

Hooks
=====

.. currentmodule:: evariste

Registering a method of your plugin as a hook means that this method will be called at a particular point during :ref:`evariste <evariste>` execution.

Hook types
----------

.. _methodhook:

Method hooks
""""""""""""

Method hooks are defined as decorator: they return a wrapped function, may (or may not) call the original function, and may (or may not) change the returned value.

.. code-block:: python
   :caption: Example of a method hook.

   @methodhook("File.make_archive")
   def make_archive(self, function):
       """Do something wile building archive"""

       @functools.wraps(function)
       def wrapped(tree, destdir):
           """Wrapped function."""
           # Do something before original function call.
           # Then call the original function.
           value = function(tree, destdir)
           # Do something after the original function call.
           # Maybe change the returnd value.
           return value

       return wrapped

.. _contexthook:

Context hooks
"""""""""""""

Most of the time, you want to use a method hook, without the hassle of defining a wrapped function (because you won't change the arguments or return value of the original function call). Any hook defined as a method hook can also be used as a context hook.

Your function must be a context manager (a :func:`contextlib.contextmanager` would make it even easier). Besides :obj:`self`, it is passed the arguments of the original function, and that original function is called between the :meth:`~object.__enter__` and :meth:`~object.__exit__` calls.

.. code-block:: python
   :caption: Example of a context hook

    @contexthook("Builder.compile")
    @contextlib.contextmanager
    def builder_compile(self, builder):
        # Do something before calling the original function

        # Call the original function
        yield

        # Do something after having called the original function

.. _iterhook:

Iteration hooks
"""""""""""""""

The last hook type are *iteration hooks*. Functions registered as such a hook must be iterators, and Évariste will aggregate all the item iterated by all functions registered as this hook.


.. code-block:: python
   :caption: Example of an iteration hook

   @iterhook("Tree.prune_before")
   def foo(self, tree):
       yield from self.bar(tree)


Chronological list of hooks
---------------------------

Here is the chronological list of hooks, that is, the list of the hooks, in the order in which they are called when running Évariste.

Just enable the :ref:`debug.hooks plugin <plugin_debug_hooks>` to print this list to standard output.

#. An instance of the plugin is created: :meth:`plugins.Plugin.__init__() <Plugin>`.
#. :class:`~tree.Tree` (:ref:`methodhook`): for every file and directory in the :ref:`repository <plugin_vcs>`, the :ref:`methodhook` ``Tree`` is called (:meth:`~object.__enter__` and :meth:`~object.__exit__`).
#. :meth:`Builder.compile.__enter__() <builder.Builder.compile>` (:ref:`methodhook`): About to build the tree.
#. ``Tree.prune_before()`` (:ref:`iterhook`): Methods must iterate files that will be pruned from the tree before file compilation (files and directories that won't be compiled, and won't appear in the final output). This method is called once for every file and directory of the tree. Argument: a :class:`~tree.Tree` object.
#. :meth:`File.compile.__enter__() <tree.File.compile>` (:ref:`methodhook`): About to compile the file. This method is called for every file in the repository. Note that file compilation is done in threads, so you don't know in which order files will be compiled.
#. :meth:`File.compile.__exit__() <tree.File.compile>` (:ref:`methodhook`): Done compiling the file. Same remarks as above.
#. ``Tree.prune_after()`` (:ref:`iterhook`): Methods must iterate files that will be pruned from the tree after file compilation (files and directories that may have been compiled, and won't appear in the final output). This method is called once for every file and directory of the tree. Argument: a :class:`~tree.Tree` object.
#. :meth:`File.make_archive.__enter__() <tree.File.make_archive>` (:ref:`methodhook`): About to build the archive of the current file and :ref:`its dependencies <depends>`. This hook is called once for every file in the repository.
#. :meth:`File.make_archive.__exit__() <tree.File.make_archive>` (:ref:`methodhook`): Done building the archive.
#. :meth:`Builder.compile.__exit__() <builder.Builder.compile>` (:ref:`methodhook`): Done building the tree.
#. :meth:`Builder.close.__enter__() <builder.Builder.close>` (:ref:`methodhook`): About to close the builder. This method is only called if compilation was successful.
#. :meth:`Builder.close.__exit__() <builder.Builder.close>` (:ref:`methodhook`): About to close the builder. See remark above.

Create your own hooks
---------------------

Method and Context hooks
""""""""""""""""""""""""

Defining a new method hook is done using the :func:`hooks.setmethodhook`.
The following example defines a context hook.

.. code-block:: python
   :caption: Definition of a context hook

   from evariste.hooks import setmethodhook

   class Foo:

       @setmethodhook()
       def bar(self, baz):
           bla_bla_bla()

Then, any plugin can register the method or context hook ``Foo.bar`` (class name dot method name, or class name only for the constructor) that will be called whenever method ``Foo.bar()`` is called.

Any method hook is also a context hook (and it is not possible to define a context hook that is not a method hook).

Iteration hooks
"""""""""""""""

Iteration hooks are defined using the :func:`plugins.Loader.applyiterhook` function (the :class:`plugins.Loader` instance being an attribute of the :class:`builder.Builder` one).

For instance, if a plugin contains the foolowing lines:

.. code-block:: python
   :caption: Definition of an iteration hook

   for item in self.shared.builder.plugins.applyiterhook("foo", bar):
       baz(bar)

Then, every method registered as an iteration hook ``foo`` will be called with the argument ``bar``, and whatever they iterate will be iterated in the *for* loop in this example.

