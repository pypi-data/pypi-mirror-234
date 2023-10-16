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

"""Système masse-ressort

Résolution des équations modélisant un ressort amorti en utilisant la méthode d'Euler.
"""

# pylint: disable=invalid-name, no-member, missing-function-docstring

import turtle


def main():
    # Allongement
    x = 300
    # Vitesse
    v = 0
    # Accélération
    a = 0
    # Temps
    t = 0

    # Coefficient de frottement
    f = 0.5
    # Coefficient de la force de rappel
    k = 20

    h = 0.001

    turtle.tracer(8, 1)
    turtle.up()
    turtle.goto(t, x)
    turtle.down()

    while True:
        t += 0.02

        x, v, a = (x + h * v, v + h * a, -f * v - k * x)

        turtle.goto(t, x)


if __name__ == "__main__":
    main()
