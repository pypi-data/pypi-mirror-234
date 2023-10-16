.. _plugin_action_make:

``action.make`` — Compile file using a Makefile
===============================================

Compile file using a Makefile.

There is no automatic Makefile detection: you have to explicitely assign this action to a file.

Options
-------

- ``bin`` (``make``): Binary.
- ``options`` (``""``): Options to call ``make`` with.

For a given targe ``foo``, the command called is: ``{bin} {options} foo``.

.. code-block:: ini
   :caption: Example

   [action.make]
   bin = make
   options = -j3
