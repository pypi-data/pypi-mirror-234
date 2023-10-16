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

"""Indique le nord par une flèche."""

from microbit import *

compass.calibrate()

while True:
    aiguille = compass.heading()

    if aiguille < 22.5:
        display.show(Image.ARROW_N)
    elif aiguille < 67.5:
        display.show(Image.ARROW_NW)
    elif aiguille < 112.5:
        display.show(Image.ARROW_W)
    elif aiguille < 157.5:
        display.show(Image.ARROW_SW)
    elif aiguille < 202.5:
        display.show(Image.ARROW_S)
    elif aiguille < 247.5:
        display.show(Image.ARROW_SE)
    elif aiguille < 292.5:
        display.show(Image.ARROW_E)
    elif aiguille < 337.5:
        display.show(Image.ARROW_NE)
    else:
        display.show(Image.ARROW_N)
