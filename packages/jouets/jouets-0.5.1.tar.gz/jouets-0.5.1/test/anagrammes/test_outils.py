# Copyright 2018 Louis Paternault
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

"""Test de anagrammes"""

import unittest

from jouets.anagrammes import Alphabet, Intervalle


# pylint: disable=too-many-public-methods
class TestAlphabet(unittest.TestCase):
    """Tests pour la classe Alphabet."""

    def test_definition(self):
        """Définition d'un alphabet."""
        alphabet = Alphabet("aabc")
        self.assertEqual(alphabet["a"], 2)
        self.assertEqual(alphabet["b"], 1)
        self.assertEqual(alphabet["c"], 1)
        self.assertEqual(alphabet["d"], 0)

    def test_operations(self):
        """Opérations sur un alphabet."""
        alphabet = Alphabet("aabc")
        alphabet = alphabet - "a"
        alphabet = alphabet - "b"

        self.assertEqual(alphabet["a"], 1)
        self.assertEqual(alphabet["b"], 0)

        self.assertIn("a", alphabet)
        self.assertNotIn("b", alphabet)
        self.assertTrue(alphabet)

        alphabet = alphabet - "a"
        alphabet = alphabet - "c"
        self.assertFalse(alphabet)


class TestIntervalle(unittest.TestCase):
    """Test de la classe Intervalle"""

    def test_intervalle(self):
        """Test de la classe Intervalle"""
        self.assertEqual(Intervalle(2, 3) - 1, Intervalle(1, 2))
        self.assertEqual(Intervalle(2, 3) + 1, Intervalle(3, 4))
        self.assertEqual(Intervalle(None, 3) + 1, Intervalle(None, 4))
        self.assertEqual(Intervalle(3, None) + 1, Intervalle(4, None))
