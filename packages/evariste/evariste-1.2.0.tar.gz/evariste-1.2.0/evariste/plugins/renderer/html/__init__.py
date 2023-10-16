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

"""Render tree as an HTML (body) page.

.. autoclass:: HTMLRenderer
   :members:

"""

import contextlib
import datetime
import logging

from .... import VERSION
from ..jinja2 import Jinja2Renderer
from . import file


class HTMLRenderer(Jinja2Renderer):
    """Render tree as an HTML div (without the ``<div>`` tags).

    The default template name is ``tree.html``,
    and such a default template is found in one of the template directories.
    """

    # pylint: disable=too-few-public-methods

    keyword = "renderer.html"

    #: Default template.
    #: This can be overloaded in the setup file.
    #: The template is looked for in any of the :ref:`templatedirs <jinja2_options>`.
    template: str = "tree.html"
    default_setup = {"href_prefix": "", "destfile": "index.html"}
    depends = ["renderer.html.readme.html", "renderer.html.file.default"]
    default_templatevar = {
        # pylint: disable=line-too-long, consider-using-f-string
        "aftertree": 'Generated using <a href="http://framagit.org/spalax/evariste">Évariste</a> version {}, on {}.'.format(
            VERSION, datetime.datetime.now().strftime("%c")
        )
    }
