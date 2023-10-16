#!/usr/bin/env python3

# Copyright 2018-2023 Louis Paternault
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

"""Calcul de la durée d'un jeu de bataille."""

import textwrap

import argdispatch

from jouets import bataille

from . import VERSION, Cache, graphiques, statistiques


def analyse():
    """Renvoie un analyseur de la ligne de commande."""
    # pylint: disable=line-too-long
    parser = argdispatch.ArgumentParser(
        prog="bataille",
        description=textwrap.dedent(
            """\
                Calcule la durée de parties de bataille, et manipule les résultats (affichage au format CSV, calcul de statistiques, tracé de graphiques…).

                Par défaut, simule une seule partie et affiche sa durée (en nombre de plis).
                """
        ),
        epilog=textwrap.dedent(
            """\
                # Simulations sauvegardées

                Si ces commandes sont appelées depuis le dépôt git, le résultat de certaines simulation (longues) est recherché dans des fichiers enregistré dans le dépôt plutôt que simulées à nouveau. Cela permet de gagner du temps.

                Utilisez `bataille cache` pour voir la liste des simulations disponibles.

                # Nombre de processeurs utilisés

                Les simulations sont faites en parallèle. Par défaut, autant de processus que de processeurs sont lancés. Pour modifier cette valeur, définir la variable d'environnement `WORKERS` au nombre de processeurs utilisés.
                """
        ),
        formatter_class=argdispatch.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}".format(version=VERSION),
    )
    parser.add_argument(
        "-c",
        "--couleurs",
        type=int,
        default=4,
        help="Nombre de couleurs du jeu de cartes.",
    )
    parser.add_argument(
        "-v",
        "--valeurs",
        type=int,
        default=13,
        help="Nombre de cartes dans chaque couleurs.",
    )

    subparsers = parser.add_subparsers()

    subparsers.add_function(bataille.affiche_brut, command="brut")
    subparsers.add_function(Cache.lscache, command="lscache")
    subparsers.add_function(graphiques.affiche, command="plot")
    subparsers.add_function(statistiques.stat)
    subparsers.add_function(statistiques.multistat)
    return parser


def main():
    """Fonction principale."""
    options = analyse().parse_args()
    print(bataille.partie(couleurs=options.couleurs, valeurs=options.valeurs))


if __name__ == "__main__":
    main()
