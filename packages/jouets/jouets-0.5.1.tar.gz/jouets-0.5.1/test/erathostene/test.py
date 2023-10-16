#!/usr/bin/env python3

# Copyright 2014-2015 Louis Paternault
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

"""Test de erathostene.py"""

import unittest
from itertools import islice

from jouets.erathostene import est_premier, premiers

from .temoin import TEMOIN


# pylint: disable=too-many-public-methods
class TestPremiers(unittest.TestCase):
    """Vérification de la liste des nombres générés"""

    def test_generateur(self):
        """Vérification des 1000 premiers nombres générés."""
        self.assertListEqual(TEMOIN, list(islice(premiers(), len(TEMOIN))))

    def test_test(self):
        """Test de la fonction de test."""
        for nombre in [2, 3, 6073]:
            self.assertTrue(est_premier(nombre))

        for nombre in [4, 38, 1000]:
            self.assertFalse(est_premier(nombre))


if __name__ == "__main__":
    unittest.main()
