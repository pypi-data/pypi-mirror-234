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

"""Création et vérification de jeux de cartes de Dobble"""

import argparse
import sys
import textwrap

from jouets.dobble import VERSION, CarteDobble, JeuDobble, genere_jeu
from jouets.dobble import output as dobbleoutput
from jouets.utils import plugins
from jouets.utils.aargparse import analyseur


class ErreurSymboles(Exception):
    """Erreur dans la définition des symboles à utiliser."""

    def __init__(self, message):
        super().__init__()
        self.message = message

    def __str__(self):
        return self.message


def command_check(arguments):
    """Gestion de la sous-commande 'check'.

    :param arguments: `namespace` renvoyé par :func:`argparse.parse`.
    :return: Le *status code* à retourner par le programme.
    """
    jeu = analyse_fichier(arguments.file)
    if not arguments.show:
        arguments.show = ["valid"]
    if not arguments.quiet:
        if "summary" in arguments.show:
            arguments.show.extend(["trivial", "regular", "valid"])
            summary = ""
            summary += f"Symbols ({len(jeu.frequences_symboles.keys())})"
            summary += "".join(
                [
                    f"\n\t{key}: {value}"
                    for (key, value) in sorted(jeu.frequences_symboles.items())
                ]
            )
            summary += "\n"
            summary += f"Cards ({len(jeu.cartes)})"
            summary += "".join(["\n\t" + str(carte) for carte in sorted(jeu)])
            summary += "\n"
            cartes_invalides = jeu.cartes_invalides()
            summary += f"Invalid cards ({len(cartes_invalides)})"
            summary += "".join(
                ["\n\t" + str(carte) for carte in sorted(cartes_invalides)]
            )
            summary += "\n"
            couples_cartes_invalides = jeu.couples_cartes_invalides()
            summary += f"Invalid card couples ({len(couples_cartes_invalides)})"
            summary += "".join(
                [
                    "\n\t" + str(card1) + " | " + str(card2)
                    for (card1, card2) in sorted(couples_cartes_invalides)
                ]
            )
            print(summary)

    quiet_status = True
    for check, value in [
        ("valid", jeu.valide),
        ("regular", jeu.regulier),
        ("trivial", jeu.trivial),
    ]:
        if check in arguments.show:
            quiet_status = quiet_status and value
            print(f"{check}: ")
            if value:
                print("yes")
            else:
                print("no")

    if not arguments.quiet:
        return 0
    if quiet_status:
        return 0
    return 1


def analyse_fichier(fileobject):
    """Analyse le fichier donné.

    :param file fileobject: Fichier à analyser.
    :return: Un jeu.
    :rtype: :class:`Jeu`
    """
    jeu = JeuDobble()
    for ligne in fileobject:
        if ligne.strip():
            jeu.cartes.append(CarteDobble(ligne.split()))
    return jeu


def analyse():
    """Renvoie un analyseur de ligne de commande."""
    parser = analyseur(VERSION, prog="dobble")
    subparsers = parser.add_subparsers(title="Commands", dest="command")
    subparsers.required = True
    subparsers.dest = "command"

    # Check
    check = subparsers.add_parser(
        "check",
        help="Check properties about the game (default is validity).",
        description="Check properties about the game.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """\
                Syntax
                  Games are given line per line: each line is a different
                  card (blank lines are ignored). Each card is a white
                  space separated list of symbols (a symbol can be any
                  string not containing white spaces).
                """
        ),
    )
    check.add_argument(
        "-f",
        "--file",
        nargs="?",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="Input file. Default is standard input.",
    )
    check.add_argument(
        "-r",
        "--regular",
        dest="show",
        action="append_const",
        const="regular",
        help=("Check if game is regular."),
    )
    check.add_argument(
        "-v",
        "--valid",
        dest="show",
        action="append_const",
        const="valid",
        help=("Check if game is valid."),
    )
    check.add_argument(
        "-t",
        "--trivial",
        dest="show",
        action="append_const",
        const="trivial",
        help=("Check if game is trivial."),
    )
    check.add_argument(
        "-s",
        "--summary",
        dest="show",
        action="append_const",
        const="summary",
        default=False,
        help="Print somme information about the game.",
    )
    check.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help=(
            "Does not print anything: exit status is 0 if condition are met, "
            "1 otherwise."
        ),
    )

    # Build
    build = subparsers.add_parser(
        "build",
        help="Build some game.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    build.add_argument(
        "-s",
        "--size",
        dest="size",
        action="store",
        type=int,
        required=True,
        help=("Size of the game."),
    )

    output_plugins = {
        output.keyword: output
        for output in plugins.iter_classes(dobbleoutput, dobbleoutput.DobbleOutput)
    }

    build.add_argument(
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


def main():
    """Fonction principale"""
    # Argument parsing
    arguments = analyse().parse_args(sys.argv[1:])

    # Running subcommands
    if arguments.command == "check":
        status = command_check(arguments)
    elif arguments.command == "build":
        print(arguments.format.genere(genere_jeu(arguments.size)))
        status = 0
    else:
        status = 1

    # End
    return status


if __name__ == "__main__":
    main()
