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

"""Abstract utilities for file renderers using Jinja2.

.. autoclass:: Jinja2FileRenderer
   :members:

"""

# Can be removed starting with python3.11
from __future__ import annotations

import typing

import jinja2

from ... import Plugin

if typing.TYPE_CHECKING:
    from ...tree import Tree


class Jinja2FileRenderer(Plugin):
    """Renderer of file using jinja2.

    This is an abstract class that defines a default renderer for files.

    From within a template,
    the `macro <https://jinja.palletsprojects.com/en/3.0.x/templates/#macros>`__
    ``render_file`` can be called, which:

    - looks for the first plugin that matches this file
      (that is, the first plugin where :meth:`Jinja2FileRenderer.match` returns ``True``;
    - calls :meth:`Jinja2FileRenderer.render`, and returns its return value.

    To implement such a renderer, you can:

    - write a :file:`file/default` template that defines a ``file()`` macro;
    - set the :attr:`Jinja2FileRenderer.extension`,
      and write a :file:`file/default.{extension}` template, that defines a ``file()`` macro;
    - overwrite the :meth:`Jinja2FileRenderer.render` method,
      if the default implementation does not pleas you.

    You can also overwrite :meth:`Jinja2FileRenderer.match`,
    so that your subplugin cannot be applied to *any* file, but only to some of them.
    """

    keyword = None
    #: Extension that is automatically added at the end of the template name when searching them.
    extension: typing.Optional[str] = None
    priority = -float("inf")

    #: Name of the template rendering files.
    template: str = "default"

    def match(self, filename: Tree) -> bool:
        """This is the default renderer, that matches everything."""
        # pylint: disable=unused-argument, arguments-renamed
        return True

    def render(self, filename: Tree, context: jinja2.runtime.Context) -> str:
        """Render ``tree``, which is a :class:`~evariste.tree.File`

        By default, call the ``file()``
        `macro <https://jinja.palletsprojects.com/en/latest/templates/#macros>`__,
        with ``filename`` as argument, and returns its value.
        """
        # pylint: disable=arguments-differ
        return context[f"file_{self.template}"](filename)
