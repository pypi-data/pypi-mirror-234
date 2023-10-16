# Copyright 2019 Louis Paternault
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

"""Trace une ligne horizontale."""

import math

from microbit import *

CROIX = Image("90009:09090:00900:09090:90009")


def tracedroite(a, b):
    """Trace une droite d'équation cartésienne ax+by=0"""
    display.clear()
    if a == b == 0:
        display.show(CROIX)
    elif abs(a) < abs(b):
        for x in range(-2, 3):
            display.set_pixel(x + 2, round(-a * x / b) + 2, 9)
    else:  # abs(b) < abs(a)
        for y in range(-2, 3):
            display.set_pixel(round(-b * y / a) + 2, y + 2, 9)


while True:
    # Récupère les données de l'accéléromètre
    x = accelerometer.get_x()
    y = accelerometer.get_y()
    z = accelerometer.get_z()

    # Convertit les mesures de l'accéléromètre en angles
    angleX = math.atan2(-x, z)
    angleY = math.atan2(-y, z)

    # Trace la droite horizontale
    tracedroite(
        math.sin(angleX) * math.cos(angleY), math.cos(angleX) * math.sin(angleY)
    )
