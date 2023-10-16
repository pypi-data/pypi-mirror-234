# Copyright 2016-2022 Louis Paternault
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

"""Quelques fonctions à manipuler avec le générateur de documentation Sphinx."""


def affiche_tableau(tableau):
    """Convertit une liste de listes en un tableau au format Sphinx.

    >>> affiche_tableau([
    ... [1, "plop"],
    ... [False, 100],
    ... [None, 0],
    ... ])
    +------+-------+------+
    | 1    | False | None |
    +------+-------+------+
    | plop | 100   | 0    |
    +------+-------+------+
    """
    tailles = [max(len(str(item)) for item in colonne) for colonne in tableau]
    format_ligne = "| " + " | ".join([f"{{:{item}}}" for item in tailles]) + " |"
    separateur = (
        format_ligne.format(*[""] * len(tableau)).replace("|", "+").replace(" ", "-")
    )

    print(separateur)
    for ligne in range(len(tableau[0])):
        print(format_ligne.format(*(str(colonne[ligne]) for colonne in tableau)))
        print(separateur)
