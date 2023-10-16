* evariste 1.2.0 (2023-10-07)

    * Python3.12 support.

    -- Louis Paternault <spalax@gresille.org>

* evariste 1.1.0 (2022-10-13)

    * Logging plugins (closes #39):
        * New logging plugins:
          - auto: rich or stdlib, depending if the output is a tty;
          - rich: colors and progress bar;
          - quiet: nothing;
          - stdlib: use stdlib logging module.
        * Logging plugin can be choosen in the configuration file.
        * Logging format can be set in the configuration file.
        * Fixed: Total number of files to compile was wrong.
    * Plugins
        * Added a ``Plugin.depends_dynamic`` method, so that plugins can declare dependencies that are computed at compilation time.

    -- Louis Paternault <spalax@gresille.org>

* evariste 1.0.1 (2022-03-21)

    * Fix bug: update cache version.

    -- Louis Paternault <spalax@gresille.org>

* evariste 1.0.0 (2022-03-09)

    * Python support
        * Drop python3.7 support.
        * Add Python3.11 support.
    * plugins
      * [renderer.htmlplus] Fix a missing space before open parenthesis.
      * [action.autocmd] Rename `action.autocmd` to `action.autocommand`.
      * [debug.hooks] New plugin "debug.hooks".
      * [vcs] Every path is a `pathlib.Path` object.
    * evs
      * evs plugins
        * Do not fail if plugin has no docstring.
    * Core
      * Introduce an `iterhook` mechanism.
      * Turn hook mechansim from classes and attributes to decorators.
      * Refactor renderer mechanism (remove the mandatory Renderer class).
      * Refactor README processing (they are now part of the Jinja2Renderer class instead of a core feature).
      * Minor core refactoring and improvement.
    * User
      * Clean and improve syntax of .evsignore files (closes #78).
      * Write user documentation (closes #9).
      * Rename setup option `enable_plugins` to `plugins`.

    -- Louis Paternault <spalax@gresille.org>

* evariste 0.4.0 (2021-12-04)

    * Add Python3.10 support.
    * Update dependency: jinja2>=3
    * Fix bug where `.evsignore` files not in the root directory were incorrectly processed.
    * Turn the ContextHook "compilefile" into a MethodHook "File.compile".
    * Add a hint if asked action plugin is available but not enabled.
    * Replace deprecated load_module() with exec_module().
    * [logging] Add progress to standard output.
    * [htmlplus] Add a template variable name for the favicon.

    -- Louis Paternault <spalax@gresille.org>

* evariste 0.3.1 (2020-06-25)

    * Core
        * Replace `pathlib.PosixPath` with `pathlib.Path`.
    * Command line
        * Command line arguments can no longer be defined in the setup file (this was a design mistake).
    * Setup file
        * Path of extended setup file is relative to directory of current setup file.
    * Installation
        * Add missing data file in release files.

    -- Louis Paternault <spalax@gresille.org>

* evariste 0.3.0 (2020-06-03)

    * Supported python versions
      * Drop python3.4, python3.5, python3.6 support.
      * Add python3.7 and python3.8 support.
    * Core (visible to users)
      * Configuration files can have arbitrary names (closes #50).
      * Configuration of directories can be recursive or not (closes #82).
      * A setup file can inherit (extend) other setup files (closes #71).
    * Core (invisible to users)
      * `evariste.tree.Root` can (should) be called as a with context.
      * Improve (clean) how plugins are defined and loaded.
      * Remove use of `functools.lru_cache` : When using several different builders, cache was shared between those builders (which is wrong: each builder is independant).
      * Various method and context hooks improvements.
      * Remove a lot of useless classes (either replaced with functions, merged with other classes, or replaced with stdlib classes).
    * Plugins
      * Loading
        * Remove `setup.disable_plugins` option.
        * Remove `goodstuff` plugin.
        * Remove `suggested` plugins.
        * Plugins can be loaded using "enable=true/false" in their configuration section (closes #72).
      * Actions
        * Generic
          * Actions can produce zero, one or several files (closes #83).
          * Any file can have a `depends` option in the `action` section.
          * Exceptions during file compilation are nicely caught (and error stack is stored as the compilation log).
          * When no suitable plugin be found to compile a file, use a fake plugin instaed (which will appear as a compilation error on the report).
        * autocmd
          * Configuration can be set in .evsconfig files, not only in main setup file.
        * command
          * Targets are now formatted using tree variables (basename, etc.).
          * Fix automatic dependecy finder using strace (which was broken).
          * Allow ONE command (which can be a script shell) instead of several commands.
        * latex:
          * Remove this plugin (use the command plugin while calling `latex` directly, or any latex compilation tool like `latexmk` or `arara` instead).
        * make
          * Target is now relative to currenrt directory
      * Renderer
        * html: Fix wrong links and error message when compilation fails
        * html: Remove unit from image size (was not valid HTML)
        * html and htmlplus: Simplify templates.
        * htmlplus: Add a missing default value for `setup.staticdir`.
        * htmlplus: Rename template variables "beforetree" and "aftertree" to "header" and "footer".
        * htmlplus: Generate valid HTML5 code
      * vcs.git
        * Simplify (and make faster?) the function that get last git modification time of versionned files
    * Command line
      * Add an `evs plugins` command (closes #16).
      * `python -m evariste` works again (closes #80).
    * Tests
      * Clean test of command line calls.
      * Add new tests of command line calls.
    * Installation
      * Replace (most of) setup.py with setup.cfg
      * Various minor setup improvements

  -- Louis Paternault <spalax@gresille.org>

* evariste 0.2.2 (2017-11-25)

    * Plugins
        * Actions
            * command: Add an `strace` option, to enable/disable strace
              profiling (to automatically set file dependencies). This can
              be enabled/disabled separately for each file.
        * Renderers
            * html and htmlplus: Add current date to the generated html
              code.

    -- Louis Paternault <spalax@gresille.org>

* evariste 0.2.1 (2017-08-25)

    * Core
        * `.evsignore` files now accepts comments (starting with #) and
          blank lines.
        * Syntax errors in `.evsignore` files are now nicely catched.
    * Plugins
        * Renderer
            * htmlplus: Add option `display_log` (decide wether logs are
              displayed always, never, only when compilation fails).

    -- Louis Paternault <spalax@gresille.org>

* evariste 0.2.0 (2017-07-27)

    * Installation
        * Various setup improvements.
    * Core
        * Add python3.6 support.
        * Change python library used to interact with git repository (was
          pygit2; is now gitpython).
        * Configuration files are now read in unicode; files are now
          written in unicode.
        * Deleting an empty cache is allowed.
        * Improve changelog formatting
        * hooks: Refactor context managers (closes #64)
    * Command line
        * Binaries are written in `__main__.py` modules, and can be called
          using `python -m evariste.MY.MODULE`.
        * The `evariste` binary is now an alias for `evs compile` (closes
          #63).
        * Catch errors in CLI arguments (closes #65).
        * Raise a nice error when no subcommand is provided (closes #56).
    * Plugins
        * Improve plugin API (closes #55).
        * Actions
            * autocmd: New plugin (closes #23).
            * command: Internal simplification and improvements.
            * make: New plugin (closes #33).
        * VCS
            * Only one VCS plugin can be enabled at a time (closes #61).
            * fs: New plugin (closes #41).
            * git: Speed file analysis.
        * Renderers
            * text:
                * Add option `reverse` (closes #66).
                * Add option `display` (closes #62).
            * htmlbox:
                * Renamed to `htmlplus`, with better CSS and javascript.
                * Set `page.tmpl` as the default template (closes #67).
                * Add an easy way to customize templates (closes #68).
                * Compilation log is now displayed (closes #18).
            * html.readme.mdwn: New plugin (closes #74).
    * Tests
        * More tests.
        * Use continuous integration (gitlab-CI).

    -- Louis Paternault <spalax@gresille.org>

* evariste 0.1.0 (2015-08-17)

    * Licence: Switched from GPL to AGPL.
    * Various setup.py improvements
    * Core
        * Python 3.5 support
        * Implemented multiprocessing
        * Sanitize the way path are handled
        * Many many internal fixes and improvements.
        * Now uses pygit2 version 0.22
    * Plugins
        * Improved management and loading
        * Added hooks
        * Improved selection (enable/disable setup options, default and
          required plugins, dependencies).
        * Renderers
            * htmllog: Removed draft. Will be addded later.
            * htmlplus: New html renderer, with CSS.
            * html: Various improvements.
            * text: New simple text renderer.
        * VCS
            * Git: Improved support (submodules, files added but not
              committed, code speed, etc.)
        * Actions
            * LaTeX: Various improvements.
            * Raw: Changed default behavior. By default, everything is
              rendered.
            * Command
                * Fixed bugs with shell commands (quotes and ampersands
                  are now supported)
                * Merged command and multicommand actions into command
    * Command line
        * Compilation is independent from current working directory
        * Added -j and -B options
        * Default value for arguments can be set in setup file
    * Tests
        * Wrote tests. Will be completed in next version.
    * Documentation
        * Wrote draft
    * evs tools
        * New evs tool
        * New evs-cache tool

    -- Louis Paternault <spalax@gresille.org>

* evariste 0.0.0 (2015-03-20)

    * First published version. Works, but with few options, and no
      documentation.

    -- Louis Paternault <spalax@gresille.org>
