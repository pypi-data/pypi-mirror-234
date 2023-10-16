.. _plugin_renderer:

Renderer plugins
================

Renderer plugins define what should be done at the end of the compilation: :ref:`display something in the standard output <plugin_renderer_text>`, :ref:`build an HTML page <plugin_renderer_html>`, etc.
Some plugins are shipped with Évariste, but you can also :ref:`write your own <write_renderer>`.

.. toctree::
   :maxdepth: 1

   renderer/jinja2
   renderer/html
   renderer/htmlplus
   renderer/text
