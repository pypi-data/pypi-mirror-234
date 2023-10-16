#!/usr/bin/env python3

# Copyright 2014-2023 Louis Paternault
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

"""Création de labyrinthes"""

import argparse
import logging
import sys

from jouets.labyrinthe import shapes
from jouets.utils import plugins
from jouets.utils.aargparse import analyseur, yesno

from . import VERSION


def analyse():
    """Renvoie un analyseur de la ligne de commande."""
    parser = analyseur(VERSION, prog="labyrinthe", description="Generate labyrinths")

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "--format", "-f", choices=["tex", "none"], default="none", help="Output format"
    )
    common.add_argument(
        "--template",
        "-t",
        default=None,
        help="Template to use for the LaTeX output format.",
    )
    common.add_argument(
        "--display",
        "-d",
        choices=["yes", "no"],
        default="yes",
        help="Display labyrinth building",
    )
    common.add_argument("-s", "--size", default=10, help="Size of the labyrinth")

    analyseur_formes = parser.add_subparsers(
        title="shapes", description="Subcommands providing shapes"
    )
    for cls in plugins.iter_classes(shapes, shapes.LabyrintheBase):
        sub_analyseur = analyseur_formes.add_parser(
            cls.keyword,
            help=cls.help,
            description=cls.description,
            parents=[common],
        )
        sub_analyseur.set_defaults(labyrinthe=cls)

    return parser


def main():
    """Fonction principale"""
    options = analyse().parse_args(sys.argv[1:])

    if "labyrinthe" not in options:
        logging.error("(ERROR) Please choose a labyrinth.")
        sys.exit(1)

    lab = options.labyrinthe(taille=int(options.size), affiche=yesno(options.display))
    lab.construit()
    if options.format == "tex":
        print(lab.export_tex(options.template))
    lab.fin()


if __name__ == "__main__":
    main()
