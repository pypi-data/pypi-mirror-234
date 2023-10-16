# Copyright 2020-2023 Louis Paternault
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

"""Calcul de la probabilité de victoire au jeu du verger"""

import argparse
import textwrap

from . import STRATEGIES, VERSION, probabilite


def analyse():
    """Renvoie un analyseur de la ligne de commande."""
    # pylint: disable=line-too-long
    parser = argparse.ArgumentParser(
        prog="verger",
        description="""Calcule la probabilité de victorie au jeu du Verger (Haba).""",
        epilog=textwrap.dedent(
            """
        # Cache

        Un cache est utilisé pour accélérer les calculs. Sa taille est définie en définissant la variable d'environnement `VERGER_CACHE_SIZE`:

        - si cette chaîne est vide, la taille du cache est infini (limitée par les capacités de l'ordinateur) ;
        - si cette variable est un nombre, elle définit la taille du cache ;
        - si cette variable est autre chose, ou non définie, la taille du cache est 2^1000.
        """
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
    )
    parser.add_argument(
        "-a",
        "--arbres",
        type=int,
        default=4,
        help="Nombre d'arbres (nombre de types de fruits différents).",
    )
    parser.add_argument(
        "-f", "--fruits", type=int, default=10, help="Nombre de fruits par arbre."
    )
    parser.add_argument(
        "-c",
        "--corbeau",
        type=int,
        default=9,
        help="Nombre de pièces du puzzle du corbeau.",
    )
    parser.add_argument(
        "-p",
        "--panier",
        default="max",
        choices=list(STRATEGIES.keys()),
        help="Stratégie à utiliser : "
        + ", ".join(
            "{} ({})".format(key, value.__doc__.strip().split("\n", maxsplit=1)[0])
            for key, value in STRATEGIES.items()
        ),
    )

    return parser


def main():
    """Fonction principale."""
    options = analyse().parse_args()
    print(options)
    print(
        probabilite(
            options.corbeau,
            STRATEGIES[options.panier],
            *(options.fruits for _ in range(options.arbres)),
        )
    )


if __name__ == "__main__":
    main()
