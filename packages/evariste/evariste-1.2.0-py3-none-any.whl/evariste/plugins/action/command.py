# Copyright Louis Paternault 2017-2023
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

"""Shell command: perform a (list of) shell command(s) on files."""

import glob
import io
import logging
import os
import pathlib
import re
import shlex
import subprocess
import tempfile
import threading

from ... import errors
from ...utils import yesno
from . import Action, Report

LOGGER = logging.getLogger("evariste")
STRACE_RE = re.compile(
    r'^\d* *open(at)?\((.*, )?"(?P<name>.*)",.*O_RDONLY.*\) = *[^ -].*'
)


class MissingOption(errors.EvaristeError):
    """No command was provided for action :class:`Command`."""

    def __init__(self, section, option, filename=None):
        super().__init__()
        self.filename = filename
        self.section = section
        self.option = option

    def __str__(self):
        # pylint: disable=line-too-long
        if self.filename is None:
            return f"Configuration for file is missing option '{self.option}' in section '{self.section}'."
        return f"Configuration for file '{self.filename}' is missing option '{self.option}' in section '{self.section}'."


def system_no_strace(command, path, log):
    """Run a system command.

    This function:
    - run command;
    - log standard output and error.
    """

    with subprocess.Popen(
        ["sh", "-c", command],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        errors="replace",
        cwd=path.parent.from_fs.as_posix(),
    ) as process:
        log.write(process.communicate()[0])

        return process.returncode


def system_strace(command, path, log, depends):
    """Run a system command, analysing strace output to set `depends` files.

    This function:
    - run command;
    - log standard output and error;
    - track opened files.
    """

    def _process_strace_line(line):
        """Process output line of strace, and complete ``depends`` if relevant."""
        match = STRACE_RE.match(line)
        if match:
            name = pathlib.Path(path.parent.from_fs) / pathlib.Path(
                match.groupdict()["name"]
            )
            if name.resolve() != path.from_fs.resolve():  # pylint: disable=no-member
                if name in path.vcs:
                    depends.add(name)

    def _process_strace(pipe):
        """Process strace output, to find dependencies."""
        with open(pipe, mode="r", errors="replace", encoding="utf8") as file:
            for line in file:
                try:
                    _process_strace_line(line)
                except FileNotFoundError:
                    # File was deleted between the time its name is read and
                    # the time we check if it is a dependency: it can be
                    # discarded.
                    pass

    with tempfile.TemporaryDirectory() as tempdir:
        stdout = list(os.pipe())
        stderr = list(os.pipe())
        fifo = os.path.join(tempdir, str(id(path)))
        os.mkfifo(fifo)

        with subprocess.Popen(
            [
                "strace",
                "-f",
                "-o",
                fifo,
                "-e",
                "trace=open,openat",
                "sh",
                "-c",
                command,
            ],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            pass_fds=stdout + stderr,
            universal_newlines=True,
            errors="replace",
            cwd=path.parent.from_fs.as_posix(),
        ) as process:
            strace_thread = threading.Thread(
                target=_process_strace, daemon=True, kwargs={"pipe": fifo}
            )
            strace_thread.start()
            log.write(process.communicate()[0])
            os.unlink(fifo)
            strace_thread.join()
            for descriptor in stdout + stderr:
                os.close(descriptor)

    return process.returncode


class Command(Action):
    """System command"""

    keyword = "action.command"
    default_setup = {"strace": False}

    def get_targets(self, path):
        """Return the path of the targets."""
        if path.config[self.keyword]["targets"] is None:
            return []

        targets = []
        for item in shlex.split(path.config[self.keyword]["targets"]):
            for target in glob.glob(
                str(path.parent.from_fs.as_posix() / pathlib.Path(path.format(item)))
            ):
                # pylint: disable=duplicate-code
                targets.append(pathlib.Path(target).relative_to(path.root.from_fs))
        return targets

    def command(self, path):
        """Return the system command to run."""
        return path.config[self.keyword]["command"]

    def _run_command(self, path, command, *, log, depends):
        """Run the system command ``command``.

        - The list of dependencies is added to the set ``depends``.
        - The log is written at the end of ``log``.
        """
        LOGGER.info(f"Running command: {command}")

        if (yesno(path.config[self.keyword].get("strace", "false"))) or (
            "strace" not in path.config[self.keyword]
            and yesno(self.local.setup["strace"])
        ):
            returncode = system_strace(
                command=command,
                path=path,
                log=log,
                depends=depends,
            )
        else:
            returncode = system_no_strace(command=command, path=path, log=log)

        return returncode == 0

    def compile(self, path):
        command = path.format(self.command(path))
        depends = set()

        with io.StringIO() as log:
            log.write(f"$ {command}\n")

            success = self._run_command(path, command, log=log, depends=depends)

            return Report(
                path,
                success=success,
                targets=self.get_targets(path),
                depends=depends,
                log=log.getvalue(),
            )

    def match(self, value):
        # pylint: disable=unused-argument
        return False
