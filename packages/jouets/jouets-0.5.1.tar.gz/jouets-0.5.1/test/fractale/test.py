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

"""Test de fractale.py"""

# pylint: disable=import-outside-toplevel

import unittest
from itertools import islice

# pylint: disable=unused-import
from .temoin import TEMOIN


# pylint: disable=too-many-public-methods
class TestAngles(unittest.TestCase):
    """Vérification de la liste des nombres générés"""

    def test_koch(self):
        """Vérification des 1000 premiers nombres générés."""
        from jouets.fractale.__main__ import Fractale
        from jouets.fractale.options import PREDEFINED

        self.assertListEqual(
            TEMOIN, list(islice(iter(Fractale(PREDEFINED["koch"])), len(TEMOIN)))
        )


if __name__ == "__main__":
    unittest.main()
