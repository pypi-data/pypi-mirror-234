# Copyright 2012-2015 Louis Paternault
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

"""Test de la résolution de grilles."""

import io
import multiprocessing
import os
import unittest

from jouets.sudoku.io import charge_fichier
from jouets.sudoku.representation import Grille
from jouets.sudoku.resolution import resout

TEMOINS = [
    {
        "short": False,
        "problem": """\
            . . 9 . 8 6 . 4 1
            5 2 . . . 3 . 7 .
            4 . . . 2 . 3 . .
            6 . 2 8 3 1 7 9 5
            . . 5 2 7 4 6 . .
            8 3 7 6 9 5 1 . 4
            . . 4 . 6 . . . 2
            . 5 . 9 . . . 6 3
            . . . . . . . . .
            """,
        "solutions": [
            [
                [2, 6, 8, 4, 7, 5, 1, 3, 0],
                [4, 1, 5, 0, 3, 2, 7, 6, 8],
                [3, 7, 0, 6, 1, 8, 2, 4, 5],
                [5, 3, 1, 7, 2, 0, 6, 8, 4],
                [8, 0, 4, 1, 6, 3, 5, 2, 7],
                [7, 2, 6, 5, 8, 4, 0, 1, 3],
                [0, 8, 3, 2, 5, 6, 4, 7, 1],
                [6, 4, 7, 8, 0, 1, 3, 5, 2],
                [1, 5, 2, 3, 4, 7, 8, 0, 6],
            ],
            [
                [2, 6, 8, 4, 7, 5, 1, 3, 0],
                [4, 1, 5, 0, 3, 2, 7, 6, 8],
                [3, 7, 0, 6, 1, 8, 2, 4, 5],
                [5, 3, 1, 7, 2, 0, 6, 8, 4],
                [8, 0, 4, 1, 6, 3, 5, 2, 7],
                [7, 2, 6, 5, 8, 4, 0, 1, 3],
                [6, 8, 3, 2, 5, 7, 4, 0, 1],
                [1, 4, 7, 8, 0, 6, 3, 5, 2],
                [0, 5, 2, 3, 4, 1, 8, 7, 6],
            ],
            [
                [2, 6, 8, 4, 7, 5, 1, 3, 0],
                [4, 1, 5, 0, 3, 2, 7, 6, 8],
                [3, 7, 0, 6, 1, 8, 2, 4, 5],
                [5, 3, 1, 7, 2, 0, 6, 8, 4],
                [0, 8, 4, 1, 6, 3, 5, 2, 7],
                [7, 2, 6, 5, 8, 4, 0, 1, 3],
                [8, 0, 3, 2, 5, 6, 4, 7, 1],
                [6, 4, 7, 8, 0, 1, 3, 5, 2],
                [1, 5, 2, 3, 4, 7, 8, 0, 6],
            ],
        ],
    },
    {
        "short": True,
        "problem": "...232....4....1",
        "solutions": [[[0, 3, 2, 1], [2, 1, 0, 3], [1, 0, 3, 2], [3, 2, 1, 0]]],
    },
    {
        "short": False,
        "problem": """\
            . . . 2
            3 2 . .
            . . 4 .
            . . . 1
            """,
        "solutions": [[[0, 3, 2, 1], [2, 1, 0, 3], [1, 0, 3, 2], [3, 2, 1, 0]]],
    },
    {
        "short": False,
        "problem": """\
                6 1 2 . . . 8 . 3
                . 4 . 7 . . . . .
                . . . . . . . . .
                . . . 5 . 4 . 7 .
                3 . . 2 . . . . .
                1 . 6 . . . . . .
                . 2 . . . . . 5 .
                . . . . 8 . 6 . .
                . . . . 1 . . . .
            """,
        "solutions": [],
    },
    {
        "short": False,
        "problem": """\
            8 5 . . . 2 4 . .
            7 2 . . . . . . 9
            . . 4 . . . . . .
            . . . 1 . 7 . . 2
            3 . 5 . . . 9 . .
            . 4 . . . . . . .
            . . . . 8 . . 7 .
            . 1 7 . . . . . .
            . . . . 3 6 . 4 .
            """,
        "solutions": [
            [
                [7, 4, 8, 5, 0, 1, 3, 2, 6],
                [6, 1, 2, 7, 4, 3, 0, 5, 8],
                [0, 5, 3, 2, 6, 8, 4, 1, 7],
                [8, 7, 5, 0, 3, 6, 2, 4, 1],
                [2, 6, 4, 1, 5, 7, 8, 0, 3],
                [1, 3, 0, 4, 8, 2, 6, 7, 5],
                [3, 2, 1, 8, 7, 0, 5, 6, 4],
                [5, 0, 6, 3, 1, 4, 7, 8, 2],
                [4, 8, 7, 6, 2, 5, 1, 3, 0],
            ]
        ],
    },
    {
        "short": False,
        "problem": """\
            8 5 . . . 2 4 . .
            7 2 . . . . . . 9
            . . 4 . . . . . .
            . . . 1 . 7 . . 2
            3 . 5 . . . 9 . .
            . 4 . . . . . . .
            . . . . 8 . . 7 .
            . 1 7 . . . . . .
            . . . . 3 6 . 4 .
            """,
        "solutions": [
            [
                [7, 4, 8, 5, 0, 1, 3, 2, 6],
                [6, 1, 2, 7, 4, 3, 0, 5, 8],
                [0, 5, 3, 2, 6, 8, 4, 1, 7],
                [8, 7, 5, 0, 3, 6, 2, 4, 1],
                [2, 6, 4, 1, 5, 7, 8, 0, 3],
                [1, 3, 0, 4, 8, 2, 6, 7, 5],
                [3, 2, 1, 8, 7, 0, 5, 6, 4],
                [5, 0, 6, 3, 1, 4, 7, 8, 2],
                [4, 8, 7, 6, 2, 5, 1, 3, 0],
            ]
        ],
    },
]


def cherche_solutions(probleme, short, process=1):
    """Renvoit la liste des solutions au problème"""
    if short:
        format_fichier = "short"
    else:
        format_fichier = "long"
    with multiprocessing.Manager() as manager:  # pylint: disable=no-member
        solutions = manager.list()
        resout(
            Grille(charge_fichier(probleme, format_fichier)), solutions.append, process
        )
        return [grille.case for grille in solutions]


def transpose(matrice):
    """Renvoit la transposée de la matrice

    Les matrices sont représentées par des listes de listes.
    """
    return [[matrice[x][y] for x in range(len(matrice))] for y in range(len(matrice))]


# pylint: disable=too-many-public-methods
class TestResout(unittest.TestCase):
    """Test de résolution"""

    def test_resout(self, process=1):
        """Resolution"""
        for temoin in TEMOINS:
            solutions = cherche_solutions(
                io.StringIO(temoin["problem"]), temoin["short"], process
            )
            self.assertListEqual(
                sorted(solutions),
                sorted([transpose(sol) for sol in temoin["solutions"]]),
            )

    def test_processus(self):
        """Lance énormément de processus, pour vérifier qu'il n'y a pas de conflits."""
        return self.test_resout(process=os.cpu_count() * 10)


if __name__ == "__main__":
    unittest.main()
