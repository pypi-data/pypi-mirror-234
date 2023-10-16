# Copyright 2016 Louis Paternault
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

"""Calculs de probabilités de victoire selon le nombre de détectives."""

import sys

from jouets import mafia
from jouets.mafia import proba_soir
from jouets.utils.aargparse import analyseur, type_naturel
from jouets.utils.sphinx import affiche_tableau


def proba_mafieux_joueurs(detectives, max_joueurs):
    """Calcule les probabilités de victoire, selon différents nombre de joueurs et de mafieux.

    Pour un nombre de détectives donné.
    """
    tableau = [[None] * ((max_joueurs + 1) // 2 + 2) for _ in range(max_joueurs)]

    # Première ligne
    tableau[0][0] = "Mafieux \\ Joueurs"
    for n in range(max_joueurs - 1):
        tableau[n + 1][0] = n + 2

    for mafieux in range(0, (max_joueurs + 1) // 2 + 1):
        tableau[0][mafieux + 1] = mafieux
        for joueurs in range(2, max_joueurs + 1):
            if mafieux >= joueurs:
                tableau[joueurs - 1][mafieux + 1] = ""
            else:
                tableau[joueurs - 1][mafieux + 1] = "{:.1f}%".format(
                    100
                    * proba_soir(mafieux, joueurs - mafieux - detectives, detectives)
                )

    return tableau


def analyse():
    """Renvoie un analyseur de ligne de commande."""
    parser = analyseur(mafia.VERSION, prog="python -m jouets.mafia.probadetective")

    parser.add_argument(
        "-d", "--detectives", type=type_naturel, default=1, help="Number of detectives"
    )
    parser.add_argument(
        "-p",
        "--players",
        type=type_naturel,
        help="Maximum number of players.",
        required=True,
    )

    return parser


def main():
    """Fonction principale."""
    arguments = analyse().parse_args()

    sys.setrecursionlimit(sys.getrecursionlimit() + 4 * arguments.players)

    affiche_tableau(proba_mafieux_joueurs(arguments.detectives, arguments.players))


if __name__ == "__main__":
    main()
