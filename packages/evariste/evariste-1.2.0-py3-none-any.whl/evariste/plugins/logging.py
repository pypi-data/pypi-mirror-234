# Copyright Louis Paternault 2021-2022
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

"""Plugin log progress."""

import contextlib
import logging
import sys
import threading

from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress

from ..hooks import contexthook
from . import Plugin

LOGGER = logging.getLogger()

LOGGING_LEVELS = {
    -1: 100,  # Quiet
    0: logging.WARNING,
    1: logging.INFO,
    2: logging.DEBUG,
    3: 1,
}


def get_logging_level(verbose):
    """Turn command line verbosity into :mod:`logging` verbosity."""
    if verbose in LOGGING_LEVELS:
        return LOGGING_LEVELS[verbose]
    if verbose is None:
        return LOGGING_LEVELS[0]
    if verbose > max(LOGGING_LEVELS.keys()):
        return LOGGING_LEVELS[max(LOGGING_LEVELS.keys())]
    raise NotImplementedError()


class Logging(Plugin):
    """Main plugin to log stuff.

    Its main goal is to load the right "actual" plugin depending on the configuration.
    """

    keyword = "logging"

    @classmethod
    def depends_dynamic(cls, shared):
        yield f"""logging.{shared.setup["logging"].get("logger", "auto")}"""


class LoggingQuiet(Plugin):
    """Does not log anything.

    Note that things logged *before* this plugin is enabled
    are still logged using the default Python module.
    """

    keyword = "logging.quiet"


class LoggingAuto(Logging):
    """Automatic selection of logging plugin.

    If standard output is a tty, log using nice colors and progress bar.
    Otherwise, log without frills.
    """

    keyword = "logging.auto"

    @classmethod
    def depends_dynamic(cls, shared):
        if shared.setup["logging"].get("logger", "auto") == "auto":
            if sys.stdout.isatty():
                yield "logging.rich"
            else:
                yield "logging.stdlib"


class LoggingStdlib(Logging):
    """Log stuff"""

    # pylint: disable=too-few-public-methods

    keyword = "logging.stdlib"
    default_setup = {"format": "%(message)s"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lock = threading.Lock()
        self.count = 0
        self.total = 0

        LOGGER.addHandler(self.get_handler())
        self.set_level(LOGGER)

    def get_handler(self):
        """Return the :class:`logging.Handler` used by this class."""
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(self.local.setup["format"]))
        return handler

    def set_level(self, logger):
        """Process --verbose and --quiet options."""
        arguments = dict(self.shared.setup["arguments"])
        if arguments.get("quiet", None):
            arguments["verbose"] = -1
        logger.setLevel(get_logging_level(arguments.get("verbose", 0)))

    @contexthook("File.compile")
    @contextlib.contextmanager
    def compile_file(self, tree):
        """Log file compilation (including progress)."""
        with self.lock:
            if self.count == 0:
                # Save the total number of files to compile.
                self.total = self.shared.builder.tree.count()
            self.count += 1
            count = self.count
        LOGGER.info(
            f"Compiling [{count: >{len(str(self.total))}}/{self.total}] "
            f"'{tree.from_source}'…"
        )

        yield

        if tree.report.success:
            LOGGER.info(
                f"Compiling [{count: >{len(str(self.total))}}/{self.total}] "
                f"'{tree.from_source}': success."
            )
        else:
            LOGGER.info(
                f"Compiling [{count: >{len(str(self.total))}}/{self.total}] "
                f"'{tree.from_source}': failed."
            )


class LoggingRich(LoggingStdlib):
    """Log stuff with colors and progress bar."""

    keyword = "logging.rich"

    def __init__(self, *args, **kwargs):
        self.console = Console()
        super().__init__(*args, **kwargs)

    def get_handler(self):
        return RichHandler(console=self.console)

    @contexthook("Builder.compile")
    @contextlib.contextmanager
    def compile_builder(
        self, builder, *args, **kwargs
    ):  # pylint: disable=unused-argument
        """Save the total number of files to compile."""

        # pylint: disable=attribute-defined-outside-init
        with Progress(console=self.console, transient=True) as self.progress:
            self.task = self.progress.add_task("Compiling", total=0)
            yield

    @contexthook("File.compile")
    @contextlib.contextmanager
    def compile_file(self, tree):
        """Log file compilation (including progress)."""
        with super().compile_file(tree):
            yield
            self.progress.update(self.task, advance=1, total=self.total)
