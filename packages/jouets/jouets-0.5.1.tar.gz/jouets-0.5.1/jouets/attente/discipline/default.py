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

"""Quelques stratégies de gestion de files d'usagers."""

import random

from . import Liste


class FIFO(Liste):
    """Premier arrivé, premier servi."""

    keyword = "fifo"

    def suivant(self):
        try:
            return self._liste.pop(0)
        except IndexError:
            return None


class LIFO(FIFO):
    """Premier arrivé, dernier servi."""

    keyword = "lifo"

    def nouveau(self, usager):
        self._liste.insert(0, usager)


class Rapide(FIFO):
    """Le plus rapide passe en premier"""

    keyword = "rapide"

    def nouveau(self, usager):
        for i, autre in enumerate(self._liste):
            if usager.service < autre.service:
                self._liste.insert(i, usager)
                return
        self._liste.append(usager)


class Lent(Rapide):
    """Le plus lent passe en premier"""

    keyword = "lent"

    def nouveau(self, usager):
        for i, autre in enumerate(self._liste):
            if usager.service > autre.service:
                self._liste.insert(i, usager)
                return
        self._liste.append(usager)


class Hasard(FIFO):
    """Une personne au hasard est choisie."""

    keyword = "hasard"

    def suivant(self):
        if len(self._liste) == 0:
            return None
        return self._liste.pop(random.randint(0, len(self._liste) - 1))
