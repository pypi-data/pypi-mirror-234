.. _plugin:

Plugins
=======

.. toctree::
   :maxdepth: 2

   plugins/mandatory
   plugins/action
   plugins/misc
   plugins/logging
   plugins/renderer
   plugins/vcs
   plugins/write

.. _libdirs:

Plugin paths
------------

Évariste looks fro new plugins (as python packages) in the following directories (this is relevant when :ref:`writing <write>` or installing new plugins):

- :file:`.evariste/plugins/foo.py` (relative to the directory of the setup file);
- :file:`~/.local/evariste/plugins/foo.py`
- :file:`~/.evariste/plugins/foo.py`
- :file:`LIBDIR/foo.py` (where :file:`LIBDIR` is any directory of the :ref:`libdirs <libdirs>` setup option).
