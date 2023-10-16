.. _plugin_renderer_htmlplus:

``renderer.htmlplus`` — HTML renderer, with a bit of CSS and javascript
=======================================================================

Like :ref:`plugin_renderer_html`, this plugin renders the repository as an HTML tree with annotated files, both as source and compiled.
The difference is that it adds a bit of CSS and javascript to make the end result nicer.

.. contents::
   :local:
   :depth: 1

Options
-------

Options are defined in section ``renderer.htmlplus`` of the :ref:`setup file <setup>`.

.. code-block:: ini
   :caption: example

   [renderer.htmlplus]
   destfile = index.html
   destdir = html
   href_prefix = html/
   display_log = no

The options of :ref:`plugin_renderer_html` also apply here. This plugin adds the following options.

- ``template`` (``"page.html"``): Name of the template to use to render the page. This option has the same meaning as the one in :ref:`plugin_renderer_html`, but the default value is different: by default, it renders a full HTML page (instead of some HTML code to be includede into an HTML page).
- ``staticdir`` (``"static"``): Directory (relative to the directory of the :ref:`setup file <setup>` where static files (CSS and Javascript files) should be copied at the end of compilation.
- ``display_log`` (``"errors"``): Defines what to do with compilation logs.
  - ``"yes"``: Include all logs. This can produce huge HTML pages.
  - ``"no"``: Do not include any log.
  - ``"errors"``: Only include logs of files when compilation failed.

Some template variables can also be defined in the setup file. See :ref:`html_templatevar`.

.. _htmlplus_template:

Template and template variables
-------------------------------

The :ref:`template variables <html_templatevar>` defined in the :ref:`HTML plugin <plugin_renderer_html>` are also defined here. Moreover, the following variables may be defined in the :ref:`setup file <setup>` to be included in the default :file:`page.html` template:

- ``lang``: Language of the page (to be included in the ``<html>`` tag as ``<html lang={{ lang }}>``).
- ``title``: Title of the page (as the ``title`` tag).
- ``favicon``: Link to the favicon.
- ``head``: Additionnal code to be included at the end of the ``<head>`` tag.
- ``header``: Some HTML code to be included in the body, before the tree.
- ``footer``: Some HTML code to be included in the body, after the tree. Default is some credit to Évariste.

All of them are optional.

.. code-block:: ini
   :caption: Example of template variables

   [renderer.htmlplus.templatevar]
   title = This is the value of the {{title}} jinja2 template variable.

File and README plugins
-----------------------

The :ref:`README plugins <plugin_renderer_html_readme>` and :ref:`file plugins <plugin_renderer_html_file>` of the :ref:`HTML renderer <plugin_renderer_html>` also work with this renderer.
