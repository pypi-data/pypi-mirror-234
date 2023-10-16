.. _plugin_renderer_html:

``renderer.html`` — HTML renderer
=================================

This plugin renders the repository as an HTML tree with annotated files, both as source and compiled. Note that you might want to use :ref:`renderer.htmlplus <plugin_renderer_htmlplus>` instead.

.. contents::
   :local:

Options
-------

Options are defined in section ``renderer.html`` of the :ref:`setup file <setup>`. The :ref:`options of any jinja2 plugin <jinja2_options>` also apply, and this plugin also defines:

.. code-block:: ini
   :caption: example

   [renderer.html]
   destfile = index.html
   destdir = html
   href_prefix = html/

- ``destfile`` (``"index.html"``) : Destination file.
- ``destdir`` (``"html"``) : Destination directory: the source and compiled files will be copied there (respecting the tree structure of the original repository).
- ``href_prefix`` (``""``) : This string is added at the beginning of each link to the source and compiled files in the destination file.
- ``template`` (``"tree.html"``) : The name of the template used to render the tree. The default templates is only an HTML list. If you want a full HTML page, see :ref:`plugin_renderer_htmlplus`.

Some template variables can also be defined in the setup file. See :ref:`html_templatevar`.

.. _html_template:

Template
--------

The template variables defined in any Jinja2 renderer are available in any HTML template as well.
See :ref:`jinja2_template`.

.. _html_templatevar:

Template variables
------------------

The ``templatevar`` mechanism defined for any Jinja2 renderer are available in any HTML template as well.
See :ref:`jinja2_templatevar`.

.. _plugin_renderer_html_file:

File plugins
------------

Every single file is not rendererd the same way. You can enable plugins to configure this.

``renderer.html.file.default`` — Default file renderer
""""""""""""""""""""""""""""""""""""""""""""""""""""""

This plugin is enabled by default.

``renderer.html.file.image`` — Render images
""""""""""""""""""""""""""""""""""""""""""""

This plugins displays a thumbnail of the image next to its name.

.. _plugin_renderer_html_readme:

Annotation: README plugins
--------------------------

READMEs can be written in several languages.

``renderer.html.readme.html`` — HTML README renderer
""""""""""""""""""""""""""""""""""""""""""""""""""""

Given a file :file:`foo`, a :file:`foo.html` will be pasted raw as its annotation.

``renderer.html.readme.mdwn`` — Markdown README renderer
""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Given a file :file:`foo`, a :file:`foo.md` or :file:`foo.mdwn` will be rendered as its annotation.

``renderer.html.readme.rst`` — RestructuredText README renderer
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Given a file :file:`foo`, a :file:`foo.rst` will be rendered as its annotation.
