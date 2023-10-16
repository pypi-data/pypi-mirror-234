.. _plugin_vcs:

VCS plugins
===========

Those plugins defines which files should be considered by Évariste.

``vcs.fs`` — Process any file of the file system
------------------------------------------------

Consider every file.

``vcs.git`` — Only process files handled by git
-----------------------------------------------

Only consider files handled by git. This prevents writing tedious :ref:`evsignore <evsignore>` files to ignore compiled files, while those are typically ignored by git itself.

``vcs.none`` — Do not process any file
--------------------------------------

This plugin is used in tests. I do not see why it would be useful to you, but who knows?

