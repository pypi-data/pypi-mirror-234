# Copyright 2020 Louis Paternault
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

"""Test de anagrammes.clique"""

import unittest

from jouets.anagrammes.clique import recherche

DICTIONNAIRE = {"Chine", "Marie", "aimer", "chien", "niche", "niché"}


# pylint: disable=too-many-public-methods
class TestClique(unittest.TestCase):
    """Test de la recherche de groupes d'anagrammes."""

    def test_recherche(self):
        """Test générique"""
        self.assertEqual(
            list(recherche(DICTIONNAIRE, accents=False, majuscules=True)),
            [{"Chine", "chien", "niche", "niché"}],
        )

    def test_accents(self):
        """Test l'argument `accents`."""
        with self.subTest("Avec accents"):
            self.assertEqual(
                list(recherche(DICTIONNAIRE, accents=True, majuscules=True)),
                [{"Chine", "chien", "niche"}],
            )

        with self.subTest("Sans accents"):
            self.assertEqual(
                list(recherche(DICTIONNAIRE, accents=False, majuscules=True)),
                [{"Chine", "chien", "niche", "niché"}],
            )

    def test_majuscules(self):
        """Test l'argument `majuscules`."""
        with self.subTest("Avec majuscules"):
            self.assertEqual(
                list(recherche(DICTIONNAIRE, accents=True, majuscules=True)),
                [{"Chine", "chien", "niche"}],
            )

        with self.subTest("Sans majuscules"):
            self.assertEqual(
                list(recherche(DICTIONNAIRE, accents=True, majuscules=False)),
                [{"chien", "niche"}],
            )
