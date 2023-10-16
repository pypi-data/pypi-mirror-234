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

"""Émulateur rudimentaire de micro:bit.

Pour le moment, il émule juste une partie de l'affichage à l'écran.

Utilisé pour tester des programmes micro:bit sur l'ordinateur.
"""

import time

DISPLAY_SIZE = 5


class Display:
    """Affichage à l'écran."""

    def __init__(self):
        self.clear()

    def _refresh(self):
        print()
        print()
        print()
        for y in range(DISPLAY_SIZE):
            for x in range(DISPLAY_SIZE):
                print(self._screen[x][y], end="")
            print()

    def set_pixel(self, x, y, value):
        """Change la luminosité d'un pixel."""
        self._screen[x][y] = value
        self._refresh()

    def get_pixel(self, x, y):
        """Renvoit la luminosité d'un pixel."""
        return self._screen[x][y]

    def clear(self):
        """Efface l'écran."""
        self._screen = [[0 for _ in range(DISPLAY_SIZE)] for _ in range(DISPLAY_SIZE)]
        self._refresh()


display = Display()


def sleep(n):
    """Attent n millisecondes."""
    time.sleep(n / 1000)


__all__ = ["display", "sleep"]
