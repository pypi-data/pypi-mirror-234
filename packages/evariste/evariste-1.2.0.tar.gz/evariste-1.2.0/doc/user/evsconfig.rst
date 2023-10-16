.. _evsconfig:

Per-file and per-directory configuration files
==============================================

The :ref:`setup file <setup>` applies to every single file and directory of the source directory.
You might wants more granular settings.

.. _evsconfig_precedence:

File precedence
---------------

The deepest the configuration file, the more precedence it has. For instance, consider a file :file:`foo/bar/baz.odt`. The list of setup and configuration files that apply (in that order) are:

- the :ref:`setup file <setup>`;
- :file:`.evsconfig`;
- :file:`foo/.evsconfig`;
- :file:`foo/bar/.evsconfig`;
- :file:`foo/bar/baz.odt.evsconfig`.

Note that if :file:`foo/bar/baz.odt.evsconfig` is defined, other files are not discarded: they all are merged together, and if an option is defined in several files, the precedence order defined above applies.

Per-directory setting
---------------------

The configuration set up in a :file:`.evsconfig` file in a directory applies to this directory, and every file and directory included in it.
To make it apply to this directory only, use the ``recursive`` option:

.. code-block:: ini

   [setup]
   recursive = false

Per-file setting
----------------

For any file :file:`foo.bar`, you can define some setting that apply to this file and this file only in configuration file :file:`foo.bar.evsconfig` or :file:`.foo.bar.evsconfig`.

On configuration file names
---------------------------

Configuration files can have arbitrary names. If they contain a ``source`` option in the ``setup`` section, then this is considered to be the name (relative to the directory of this configuration file) that this configuration applies to.

For instance, if file :file:`foo/bar/baz.evsignore` contains:

.. code-block:: ini

   [setup]
   source = ../toto/titi.txt

Then the configuration in this file applies to file :file:`foo/bar/../toto/titi.txt`, that is :file:`foo/toto/titi.txt`.

Using this feature, one can define *both* a recursive and non-recursive configuration for the same directory.
