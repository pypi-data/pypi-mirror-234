.. _plugin_renderer_text:

``renderer.text`` — Text renderer
=================================

At the end of compilation, display (in standard output) a tree to sum up the compilation: which files were successfully compiled, which were not…

.. code-block:: ini
   :caption: Example

   [renderer.text]
   enable = true
   color = true
   display = errors_or_all

Options
-------

The default value is given between parenthesis.

``color`` (``auto``)
  If ``True``, use color to draw the tree. If ``auto``, use color only if standard output is not piped or redirected.

``ascii`` (``False``)
  If ``True`` draw tree structure using only ASCII characters. Otherwise, use a wider set of characters.

``reverse`` (``False``)
  If ``True``, draw tree in reverse order.

``display`` (``all``)
  Define which files should be displayed at the end of compilation.

  ``all``
    Display all files.

  ``errors``
    Only display files when their compilation failed.

  ``errors_or_all``
    If some files did not compile successfully, only display those files. Otherwise, display all files.

