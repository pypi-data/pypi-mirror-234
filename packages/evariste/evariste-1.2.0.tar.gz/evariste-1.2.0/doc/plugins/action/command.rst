.. _plugin_action_command:

``action.command`` — Explicitly set the command to compile a file
=================================================================

Using this action plugin, one can explicitely set the command used to compile a file.

.. contents::
   :local:

.. note::

   Althought one can configure this plugin in the :ref:`setup file <setup>` or in the :ref:`configuration file <evsconfig>` of a directory, so that it applies to every single file of this repository or directory, you should probably use :ref:`plugin_action_autocommand` for this purpose.

Example
-------

Let's say file :file:`foo.tex` has the following configuration file :file:`foo.tex.evsconfig`.

.. code-block:: ini
   :caption: Example

   [action]
   plugin = command

   [action.command]
   targets = {basename}.pdf
   command =
     latex {basename}
     dvipdf {basename}.dvi {basename}.pdf

The ``plugin`` option in the ``[action]`` section means that this plugin is to be used to compile this file. Then, in the ``[action.command]`` section:

- the ``targets`` option gives the name(s) of the compiled file(s);
- the ``command`` option defines the shell command to use to compile this file.

Note that strings are :ref:`formatted <format>`.

.. _plugin_action_command_options:

Options
-------

Here are the options of this plugin:

- ``command`` (``""``): Command to run.
- ``strace`` (``"false"``): If true, the command is run using `strace <https://strace.io/>`__ to automatically find the dependencies of this file (the other files of this repository that are used to compile this file). Note that the compilation is slower, and this option is experimental.
- ``targets`` (``""``): Space-separated list of names of the compiled files. See :ref:`targets`.
- ``depends`` (``""``): Space-separated list of names of the files that are used to compile this file. See :ref:`depends`.

Example with :ref:`action.autocommand <plugin_action_autocommand>`
------------------------------------------------------------------

Imagine every single file of your repository is to be compiled with ``pdflatex``, excepted for that file :file:`foo.tex` that is to be compiled with ``latex+dvipdf``.
What you would do is:

- In the :ref:`setup file <setup>` (or the :ref:`configuration file <evsconfig>` of the root directory), use :ref:`action.autocommand <plugin_action_autocommand>` to specify that every LaTeX file should be compiled using ``pdflatex``:

  .. code-block:: ini
     :caption: evariste.setup

     [action.autocommand.latex]
     extensions = tex
     targets = {basename}.pdf
     command = pdflatex {basename}

- In the :ref:`configuration file <evsconfig>` of :file:`foo.tex` (that is: :file:`foo.tex.evsconfig`), explicitely set the command to compile this file:

  .. code-block:: ini
     :caption: foo.tex.evsconfig

     [action]
     plugin = command

     [action.command]
     command =
         latex {basename}
         dvipdf {basename}

Since the configuration file for :file:`foo.tex` has precedence over the other configuration files, or the setup file itself, this will do the trick.
