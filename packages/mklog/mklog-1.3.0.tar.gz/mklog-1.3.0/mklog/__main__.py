# Copyright 2009-2023 Louis Paternault

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Simple way of logging things.

* "Logging" means prepending date and time at the beginning of lines.
* "Things" may be content of files, standard input, or output of a command.
"""

import argparse
import io
import logging
import os
import subprocess
import sys
import textwrap
import threading
import time
from collections import namedtuple

import mklog
from mklog import errors

LOGGER = logging.getLogger(mklog.__name__)
LOGGER.addHandler(logging.StreamHandler())

TIMEFORMAT = "%Y-%m-%d %H:%M:%S"


################################################################################
##### Print line preceded by date and time
# No verification is done whether argument contains exactly one line or not.
def log(line, output_format, out=sys.stdout):
    r"""Print argument, preceded by current time and date

    Arguments:
    - out: destination file-object.
    - line: a string to print, supposed to end with an EOL character (\n).
    - output_format: a named tuple of two strings.
        - output_format.line is the line-format. It can (should?) contain
          substrings as "{time}" and "{line}" which are replaced by current
          time and the line to print.
        - output_format.time is the time-format. It will be passed to
          "time.strftime()" to print current time.

    >>> log(
    ...     "Foo bar baz.",
    ...     namedtuple("Format", "line, time")(line="XXX {line}", time=""),
    ...     out=sys.stdout,
    ...     )
    XXX Foo bar baz.
    """
    print(
        output_format.line.format(time=time.strftime(output_format.time), line=line),
        file=out,
        flush=True,
    )


def log_fd(file_desc, output_format, out=sys.stdout):
    """Print content from `file_desc`, preceding it by current date and time.

    :param int file_desc: File descriptor to read from.
    :param str output_format: format to use to print content. See :func:`log`
        to know its syntax.
    :param file out: Destination file-object.
    """
    with os.fdopen(file_desc, errors="replace") as file:
        log_file(file, output_format, out)


def log_file(file, output_format, out=sys.stdout):
    """Print content from :class:`file` `file`, preceding it by current date and time.

    Except from `file`, arguments are the same as arguments of :func:`log_fd`.
    """
    for line in file:
        log(line.strip("\n"), output_format, out)


################################################################################
def safe_open(name):
    """Safely open a file, and return

    - None if an error occured
    - The file object otherwise"""
    try:
        # pylint: disable=unspecified-encoding
        return open(name, "r", errors="replace")
    except IOError:
        LOGGER.error("Error while opening '%s'.", name)
        return None


################################################################################
### Parsing arguments
def commandline_parser():
    """Parse command line

    Return a tuple (options, file), where:
    - options: a dictionary containing only the command (if any) to be executed
      (corresponding to option "-c") in the key "command";
    - file: the list of files to be processed.
    """
    # Defining parser
    parser = argparse.ArgumentParser(
        prog="mklog",
        formatter_class=argparse.RawTextHelpFormatter,
        description=textwrap.dedent(
            """
            Print the standard input, content of files, or result of a command
            to standard output, preceded by date and time (in a log-like way).
            """
        ),
        epilog=textwrap.dedent(
            """
            `mklog` aims to be a simple way to write text in a log format,
            i.e.  each line being preceded by date and time it was written.
            Text can be either standard input, content of files, or both
            standard and error output of a command.

            If neither files nor a command are given, standard input is
            processed.  Otherwise, the content of each file (if any), and the
            output of the command (if any) are processed.

            # Environment

            When executing command (with `-c` option), environment is
            preserved, and command should run exactly the same way it should
            have run if it had been executed directly within the shell.
            """
        ),
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {mklog.VERSION}"
    )

    parser.add_argument("files", metavar="FILES", nargs="*", help="Files to process.")

    parser.add_argument(
        "-f",
        "--format",
        dest="line_format",
        default="{time} {line}",
        help=textwrap.dedent(
            """\
            Format of output. Interpreted sequences are "{time}" for current
            time, "{line}" for lines of the command.  Default is "{time}
            {line}".
            """
        ),
    )

    parser.add_argument(
        "-t",
        "--time-format",
        dest="time_format",
        default=TIMEFORMAT,
        help=textwrap.dedent(
            # pylint: disable=consider-using-f-string
            """\
            Format of time. See the "time" documentation for more information
            about format (e.g.
            http://docs.python.org/library/time.html#time.strftime).  Default
            is "{}".
            """.format(
                TIMEFORMAT.replace("%", "%%")
            )
        ),
    )

    parser.add_argument(
        "-c",
        "--command",
        nargs=argparse.REMAINDER,
        help=textwrap.dedent(
            """
            Run command, processing both its standard and error output.

            Commands can be written whithout quotes (such as `mklog -c tail -f
            file1 file2`), or with it, which allows using shell features (such
            as `mklog -c "(ls; cat file1) & cat file2"`).

            Destination of output is preserved: standard output of command is
            written to standard output of `mklog`, and standard error to
            standard error. Both are processed.

            This must be the last option on the command line.
        """
        ),
    )

    # Running parser
    return parser


################################################################################
### Main function
def main():
    "Main function"

    options = commandline_parser().parse_args()
    # Now, "options" contains a dictionary containing only the command (if any)
    # to be executed (corresponding to option "-c") in the key "command", and
    # "files" contains the list of files to be processed.

    try:
        # Handling files
        # At the end of this block, "files" will contain the list of files to
        # be read from: either files given in argument, or standard input if no
        # file is given in the command line.
        if (not options.files) and options.command is None:
            options.files = [
                io.TextIOWrapper(
                    sys.stdin.buffer, encoding=sys.stdin.encoding, errors="replace"
                )
            ]
        else:
            options.files = [safe_open(f) for f in options.files]

        # Processing "options.line_format" and "options.time_format".
        # Quick and dirty parsing.
        output_format = namedtuple("Format", "line, time")(
            line=options.line_format, time=options.time_format
        )

        # Processing files
        for fileobj in options.files:
            if fileobj is None:
                continue
            log_file(fileobj, output_format)

        # Handling command
        if options.command is not None:
            stdoutpipe = os.pipe()
            stderrpipe = os.pipe()
            try:
                with subprocess.Popen(
                    options.command,
                    stdin=sys.stdin,
                    stdout=stdoutpipe[1],
                    stderr=stderrpipe[1],
                    shell=(len(options.command) == 1),
                ) as process:
                    standard = [
                        threading.Thread(
                            target=log_fd,
                            kwargs={
                                "file_desc": pipe[0],
                                "output_format": output_format,
                                "out": out,
                            },
                            daemon=True,
                        )
                        for pipe, out in [
                            (stdoutpipe, sys.stdout),
                            (stderrpipe, sys.stderr),
                        ]
                    ]
                    for thread in standard:
                        thread.start()
                    process.wait()
                    os.close(stderrpipe[1])
                    os.close(stdoutpipe[1])
                    for thread in standard:
                        thread.join()
            except OSError as error:
                raise errors.ExecutionError(options.command, str(error)) from error

    except KeyboardInterrupt:
        sys.exit(1)
    except errors.MklogError as error:
        LOGGER.error(error)
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
