# Copyright 2020 Louis Paternault
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

"""Quelques lois de probabilité."""

import random

from . import LoiProba


class Uniforme(LoiProba):
    """Loi de probabilité uniforme (arguments : "min:max")."""

    # pylint: disable=too-few-public-methods

    keyword = "uniforme"

    def __init__(self, *args):
        self.bornes = int(args[0]), int(args[1])

    def random(self):
        return random.randint(*self.bornes)


class Normale(LoiProba):
    """Loi de probabilité normale (arguments : "moyenne:écart-type")."""

    # pylint: disable=too-few-public-methods

    keyword = "normale"

    def __init__(self, *args):
        self.moyenne = float(args[0])
        self.ecarttype = float(args[1])

    def random(self):
        valeur = int(round(random.normalvariate(self.moyenne, self.ecarttype)))
        if valeur < 1:
            return 1
        return valeur


class Exponentielle(LoiProba):
    """Loi de probabilité exponentielle (arguments : "moyenne")."""

    # pylint: disable=too-few-public-methods

    keyword = "exp"

    def __init__(self, *args):
        self.moyenne = float(args[0])

    def random(self):
        valeur = int(round(random.expovariate(1 / self.moyenne)))
        if valeur < 1:
            return 1
        return valeur


class Constante(LoiProba):
    """Renvoit toujours la même valeur (celle donnée en argument)."""

    # pylint: disable=too-few-public-methods

    keyword = "constante"

    def __init__(self, *args):
        self.constante = int(args[0])

    def random(self):
        return self.constante
