.. _plugin_action_autocommand:

``action.autocommand`` — Compile file according to mime type or extension
=========================================================================

Like the :ref:`action.command <plugin_action_command>` plugin, this plugin is used to define which command should be used to compile some files.
But with this plugin, you can define several rules that will apply dependinng of the mime type or extension of the file to compile.

.. contents::
   :local:

Scope
-----

Commands defined in the :ref:`setup file <setup>` apply to the whole repository.
Commands defined in the :ref:`configuration file <evsconfig>` of a directory recursively apply to this directory.

Options
-------

Each rule is defined into its own section ``[action.autocommand.FOO]``.

Common options of :ref:`action plugins <plugin_action>` and options of :ref:`action.command <plugin_action_command>` also apply here (``strace``, ``command``, ``targets``). New options are:

- ``priority`` (50): If several rules apply to a file, the one with highest priority applies.
- ``extensions``: Space separated list of file extensions this rule should apply to.
- ``mimetypes``: Space separated list of mime types this rule should apply to.

Note that:

- if ``extensions`` and ``mimetypes`` are both set, the rule applies to files that match *either* of them.
- if neither ``extensions`` nor ``mimetypes`` are set, the end of the section is considered to be the extension (that is, a section ``[action.autocommand.ods]`` with no ``extensions`` or ``mimetypes`` option would apply to :file:`.ods` files).

Examples
--------

- Compile LaTeX files using ``latex+dvipdf``:

  .. code-block:: ini

     [action.autocommand.tex]
     targets = {basename}.pdf
     command =
         latex {basename}
         dvipdf {basename}

  .. note:: Shameless self-promotion

     If you have several LaTeX files that require different compilation tools, you might be interested in `SpiX <https://framagit.org/spalax/spix>`__, which reads the compilation chain that has been written into the :file:`tex` file itself.

- Convert `OpenDocuments <https://www.libreoffice.org/discover/what-is-opendocument/>`__ to PDF:

  .. code-block:: ini

     [action.autocommand.opendocument]
     mimetypes = application/vnd.oasis.opendocument.*
     extensions = fods fodt
     command = libreoffice --headless --convert-to pdf {filename}
     targets = {basename}.pdf

- Convert `Gimp <https://gimp.org>`__ files to ``png``:

  .. code-block:: ini

     [action.autocommand.xcf]
     command = echo "\
           (define (convert-xcf-to-png filename outfile) \
              (let* \
                 ( \
                    (image (car (gimp-file-load RUN-NONINTERACTIVE filename filename))) \
                    (drawable (car (gimp-image-merge-visible-layers image CLIP-TO-IMAGE))) \
                 ) \
                 (file-png-save RUN-NONINTERACTIVE image drawable outfile outfile 0 9 0 0 0 0 0) \
              ) \
           ) \
           (convert-xcf-to-png \"{filename}\" \"{basename}.png\") \
           (gimp-quit 0)" | \
           gimp -i -b -
     targets = {basename}.png
