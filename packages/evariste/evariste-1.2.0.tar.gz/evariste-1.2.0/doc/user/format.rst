.. _format:

String formatting
=================

In the :ref:`setup <setup>` and :ref:`per-file and per-directory configuration <evsconfig>` files, strings related to path are formatted by replacing part of the string by part of the file name. Using this, one can define a string which applies to *all* files (instead of having to rewrite the option for every single file).

See :meth:`evariste.tree.Tree.format` for the list of replacements.


.. note:: Implementation detail

   Right now, those strings are processed using :meth:`str.format`, and you might want to use some of rich features of the Python string formatting.
   However, this is only an implementation detail, and might change in the future without notice.
