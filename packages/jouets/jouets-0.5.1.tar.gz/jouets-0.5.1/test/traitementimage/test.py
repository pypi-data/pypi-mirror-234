#!/usr/bin/env python3

# Copyright 2018-2021 Louis Paternault
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

"""Test de traitementimage."""

import os
import unittest

from PIL import Image, ImageChops

import jouets.traitementimage.__main__ as traitementimage

TESTDIR = os.path.dirname(__file__)


def sourcename():
    """Renvoit le nom de l'image source pour les tests."""
    return os.path.join(TESTDIR, "source.png")


def destname(function):
    """Renvoit le nom de l'image qui va être produite lors du test."""
    return os.path.join(TESTDIR, f"test-{function.__name__}.png")


def temoinname(function):
    """Renvoit le nom de l'image témoin."""
    return os.path.join(TESTDIR, f"temoin-{function.__name__}.png")


# pylint: disable=too-many-public-methods
class TestTransformations(unittest.TestCase):
    """Test des transformations"""

    def test(self):
        """Test des transformations"""
        for transformation in traitementimage.TRANSFORMATIONS:
            with self.subTest(transformation.__name__):
                transformation(sourcename(), destname(transformation))
                testimg = Image.open(destname(transformation))
                temoinimg = Image.open(temoinname(transformation))
                self.assertIsNone(ImageChops.difference(testimg, temoinimg).getbbox())


if __name__ == "__main__":
    unittest.main()
