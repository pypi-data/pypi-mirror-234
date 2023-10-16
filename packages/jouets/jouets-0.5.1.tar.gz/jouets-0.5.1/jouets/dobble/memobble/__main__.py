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

"""Création et vérification de jeux de cartes de Mémobble"""

import random

from jouets.dobble import VERSION, Carte
from jouets.dobble import output as dobbleoutput
from jouets.dobble.memobble import Jeu
from jouets.utils import plugins
from jouets.utils.aargparse import analyseur

from . import algo as memobblealgo


def analyse():
    """Renvoie un analyseur de ligne de commande."""
    parser = analyseur(VERSION, prog="memobble")

    parser.add_argument(
        "-n", "--num", type=int, default=None, help="Number of cards in each sub-game."
    )

    parser.add_argument(
        "-s", "--sub", type=int, default=None, help="Number of sub-games."
    )

    algo_plugins = {
        algo.keyword: algo
        for algo in plugins.iter_classes(memobblealgo, memobblealgo.MemobbleAlgo)
    }
    parser.add_argument(
        "-a",
        "--algo",
        type=memobblealgo.argparse_type_algo,
        default="bipartite",
        help=(
            # pylint: disable=consider-using-f-string
            "Algorithm to use to create each sub-game: {}.".format(
                ", ".join(
                    [
                        f"'{key}' ({plugins.get_description(algo)})"
                        for key, algo in algo_plugins.items()
                    ]
                )
            )
        ),
    )
    parser.add_argument(
        "-r",
        "--random",
        dest="random",
        action="store_true",
        default=0,
        help="Random seed.",
    )
    parser.add_argument(
        "-g", "--group", action="store_true", help="Highlight connex groups of cards."
    )

    output_plugins = {
        output.keyword: output
        for output in plugins.iter_classes(dobbleoutput, dobbleoutput.DobbleOutput)
    }
    parser.add_argument(
        "-f",
        "--format",
        type=dobbleoutput.argparse_type_output,
        default="raw",
        help=(
            # pylint: disable=consider-using-f-string
            "Output format: {}.".format(
                ", ".join(
                    [
                        f"'{key}' ({plugins.get_description(output)})"
                        for key, output in output_plugins.items()
                    ]
                )
            )
        ),
    )

    return parser


def genere_jeu(algo, sub, num):
    """Génère un jeu."""

    base = algo.genere(num)

    jeu = Jeu()
    symboles = base.symboles
    for i in range(sub):
        for carte in base:
            nouvelle = Carte(groupe=i)
            for symbole in carte:
                nouvelle.symboles.append(symbole + i * len(symboles))
            jeu.cartes.append(nouvelle)

    return jeu


def process_arguments(arguments):
    """Traitement supplémentaire des arguments."""
    if arguments.num is None:
        arguments.num = arguments.algo.default["num"]
    if arguments.sub is None:
        arguments.sub = arguments.algo.default["sub"]

    return arguments


def main():
    """Fonction principale"""
    # Argument parsing
    arguments = process_arguments(analyse().parse_args())

    random.seed(arguments.random)
    jeu = genere_jeu(arguments.algo, arguments.sub, arguments.num)

    print(arguments.format.genere(jeu, groupe=arguments.group))


if __name__ == "__main__":
    main()
