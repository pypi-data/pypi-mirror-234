#!/usr/bin/env python3

# Copyright 2019 Louis Paternault
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

# pylint: disable=invalid-name

"""Calcul du score maximal à Azul"""

import textwrap

from jouets.utils.aargparse import analyseur

VERSION = "0.1.0"


def analyse():
    """Renvoie un analyseur de la ligne de commande."""
    parser = analyseur(
        VERSION,
        prog="azul",
        description="Calcule le score maximal à Azul.",
        epilog=textwrap.dedent(
            """
            Pour les explications du calcul de ce score, voir :
            http://jouets.ababsurdo.fr/fr/latest/azul.
            """
        ),
    )
    return parser


def score_maximal():
    """Renvoit le score maximal d'une partie d'Azul."""
    return 245


def main():
    """Fonction principale

    Prend en argument les arguments de la ligne de commande.
    """
    analyse().parse_args()
    print(score_maximal())


if __name__ == "__main__":
    main()
