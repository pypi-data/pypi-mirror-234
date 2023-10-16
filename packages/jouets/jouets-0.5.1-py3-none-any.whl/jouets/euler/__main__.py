#!/usr/bin/env python3

# Copyright 2015-2023 Louis Paternault
#
# This file is part of Jouets.
#
# Jouets is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Jouets is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Jouets.  If not, see <http://www.gnu.org/licenses/>.

"""Exemples d'utilisation de la méthode d'Euler"""

import runpy
import sys

from jouets.utils import plugins
from jouets.utils.aargparse import analyseur

VERSION = "0.1.1"


def analyse():
    """Renvoie un analyseur de ligne de commande."""
    parser = analyseur(
        VERSION,
        prog="euler",
        description="Simule des phénomènes physiques en utilisant la méthode d'Euler.",
    )
    subparsers = parser.add_subparsers(title="Commands", dest="command")
    subparsers.required = True
    subparsers.dest = "command"

    for module in plugins.iter_modules(
        sys.modules[__package__], ignore=[r".*\.__main__$"]
    ):
        subparsers.add_parser(
            module.__name__.split(".")[-1], help=plugins.get_description(module)
        )

    return parser


def main():
    """Fonction principale"""
    # Argument parsing
    arguments = analyse().parse_args(sys.argv[1:])

    # Running subcommand
    runpy.run_module("jouets.euler.{}".format(arguments.command), run_name="__main__")


if __name__ == "__main__":
    main()
