# Copyright Louis Paternault 2016-2023
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


"""Text renderer: print report on terminal."""

import contextlib
import logging
import sys
import typing
from dataclasses import dataclass

import unidecode

from ...hooks import contexthook
from ...utils import yesno
from .. import Plugin

LOGGER = logging.getLogger("evariste")


@dataclass
class TreePrettyPrinter:
    """Pretty print a tree"""

    # pylint: disable=too-few-public-methods

    # This class could be a function, but it is a recursive function, and
    # turning it into a class allows to tell appart arguments that change
    # for every recursive call, and arguments that never change.

    print_function: typing.Callable = print
    report: bool = False
    color: bool = False
    reverse: bool = False
    display: typing.Union[str, None] = None

    def pprint(self, tree, *, prefix="", last=True):
        """Pretty print the given tree"""
        # pylint: disable=too-many-branches

        # If there is a bug here, before fixing it, think about replacing this function
        # with rich tree
        # https://rich.readthedocs.io/en/latest/tree.html
        line = []

        txttree = ""
        txttree += prefix
        if last:
            txttree += {False: "└", True: "┌"}[self.reverse]
        else:
            txttree += "├"
        txttree += "─"
        if tree.is_dir():
            txttree += {True: "┴", False: "┬"}[self.reverse]
        else:
            txttree += "─"
        txttree += "╼"
        line.append(txttree)

        if self.report:
            if tree.report.success:
                if self.color:
                    reportstr = "\033[92m ok \033[0m"
                else:
                    reportstr = " ok "
            else:
                if self.color and tree.is_dir():
                    reportstr = "\033[93mfail\033[0m"
                elif self.color and not tree.is_dir():
                    reportstr = "\033[91mfail\033[0m"
                else:
                    reportstr = "fail"
            reportstr = f"[{reportstr}]"
            line.append(reportstr)

        line.append(str(tree.relativename))

        if not self.reverse:
            self.print_function(" ".join(line))

        if tree.is_dir():
            if last:
                postfix = "  "
            else:
                postfix = "│ "

            subtree = [branch for branch in tree.values() if self.display(branch)]
            if self.reverse:
                lastcounter = 1
            else:
                lastcounter = len(subtree)
            counter = 0
            for sub in sorted(subtree, reverse=self.reverse):
                counter += 1
                self.pprint(sub, prefix=prefix + postfix, last=counter == lastcounter)

        if self.reverse:
            self.print_function(" ".join(line))


ALLOWED_DISPLAY_OPTIONS = ["errors", "all", "errors_or_all"]


class TextRenderer(Plugin):
    """Text renderer: print report on terminal."""

    keyword = "renderer.text"
    default_setup = {
        "color": "auto",
        "ascii": False,
        "reverse": False,
        "display": "all",
    }

    @contexthook("Builder.compile")
    @contextlib.contextmanager
    def render(self, builder):
        """Print the report to the standard output."""

        yield

        # Option 'ascii'
        if yesno(self.local.setup["ascii"]):

            def asciiprint(text):
                """Convert argument to ascii, and print it."""
                print(unidecode.unidecode(text))

            print_function = asciiprint
        else:
            print_function = print

        # Option 'reverse'
        reverse = yesno(self.local.setup["reverse"])

        # Option 'display'
        displayoption = self.local.setup["display"]
        if displayoption not in ALLOWED_DISPLAY_OPTIONS:
            LOGGER.warning(
                (
                    # pylint: disable=consider-using-f-string
                    "[renderer.text] Option 'display' must be one of {} (currently {})."
                ).format(
                    ", ".join((f"'{option}'" for option in ALLOWED_DISPLAY_OPTIONS)),
                    f"'{displayoption}'",
                )
            )
            displayoption = self.default_setup["display"]
        if displayoption == "errors_or_all":
            if builder.tree.report.success:
                displayoption = "all"
            else:
                displayoption = "errors"

        # pylint: disable=unnecessary-lambda-assignment
        if displayoption == "errors":
            display = lambda tree: not tree.report.success
        else:
            display = lambda tree: True

        # Option 'color'
        color = self.local.setup["color"]
        if color.lower() == "auto":
            color = sys.stdout.isatty()  # pylint: disable=no-member
        color = yesno(color)

        # Render
        TreePrettyPrinter(
            report=True,
            color=color,
            print_function=print_function,
            reverse=reverse,
            display=display,
        ).pprint(builder.tree)
