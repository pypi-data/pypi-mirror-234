.. _evs:

`evs` tools
===========

Some helpers tools are installed together with Évariste.
They are mostly meant to be used by developers (of Évariste, or plugins) rather than end users.

.. contents::
   :local:

`evs cache` — Cache management
------------------------------

Using this tool, one can display, explore, or clean cache.

`evs plugins` — Plugin management
---------------------------------

Using this tool, one can display the list of available plugins.

`evs compile` — Run Évariste
----------------------------

The ``evariste`` binary is actually a shortcut to this subcommand.

.. _write_evs:

Write your own
--------------

If you want to write your own ``evs`` tool, simply place an executable file named ``evs-foo`` in a directory of the ``PATH`` shell variable. It will be called when calling ``evs foo``, with the same command line arguments.
