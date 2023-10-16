.. _setup:

Setup file
==========

The setup file contains:

- general configuration about how Évariste should handle this repository;
- configuration that is to be applied to every single file and directory (and that can be :ref:`overloaded later <evsconfig>`).

The file is parsed using :mod:`configparser`, you can use any feature of this module.

It is organized in sections (``setup``, ``renderer.text``, etc.), each section containing some options.

.. code-block:: ini

   [setup]
   source = .
   extends = foo.setup
   cachedir = .foo.cache
   libdirs =
       plugins1
       plugins2
   plugins =
       vcs.git
       renderer.text
       action.autocmd
       action.command

   [renderer.html.readme.mdwn]
   enable = yes

   [renderer.text]
   ascii = True

   [renderer.htmlplus]
   enable = yes
   destfile = public/index.html
   destdir = public
   staticdir = public/static

   [renderer.htmlplus.templatevar]
   title = My awesome title!
   lang = fr

``[setup]`` section
-------------------

The only mandatory section is ``[setup]``. Every other section is optionnal, and depends on which plugins are enabled. The options are:

- ``source``: The root of the directory that is to be processed by Évariste, absolute (starting with :file:`/` or relative to the directory of the setup file). Default is ``.`` (the same directory as the setup file).
- ``extends``: A list of configuration files. If set, Évariste first loads the first of those files, then the second (overwriting options that are already defined), then the third, and so on, and loads this file last. This can be useful if you have:
  - one setup file that setup up the compilation of files (that you want to perform on your home computer or USB key);
  - another file that is processed by the continuous integration system of your public hosting software, that extends the first one by adding the generation of an HTML page.
- ``cachedir``: The cache directory, if different from the default one.
- ``plugins``: The list of plugins to enable. Note that plugins can also be enabled individually: see :ref:`plugins`. This list must include exactly one :ref:`VCS plugin <plugin_vcs>`.
- ``libdirs``: The list of directories the plugins (as python files) are to be searched in: see :ref:`libdirs`.

.. _plugins:

Enabling plugins
----------------

There are two ways to enable plugins, which can be used at the same time.

- ``plugins`` option of the ``[setup]`` section:

  .. code-block:: ini

     [setup]
     plugins = foo bar baz

- ``enable`` option of the section of each plugin:

  .. code-block:: ini

     [foo]
     enable = true

Évariste includes several plugins; you can also :ref:`write your own <write>`. Those plugins are python files, that are searched in plugin directories: see :ref:`libdirs`.

Other sections
--------------

Each plugin can define its own sections (or read sections of other plugins).
Generally, a plugin ``foo`` will have a corresponding section, and might have other sections ``[foo.SOMETHING]``:

.. code-block:: ini

   [foo]
   bar = baz

   [foo.bar]
   toto = titi

   [foo.baz]
   tagada = tsoin tsoin
