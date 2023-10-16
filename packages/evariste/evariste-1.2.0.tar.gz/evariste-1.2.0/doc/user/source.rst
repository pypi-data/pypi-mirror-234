.. _source:

Source
======

In the :ref:`setup`, the ``source`` option of section ``[setup]`` defines the directory that is to be processed by Évariste.

.. contents::
   :local:
   :depth: 1

Configuration files
-------------------

To apply specitif configuration to a single file or directory, or to any subfile and subdirectory of a given directory, use: :ref:`evsconfig`.

.. _evsignore:

Ignore files
------------

You might want to ignore some files (no :ref:`compilation <plugin_action>`, nor :ref:`rendering <plugin_renderer>`). There are two ways of doing this.

Ignore one file
"""""""""""""""

For any file :file:`foo.bar`, if a file :file:`foo.bar.evsignore` or :file:`.foo.bar.evsignore` exists, then :file:`foo.bar` is ignored. The content of the :file:`*.evsignore` files here is not read: their mere existence is sufficient.

Ignore several files
""""""""""""""""""""

Patterns of file to ignore can be set in :file:`.evsignore` files in any directory.

- Each line contains a pattern of some files to ignore.
- Empty lines and line starting with ``#`` are ignored.
- Lines starting with ``/`` match absolute path, while line not starting with ``/`` match relative path. For instance, let us consider the following directory tree.

  .. code-block::

     + foo
       + bar
       + baz
         + bar

  In a file :file:`foo/.evsignore`, pattern ``/bar`` would ignore :file:`foo/bar` but not :file:`foo/baz/bar`, while ``bar`` would ignore both :file:`foo/bar` and :file:`foo/baz/bar`.
- In patterns:

  - ``*`` matches everything;
  - ``?`` matches any single character;
  - ``[seq]`` matches any character in seq;
  - ``[!seq]`` matches any character not in seq.

READMEs
-------

Annotation of files is implemented in the :ref:`HTML <plugin_renderer_html>` and :ref:`HTMLplus <plugin_renderer_htmlplus>` plugins.
