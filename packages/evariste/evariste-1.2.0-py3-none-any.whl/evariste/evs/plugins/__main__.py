# Copyright Louis Paternault 2020-2022
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

"""Command line client to :mod:`evs`"""

import operator

import argdispatch

from ... import plugins


def do_list(args):
    """List available plugins."""
    parser = argdispatch.ArgumentParser(
        prog="evs plugins list",
        description=("List available plugins"),
        formatter_class=argdispatch.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        default=0,
        help="Add verbosity",
    )
    parser.add_argument(
        "--dir",
        "-d",
        action="append",
        default=[],
        help="Additional plugin directories.",
    )
    arguments = parser.parse_args(args)
    if arguments.verbose:
        formatter = (
            """{plugin_type} {plugin.keyword} {plugin.__module__} "{description}" """
        )
        print("""# Type Keyword Module Description""")
    else:
        formatter = "{plugin.keyword}"

    for plugin in sorted(
        plugins.find_plugins(arguments.dir), key=operator.attrgetter("keyword")
    ):
        if plugin.plugin_type:
            plugin_type = plugin.plugin_type
        else:
            plugin_type = "none"
        if isinstance(plugin.__doc__, str):
            description = plugin.__doc__.split("\n")[0]
        else:
            description = ""
        print(
            formatter.format(
                plugin=plugin, plugin_type=plugin_type, description=description
            )
        )


def commandline_parser():
    """Return a command line parser."""

    parser = argdispatch.ArgumentParser(
        prog="evs plugins",
        description=("Some useful plugin utilities for evariste."),
        formatter_class=argdispatch.RawTextHelpFormatter,
    )

    subparsers = parser.add_subparsers(
        title="Subcommands",
    )

    subparsers.required = True
    subparsers.dest = "subcommand"
    subparsers.add_function(do_list, command="list")

    return parser


def main():
    """Main function"""
    commandline_parser().parse_args()


if __name__ == "__main__":
    main()
