#!/usr/bin/env python3

# Copyright 2014-2023 Louis Paternault
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

"""Trajectoire d'un satellite

Résolution des équations modélisant la trajectoire d'un satellite avec la méthode d'Euler."""

# pylint: disable=invalid-name, no-member, missing-function-docstring

import turtle
from math import atan2, cos, sin


def main():
    # Position initiale (à droite)
    px, py = 250, 0
    # Vitesse initiale (perpendiculaire à l'axe étoile-satellite)
    vx, vy = 0, 40
    # Accélération initiale (nulle, mais c'est sans importance)
    ax, ay = 0, 0
    # Composante M×m×G de la gravité (unité arbitraire)
    f = 1000000

    h = 0.001

    turtle.delay(0.1)
    turtle.up()
    turtle.goto(px, py)
    turtle.down()

    while True:
        # Calcul de la gravité
        gravite = f / (px**2 + py**2)
        # Calcul de l'angle entre l'étoile et son satellite
        angle = atan2(py, px)

        px, py, vx, vy, ax, ay = (
            px + h * vx,
            py + h * vy,
            vx + h * ax,
            vy + h * ay,
            -gravite * cos(angle),
            -gravite * sin(angle),
        )

        turtle.goto(px, py)


if __name__ == "__main__":
    main()
