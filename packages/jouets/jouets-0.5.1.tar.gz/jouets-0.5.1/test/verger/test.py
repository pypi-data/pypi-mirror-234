# Copyright 2016 Louis Paternault
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

"""Test de mafia"""

import unittest

from jouets.verger import STRATEGIES, probabilite

TEMOINS = [
    ((2, STRATEGIES["max"], 2, 2), 0.677),
    ((9, STRATEGIES["max"], 10, 10, 10, 10), 0.684),
    ((1, STRATEGIES["max"], 1), 0.667),
]


# pylint: disable=too-many-public-methods
class TestProba(unittest.TestCase):
    """Vérification de quelques cas particuliers"""

    def test_proba(self):
        """Vérification de quelques cas particuliers"""
        for args, proba in TEMOINS:
            with self.subTest(args=args, proba=proba):
                self.assertAlmostEqual(probabilite(*args), proba, places=3)
