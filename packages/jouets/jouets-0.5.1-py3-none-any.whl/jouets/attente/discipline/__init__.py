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

"""Organisation des usagers dans la file : quel usager passe en premier ?"""


class Discipline:
    """File d'usagers."""

    def __len__(self):
        raise NotImplementedError()

    def __iter__(self):
        raise NotImplementedError()

    def nouveau(self, usager):
        """Ajoute un nouvel usager à la file."""
        raise NotImplementedError()

    def suivant(self):
        """Renvoit (et enlève) le prochain usager de la file."""
        raise NotImplementedError()

    @property
    def vide(self):
        """Renvoit `True` si la file est vide."""
        raise NotImplementedError()


class Liste(Discipline):
    """Gestion interne par une liste"""

    def __init__(self):
        self._liste = []

    def __len__(self):
        return len(self._liste)

    def __iter__(self):
        yield from self._liste

    def nouveau(self, usager):
        self._liste.append(usager)

    def suivant(self):
        try:
            return self._liste.pop()
        except IndexError:
            return None

    @property
    def vide(self):
        return not self._liste
