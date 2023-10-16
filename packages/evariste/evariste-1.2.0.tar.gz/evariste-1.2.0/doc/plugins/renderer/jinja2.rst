.. _plugin_renderer_jinja2:

``renderer.jinja2`` — :mod:`jinja2` renderer
============================================

This plugin is an abstract plugin:
it cannot be directly used, but several plugins with common features inherit from it.

This page describes those common features.

.. _jinja2_options:

Options
-------

Here are the common options to any plugin that is a subclass of this one.

- ``templatedirs`` : Additionnal directories where templates are being searched. By default, the following directories are used:

  - some directory containing the default templates of this plugin;
  - :file:`.evariste/templates` (relative to the directory of the :ref:`setup file <setup>`);
  - :file:`~/.config/evariste/templates`;
  - :file:`~/.evariste/templates`;
  - :file:`/usr/share/evariste/templates`.

- ``template``: The name of the template used to render the tree.

.. _jinja2_template:

Template
--------

The following template variables are defined:

- ``destdir``: Destination directory.
- ``shared``: ``shared`` data (see :attr:`evariste.builder.Builder.shared`).
- ``local``: Local reference to the shared data (see :meth:`evariste.shared.Shared.get_plugin_view`).
- ``sourcepath``: Source path of the repository.
- ``render_file``: Function that renders the :class:`file <evariste.tree.File>` given in argument (this functions uses the :ref:`file renderers <plugin_renderer_html_file>`).
- ``render_readme``: Function that renders the README of a file (this functions uses the :ref:`README renderers <plugin_renderer_html_readme>`).
- ``render_template``: Function that renders the template given in argument.
- ``templatevar``: Dictionary of template variables (see :ref:`jinja2_templatevar`).
- ``tree``: The :class:`~evariste.tree.Root` being rendered.

.. _jinja2_templatevar:

Template variables
------------------

It can be convenient to define template variables in the :ref:`setup file <setup>` (the :ref:`htmlplus <plugin_renderer_htmlplus>` plugins uses this). A dictionnary ``templatevar`` is available in the template, and contains the following items:

- ``date``: Compilation date.
- ``time``: Compilation time.
- ``datetime``: Compilation date and time.
- ``aftertree``: A credit line (with the date and Évariste version, and a link to the Évariste website).

It also contains any option that has been defined in the setup file, in the ``renderer.{keyword}.templatevar`` option (where ``keyword`` is the keyword of the plugin).

.. code-block:: ini
   :caption: Example of template variables for the HTML template

   [renderer.html.templatevar]
   title = This is the value of the <em>title</em> jinja2 template variable.
