Misc plugins
============

Some plugins that do not belong to any other category.

``copy`` — Copy files at the end of compilation
-----------------------------------------------

In the ``copy`` section of the :ref:`setup file <setup>`, each option starting with ``copy`` is a copy instruction: the first words are source paths, the last one is the destination path. All paths (source and destination) are relative to the directory of the setup file.

Consider the source path :file:`foo` and the destination path :file:`dest`.

- If the source is a file, it is copied into the destination: :file:`foo` is copied to :file:`dest/foo`.
- If the source is a directory, its content is copied into the destination: :file:`foo/bar` is copied to :file:`dest/bar`.

:meth:`Pattern matching <pathlib.Path.glob>` is performed to the source files:

- ``?``: a single character;
- ``*``: everything, excepted directory separators;
- ``**``: everything, including directory separators;
- ``[seq]`` any characteur in ``seq``.

.. code-block:: ini
   :caption: Example

   [copy]
   copy_foo = foo* bar baz
   copy_toto =
     toto
     titi*
     tata

.. _plugin_debug_hooks:

``debug.hooks`` — Print hook calls
----------------------------------

This plugins can help :ref:`writing new plugins <write>`:
it prints to standard output each :ref:`hook <hooks>`, and a few more things.
