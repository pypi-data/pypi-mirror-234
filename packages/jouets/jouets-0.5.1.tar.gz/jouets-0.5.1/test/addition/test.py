#!/usr/bin/env python3

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

"""Test de addition"""

import unittest

from jouets import addition


# pylint: disable=too-many-public-methods
class TestAddition(unittest.TestCase):
    """Vérification des solutions"""

    def test_egal(self):
        """Vérifie que tous les algorithmes donnent le même résultat."""
        # Les fonctions addition1 et addition2 ne sont pas testées :
        # chacune met une dizaine de minutes à être exécutées.
        # C'est trop long.
        temoin = set(addition.addition6())
        for fonction in (addition.addition3, addition.addition4, addition.addition5):
            self.assertEqual(temoin, set(fonction()))
