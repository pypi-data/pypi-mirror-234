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

"""Chute libre d'un solide

En utilisant la méthode d'Euler.
"""

# pylint: disable=invalid-name, missing-function-docstring

import turtle


def main():
    # Position initiale
    px, py = 0, 0
    # Vitesse initiale
    vx, vy = 5, 40
    # Accélération (qui est constante)
    ax, ay = 0, -9.81

    h = 0.01

    while True:
        # Application de la méthose d'Euler
        px, py, vx, vy = (px + h * vx, py + h * vy, vx + h * ax, vy + h * ay)

        # Rebond
        if py < 0:
            py = -py
            vy = -0.9 * vy

        # Tracé
        turtle.goto(px, py)  # pylint: disable=no-member


if __name__ == "__main__":
    main()
