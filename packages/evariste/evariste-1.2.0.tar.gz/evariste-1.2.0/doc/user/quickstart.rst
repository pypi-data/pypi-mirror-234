.. _quickstart:

Getting started
===============

You have a directory that you want to be processed using Évariste.

Minimal configuration file
--------------------------

Create a :file:`evariste.setup` file containing the following text:

.. code-block:: ini

  [setup]
  plugins = vcs.fs

Note that if your directory is a git repository, you can use ``vcs.git`` instead of ``vcs.fs``. That way, only files handled by git will be processed (more information about :ref:`vcs plugins <plugin_vcs>` and :ref:`setup files <setup>`).

That's it! You can now run ``evariste`` on this file::

  evariste evariste.setup

And nothing happens… You need to give Évariste to pieces of information:

- how files are to be compiled;
- what should be the output.

Compile file
------------

To actually compile files, you need to enable one or several :ref:`action plugins <plugin_action>` in the ``enable_plugin`` option of the configuration file (see first section).

Let's use the :ref:`action.command <plugin_action_command>` and :ref:`action.autocommand <plugin_action_autocommand>` plugins. Our setup file now looks like this:

.. code-block:: ini

   [setup]
   plugins =
       vcs.git
       action.command action.autocommand

   [action.autocommand.latex]
   extensions = tex
   targets = {basename}.pdf
   command =
     latex {basename}
     dvipdf {basename}

The ``action.command`` plugin is not used yet. The ``action.autocommand`` is used, and the ``action.autocommand.latex`` means: Every file with extension ``.tex`` will be compiled (in its directory) using command ``pdflatex {basename}`` (where ``{basename}`` is replaced with the base name of the file, that is, without directory or extension; more info in :ref:`format`), and will produce a ``{basename}.pdf`` file.

Now, that particular :file:`foo.tex` file must be compiled using ``lualatex``. Let's use the ``action.command`` plugin, and write a small configuration file for it. This file can be named either :file:`foo.tex.evsconfig` or :file:`.foo.tex.evsconfig`, and contains:

.. code-block:: ini

   [action]
   plugin = command

   [action.command]
   targets = {basename}.pdf
   command = lualatex {basename}

This means:

- for this file, and this file only, the ``action.command`` will be used;
- it will be compiled using the ``lualatex foo`` command.

Let's run ``evariste`` again, this time with the ``--verbose`` option::

  evariste evariste.setup --verbose

You can see that your latex files are correctly compiled.

More information, as well as the list of action plugins, can be found in :ref:`plugin_action`.

Output
------

Right now, nothing is displayed at the end of the compilation. Let's improve thit.

Text renderer
"""""""""""""

Let's enable the :ref:`renderer_text plugin <plugin_renderer_text>`. The ``[setup]`` section of your setup file now looks like this:

.. code-block:: ini

   [setup]
   plugins =
       vcs.git
       action.command action.autocommand
       renderer.text

And a tree is displayed at the end of the ``evariste evariste.setup`` call: it lists all the files that were compiled, with their status (success or failed compilation).

HTML renderer
"""""""""""""

Now you want to publish your directory as an HTML page like `this one <https://lpaternault.frama.io/cours-2-math/>`__. To do so, we simply enable the :ref:`renderer_html plugin <plugin_renderer_html>`.

.. code-block:: ini

   [setup]
   plugins =
       vcs.git
       action.command action.autocommand
       renderer.text renderer.html

Let's run ``evariste evariste.setup`` again, and *voilà!*, we get a :file:`index.html` file listing the files of our repository as a tree, linking to both as source (latex) and compiled (pdf) files.

This plugin can be configured (:ref:`plugin_renderer_html`), but you might prefer the :ref:`HTMLplus renderer <plugin_renderer_htmlplus>`, which add a bit of CSS and javascript to make the output nicer.

Conclusion
----------

Évariste is very configurable. There is a lot more to discover: :ref:`more options <setup>`, :ref:`configure and ignore files <source>`, several :ref:`action plugins <plugin_action>` or :ref:`renderer plugins <plugin_renderer>`, or :ref:`more <plugin>`.

Enjoy!
