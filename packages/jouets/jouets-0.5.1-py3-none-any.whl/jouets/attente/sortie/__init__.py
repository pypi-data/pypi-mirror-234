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

"""Différents affichages au cours de la simulation."""


class Sortie:
    """Classe abstraite de laquelle héritent tous les affichages."""

    def __init__(self, salle):
        self.salle = salle

    def debut(self):
        """Appelé au début de la simulation."""

    def fin(self):
        """Appelée à la fin de la simulation."""

    def entree(self, usager):
        """L'usager entre dans la salle."""

    def suivant(self, usager):
        """L'usager passe de sa file au guichet."""

    def sortie(self, usager):
        """L'usager quitte la salle."""

    def tictac(self):
        """La simulation avance d'une unité de temps."""
