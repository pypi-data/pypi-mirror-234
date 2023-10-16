# Copyright 2016-2023 Louis Paternault
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

"""Calculs relatifs à la recherche de jeux équilibrés."""

import functools
import itertools
import sys

from jouets import mafia
from jouets.mafia import proba_soir
from jouets.utils.aargparse import analyseur, type_intervalle
from jouets.utils.sphinx import affiche_tableau


@functools.total_ordering
class Configuration:
    """Configuration de jeu (nombre de joueurs, et de rôles)."""

    def __init__(self, mafieux, detectives, joueurs):
        self.mafieux = mafieux
        self.detectives = detectives
        self.joueurs = joueurs
        self.proba = proba_soir(mafieux, joueurs - mafieux - detectives, detectives)

    def __eq__(self, other):
        return (
            self.mafieux == other.mafieux
            and self.detectives == other.detectives
            and self.joueurs == other.joueurs
        )

    def __lt__(self, other):
        if self == other:
            return (self.mafieux, self.detectives, self.joueurs) < (
                other.mafieux,
                other.detectives,
                other.joueurs,
            )
        return self.proba < other.proba


def equilibre(intervalle_joueurs, intervalle_detectives):
    """Calcule le nombre de mafieux et détectives nécessaires pour approcher le jeu équitable."""

    tableau = [["Joueurs", "Défaut", "Excès"]]

    for joueurs in range(*intervalle_joueurs):
        configurations = [
            Configuration(mafieux, detectives, joueurs)
            for mafieux, detectives in itertools.product(
                range(0, intervalle_joueurs[1] // 2 + 1), range(*intervalle_detectives)
            )
            if mafieux + detectives <= joueurs
        ]
        try:
            exces = min((conf for conf in configurations if conf.proba >= 0.5))
        except ValueError:
            exces = Configuration(joueurs, joueurs, 0)

        try:
            defaut = max((conf for conf in configurations if conf.proba <= 0.5))
        except ValueError:
            defaut = Configuration(joueurs, 0, joueurs)

        tableau.append(
            [
                joueurs,
                "{:.1f}% ({}m, {}d)".format(
                    100 * defaut.proba, defaut.mafieux, defaut.detectives
                ),
                "{:.1f}% ({}m, {}d)".format(
                    100 * exces.proba, exces.mafieux, exces.detectives
                ),
            ]
        )

    return tableau


def analyse():
    """Renvoie un analyseur de ligne de commande."""
    parser = analyseur(mafia.VERSION, prog="python -m jouets.mafia.equilibre")

    parser.add_argument(
        "-d",
        "--detectives",
        type=type_intervalle,
        default=[None, None],
        help="Number of detectives, in the form MIN:MAX.",
    )
    parser.add_argument(
        "-p",
        "--players",
        type=type_intervalle,
        help="Number of players, in the forms MIN:MAX.",
        required=True,
    )

    return parser


def main():
    """Fonction principale."""
    arguments = analyse().parse_args()

    if arguments.players[0] is None:
        arguments.players[0] = 2
    if arguments.players[1] is None:
        sys.stderr.write("Error: No maximum number of players specified.")
        sys.exit(1)
    else:
        arguments.players[1] += 1

    if arguments.detectives[0] is None:
        arguments.detectives[0] = 0
    if arguments.detectives[1] is None:
        arguments.detectives[1] = arguments.players[1]
    else:
        arguments.detectives[1] += 1

    sys.setrecursionlimit(sys.getrecursionlimit() + 4 * arguments.players[1])

    affiche_tableau(equilibre(arguments.players, arguments.detectives))


if __name__ == "__main__":
    main()
