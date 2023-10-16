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

"""Common utilities for readme renderers using Jinja2.

.. autoclass:: Jinja2ReadmeRenderer
   :members:

"""

# Can be removed starting with python3.11
from __future__ import annotations

import glob
import os
import pathlib
import typing

from ... import Plugin

if typing.TYPE_CHECKING:
    from ....tree import Tree


class Jinja2ReadmeRenderer(Plugin):
    """Default readme renderer using jinja2.

    This is an abstract class that defines a default README renderer for files.
    From within a template,
    the `macro <https://jinja.palletsprojects.com/en/3.0.x/templates/#macros>`__ ``render_readme``
    can be called to annotate a file, which:

    - looks for the first plugin that matches this file
      (that is, the first plugin where :meth:`Jinja2ReadmeRenderer.match` returns ``True``);
    - calls :meth:`Jinja2ReadmeRenderer.render`, and returns its return value.

    To implement such a renderer, in a subclass:

    - do one of:
        - set :attr:`Jinja2ReadmeRenderer.extensions` as a list of extensions:
          the README of any file ``foo`` is ``foo.{ext}``,
          the README of any directory is ``directory/README.{ext}``,
          where ``ext`` is one of the extensions listed here.
        - implement :meth:`Jinja2ReadmeRenderer.render`;
    - (optional) implement
      :meth:`Jinja2ReadmeRenderer.match` and :meth:`Jinja2ReadmeRenderer.get_readme`
      if the default implementation does not please you.
    """

    # pylint: disable=too-few-public-methods, abstract-method

    #: List of extensions of the READMEs (see :class:`Jinja2ReadmeRenderer`).
    extensions: typing.List[str] = []

    def match(self, tree: Tree) -> bool:
        """Return ``True`` if this plugin can handle the README of the argument."""
        # pylint: disable=arguments-renamed
        return self.get_readme(tree) is not None

    def get_readme(self, tree: Tree) -> typing.Optional[Tree]:
        """Return readme file for ``tree``, or ``None`` if there is no such README file."""
        if tree.is_dir():
            return self._get_readme_dir(tree)
        return self._get_readme_file(tree)

    def _get_readme_dir(self, tree):
        """Iterate over potential readme for the given directory ``tree``."""
        for ext in self.extensions:
            for filename in glob.iglob((tree.from_fs / f"*.{ext}").as_posix()):
                basename = os.path.basename(filename)
                if not tree.find(basename):
                    continue
                if basename.count(".") == 1:
                    if basename.split(".")[0].lower() == "readme":
                        return tree.root.find(
                            pathlib.Path(filename).relative_to(tree.root.from_fs)
                        )
        return None

    def _get_readme_file(self, tree):
        """Iterate over potential readme for the given file ``tree``."""
        for ext in self.extensions:
            for filename in glob.iglob(f"{tree.from_fs}.{ext}"):
                readme = tree.root.find(
                    pathlib.Path(filename).relative_to(tree.root.from_fs)
                )
                if readme:
                    return readme
        return None

    @staticmethod
    def render(tree: Tree) -> str:
        """Render argument as README.

        Return a string to be included when rendering the template.
        The functions and variables available in the template
        are described in :ref:`plugin_renderer_jinja2`.
        """
        # pylint: disable=unused-argument
        with open(tree.from_fs, encoding="utf8") as source:
            return source.read()
