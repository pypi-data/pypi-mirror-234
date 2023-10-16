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

"""Default HTML file renderer

.. autoclass:: HtmlFileRenderer
   :members:

"""

from ...jinja2.file import Jinja2FileRenderer


class HtmlFileRenderer(Jinja2FileRenderer):
    """Default HTML file renderer.

    This displays the file name together with the file source.

    To write another file renderer, you can:

    - define a new
      :attr:`~evariste.plugins.renderer.jinja2.file.Jinja2FileRenderer.template` to use:
    - overwrite the default
      :meth:`~evariste.plugins.renderer.jinja2.file.Jinja2FileRenderer.match` method;
    - overwrite the default
      :meth:`~evariste.plugins.renderer.jinja2.file.Jinja2FileRenderer.render` method.
    """

    # pylint: disable=too-few-public-methods

    plugin_type = "renderer.html.file"
    keyword = "renderer.html.file.default"
    extension = "html"
