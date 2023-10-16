#!/usr/bin/env python3

# Copyright 2014-2020 Louis Paternault
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

"""Crible d'Érathostène optimisé en mémoire"""

import sys

from jouets.erathostene import premiers
from jouets.utils.aargparse import analyseur

VERSION = "0.2.0"


def _affiche_premiers():
    """Affiche les nombres premiers."""
    try:
        for premier in premiers():
            print(premier)
    except KeyboardInterrupt:
        sys.exit(0)
    except BrokenPipeError:
        sys.exit(0)


def analyse():
    """Renvoie un analyseur de la ligne de commande."""
    return analyseur(
        VERSION,
        description="Affiche les nombres premiers.",
        epilog="This program prints prime numbers until it is killed.",
    )


def main():
    """Fonction principale"""
    analyse().parse_args(sys.argv[1:])
    _affiche_premiers()


if __name__ == "__main__":
    main()
