.. _write_renderer:

Write renderer plugins
======================

.. currentmodule:: evariste.plugins.renderer

Contrary to :ref:`action <write_action>` and :ref:`VCS <write_vcs>` plugins, renderer plugins are plain :class:`~evariste.plugins.Plugin`, that implement interesting stuff at the end of the :ref:`Builder.compile hook <hooks>`.

Jinja2 renderer
---------------

If you plan to write a renderer that write some file using the `jinja2 <https://jinja.palletsprojects.com>`__ module, you should probably subclass :class:`jinja2.Jinja2Renderer`.

HTML renderer
-------------

The :class:`~html.HTMLRenderer` is a subclass of :class:`~jinja2.Jinja2Renderer` (see above). If you want it to render files and README differently, you can write a file or README renderer, which are subclasses of :class:`~html.file.HtmlFileRenderer` and :class:`~html.readme.HtmlReadmeRenderer`.
