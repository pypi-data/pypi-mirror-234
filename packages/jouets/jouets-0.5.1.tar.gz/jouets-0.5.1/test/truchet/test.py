# Copyright 2023 Louis Paternault
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

import functools
import io
import multiprocessing
import os
import unittest

from jouets import truchet


@functools.cache
def catalan(n):
    if n == 0:
        return 1
    return sum(catalan(i) * catalan(n - 1 - i) for i in range(n))


# Taille maximale testée
TAILLE = 10


class TestCardinal(unittest.TestCase):
    """Vérification du nombre de solutions trouvées."""

    def test_unique(self):
        """Vérifie l'unicité des solutions"""
        for i in range(TAILLE):
            with self.subTest(i):
                tuiles = list(str(tuile) for tuile in truchet.tuiles(i))
                self.assertEqual(len(set(tuiles)), len(tuiles))

    def test_catalan(self):
        """Vérifie que le nombre de solutions trouvées est correct."""
        for i in range(TAILLE):
            with self.subTest(i):
                self.assertEqual(len(list(truchet.tuiles(i))), catalan(i))
