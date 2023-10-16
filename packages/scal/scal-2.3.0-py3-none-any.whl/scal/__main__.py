#!/usr/bin/env python3

# Copyright Louis Paternault 2011-2022
#
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>. 1

"""Produce a calendar."""

import logging
import sys

import argdispatch

import scal

from . import VERSION, calendar, errors, template
from .template import commands

LOGGER = logging.getLogger(scal.__name__)
LOGGER.addHandler(logging.StreamHandler())


def _subcommand_templates_list(args):
    """List built-in templates."""
    parser = argdispatch.ArgumentParser(
        prog="scal templates list",
        description="List built-in templates.",
    )

    parser.parse_args(args)

    for name in commands.list_templates():
        print(name)


def _subcommand_templates_config(args):
    """Display an example configuration file for a given built-in template."""
    parser = argdispatch.ArgumentParser(
        prog="scal templates config",
        description="Display an example configuration file default for a given built-in template.",
    )

    parser.add_argument(
        "TEMPLATE",
        help="Template name",
    )

    arguments = parser.parse_args(args)

    with open(commands.config_file(arguments.TEMPLATE), encoding="utf8") as file:
        print(file.read().strip())


def _subcommand_templates(args):
    """Manage 'scal' templates."""
    parser = argdispatch.ArgumentParser(
        prog="scal templates",
        description="Manage 'scal' templates.",
    )

    subparser = parser.add_subparsers()
    subparser.add_function(_subcommand_templates_list, command="list")
    subparser.add_function(_subcommand_templates_config, command="config")

    parser.parse_args(args)


def _subcommand_generate(args):
    """Generate calendar."""
    parser = argdispatch.ArgumentParser(
        prog="scal generate",
        description="A year calendar producer.",
        formatter_class=argdispatch.RawTextHelpFormatter,
    )

    parser.add_argument(
        "FILE",
        help="Configuration file",
        type=argdispatch.FileType("r"),
        default=sys.stdin,
    )

    arguments = parser.parse_args(args)

    try:
        inputcalendar = calendar.Calendar.from_stream(arguments.FILE)
    except errors.ConfigError as error:
        LOGGER.error("Configuration error in file %s: %s", arguments.FILE.name, error)
        sys.exit(1)
    print(template.generate_tex(inputcalendar))


SUBCOMMANDS = {
    "generate": _subcommand_generate,
    "templates": _subcommand_templates,
}
DEFAULT_SUBCOMMAND = "generate"


def argument_parser():
    """Return a command line parser."""

    parser = argdispatch.ArgumentParser(
        prog="scal",
        description="A year calendar producer.",
        formatter_class=argdispatch.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--version",
        help="Show version",
        action="version",
        version="%(prog)s " + VERSION,
    )

    subparser = parser.add_subparsers(
        required=True,
        title="Subcommands",
        description="""If no subcommand is given, "generate" is used by default.""",
    )

    for command, function in sorted(SUBCOMMANDS.items()):
        subparser.add_function(function, command=command)

    return parser


def main(args=None):
    """Main function."""
    parser = argument_parser()

    if args is None:
        args = sys.argv[1:]

    if not args:
        return parser.parse_args()
    if args[0] in ("-h", "--help", "--version"):
        return parser.parse_args(args)
    if args[0] in SUBCOMMANDS:
        return parser.parse_args(args)
    return parser.parse_args([DEFAULT_SUBCOMMAND] + args)


if __name__ == "__main__":
    main()
