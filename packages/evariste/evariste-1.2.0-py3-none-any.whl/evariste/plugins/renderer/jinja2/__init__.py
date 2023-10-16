# Copyright Louis Paternault 2015-2022
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Abstract class for jinja2 renderers.

See also :ref:`plugin_renderer_jinja2`.

.. autoclass:: Jinja2Renderer
   :members:

"""

# Can be removed starting with python3.11
from __future__ import annotations

import contextlib
import datetime
import functools
import os
import pathlib
import textwrap
import typing

import jinja2
import pkg_resources

from ....hooks import contexthook, iterhook
from ....utils import expand_path, smart_open
from ... import NoMatch, Plugin, errors, utils
from .file import Jinja2FileRenderer
from .readme import Jinja2ReadmeRenderer

if typing.TYPE_CHECKING:
    from ....builder import Builder
    from ....shared import Shared
    from ....tree import Tree

NOW = datetime.datetime.now()


class Jinja2Renderer(Plugin):
    """Abstract class for jinja2 renderers.

    To write your own renderer:

    - subclass this class;
    - define a default template name: :attr:`Jinja2Renderer.template`;
    - write such a template file,
      and place it in one of the :ref:`templatedirs <jinja2_options>`.
      The following template variables are defined
      and can be used in the template: :ref:`jinja2_template`;
    - you can also overwrite the methods defined here.

    You might also have a look at
    the implementation of the :class:`HTML renderer <evariste.plugins.renderer.html.HTMLRenderer>`.

    - Each file can be rendered in its own way:
      see :class:`~evariste.plugins.renderer.jinja2.file.Jinja2FileRenderer`
      (for instance, you might want to add a nice thumbnail to files that are images);
    - To define how files are annotated,
      see :class:`~evariste.plugins.renderer.jinja2.readme.Jinja2ReadmeRenderer`.
    """

    # pylint: disable=too-few-public-methods

    default_templatevar = {
        "date": NOW.strftime("%x"),
        "time": NOW.strftime("%X"),
        "datetime": NOW.strftime("%c"),
    }
    #: Name of the default template.
    template: str = None
    default_setup = {"destfile": "output"}

    def __init__(self, shared: Shared):
        super().__init__(shared)

        # Manage destination directory
        if self.local.setup["destdir"] is None:
            self.destdir = self.keyword
        else:
            self.destdir = utils.expand_path(self.local.setup["destdir"])
        try:
            os.makedirs(self.destdir, exist_ok=True)
        except FileExistsError as error:
            raise errors.EvaristeError(
                f"Cannot create directory '{self.destdir}'."
            ) from error

        # Create Jinja2 environment
        self.environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self._templatedirs()),
        )
        self.environment.filters["basename"] = os.path.basename
        self.environment.filters["yesno"] = utils.yesno

        # Dictionary of README files and renderers
        self.readmes = {}

    @iterhook("Tree.prune_before")
    def get_readme(self, tree: Tree) -> Tree:
        """Iterate the only README file for ``tree``.

        If there is such a README file, iterate over it (a single value);
        otherwise, iterate nothing.

        Side effect:
        Store a (partial) function in ``self.readmes[tree.from_source]`` to render this README file.
        """
        for plugin_type in self.iter_subplugins("readme"):
            try:
                renderer = self.shared.builder.plugins.match(plugin_type, tree)
                readme = renderer.get_readme(tree)
                self.readmes[tree.from_source] = functools.partial(
                    renderer.render, readme
                )
                yield readme.from_source
                return
            except NoMatch:
                continue
        return

    @utils.cached_iterator
    def iter_subplugins(self, subtype: str) -> typing.Iterable[Plugin]:
        """Iterate over subplugins of type ``subtype``.

        This method iterates plugins (as their keywords)
        ``{keyword}.{subtype}``, where ``keyword`` is the attribute of this class,
        or its subclasses.

        For instance, given that:

        - the correct plugins are loaded;
        - plugin :class:`renderer.html <evariste.plugins.renderer.html.HTMLRenderer>`
          is a subclass of :class:`renderer.jinja2 <Jinja2Renderer>`,

        call to ``Jinja2Renderer.iter_subplugins(HtmlRenderer(), "readme")``
        will yield: ``renderer.html.readme``, ``renderer.html.readme.mdwn``…
        """
        for parent in self.__class__.mro():  # pylint: disable=no-member
            if not hasattr(parent, "keyword"):
                break
            if parent.keyword is None:
                continue
            yield f"{parent.keyword}.{subtype}"

    def _templatedirs(self):
        """Iterator over the directories in which templates may exist.

        - Directories are returned as strings;
        - directories may not exist.
        """
        if self.local.setup["templatedirs"] is not None:
            yield from utils.expand_path(self.local.setup["templatedirs"]).split()
        yield pkg_resources.resource_filename(  # pylint: disable=no-member
            self.__class__.__module__, os.path.join("data", "templates")
        )
        yield from [
            os.path.join(utils.expand_path(path), "templates")
            for path in [
                ".evariste",
                "~/.config/evariste",
                "~/.evariste",
                "/usr/share/evariste",
            ]
        ]

    def render_tree(self, tree: Tree) -> str:
        """Render the tree using templates, and return the string."""
        # Copy targets to destination
        for file in tree.walk(dirs=False, files=True):
            if file.report.success:
                for target in file.report.targets:
                    utils.copy(
                        (file.root.from_fs / target).as_posix(),
                        (pathlib.Path(self.destdir) / target).as_posix(),
                    )
        # Select main template
        if self.local.setup["template"] is None:
            template = self.template
        else:
            template = self.local.setup["template"]

        # Create template loading file renderers
        content = ""
        for plugin_type in self.iter_subplugins("file"):
            for subrenderer in self.shared.builder.plugins.values(plugin_type):
                if subrenderer.extension is None:
                    subtemplate = subrenderer.template
                else:
                    subtemplate = f"{subrenderer.template}.{subrenderer.extension}"
                content += textwrap.dedent(
                    f"""\
                        {{%
                            from "file/{subtemplate}"
                            import file as file_{subrenderer.template}
                            with context
                        %}}
                        """
                )
        content += f"""{{% include "{template}" %}}"""

        # Render template
        return self.environment.from_string(content).render(
            {
                "destdir": pathlib.Path(self.destdir),
                "shared": self.shared,
                "local": self.local,
                "sourcepath": self._sourcepath,
                "render_file": self._render_file,
                "render_readme": self._render_readme,
                "render_template": self._render_template,
                "templatevar": self._get_templatevar(),
                "tree": tree,
            }
        )

    @contexthook("Builder.compile")
    @contextlib.contextmanager
    def render(self, builder: Builder) -> None:
        """Render the tree as a file, and write result into the destination file."""
        yield

        with smart_open(expand_path(self.local.setup["destfile"]), "w") as destfile:
            destfile.write(self.render_tree(builder.tree))

    def _get_templatevar(self):
        """Return the template variables.

        - First, update it with the default variables of this class
          (`self.default_templatevar`), then its ancestors.
        - Then, update it with the variables defined in the setup file.
        """
        templatevar = {}
        for parent in reversed(self.__class__.mro()):  # pylint: disable=no-member
            templatevar.update(getattr(parent, "default_templatevar", {}))
        templatevar.update(self.shared.setup[f"{self.keyword}.templatevar"])
        return templatevar

    @jinja2.pass_context
    def _render_file(self, context, filename):
        """Render ``context['file']``, which is a :class:`pathlib.Path`."""
        for plugin_type in self.iter_subplugins("file"):
            try:
                return self.shared.builder.plugins.match(plugin_type, filename).render(
                    filename, context
                )
            except NoMatch:
                continue
        return ""

    @jinja2.pass_context
    def _sourcepath(self, context, tree):
        """Return the path to the source file or archive.

        This functions builds the archive before returning its path. It can be
        called several times: the archive will be built only once.
        """
        return tree.make_archive(context["destdir"])

    @jinja2.pass_context
    def _render_readme(self, context, tree):
        """Return the code for the readme of `tree`."""
        # pylint: disable=unused-argument
        if tree.from_source in self.readmes:
            return self.readmes[tree.from_source]()
        return ""

    @jinja2.pass_context
    def _render_template(self, context, template):
        """Render template given in argument."""
        return textwrap.indent(
            self.environment.get_or_select_template(template).render(context), "  "
        )
