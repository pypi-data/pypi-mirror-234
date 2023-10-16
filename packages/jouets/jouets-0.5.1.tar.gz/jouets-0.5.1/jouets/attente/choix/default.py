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

"""Quelques stratégies de choix de file par un usager entrant dans la salle."""

import random

from . import Choix


class Personnes(Choix):
    """File la plus courte en nombre de personnes."""

    keyword = "personnes"

    def entre(self, usager):
        try:
            # Y a-t-il un guichet de libre ?
            numero = self.guichets.index(None) * len(self.files) // len(self.guichets)
        except ValueError:
            # Recherche de la file comportant le moins de personnes
            numero = list(sorted((len(file), i) for i, file in enumerate(self.files)))[
                0
            ][1]

        self.files[numero].nouveau(usager)


class Temps(Choix):
    """File la plus courte en temps d'attente."""

    keyword = "temps"

    def entre(self, usager):
        try:
            # Y a-t-il un guichet de libre ?
            numero = self.guichets.index(None) * len(self.files) // len(self.guichets)
        except ValueError:
            # Recherche de la file la plus courte en nombre de personnes.
            # Remarque :
            # Ceci ne tient pas compte du temps restant à la personne au guichet.
            # Cela pourrait être amélioré.
            temps = [
                (sum(usager.service for usager in file), i)
                for i, file in enumerate(self.files)
            ]
            numero = min(temps)[1]

        self.files[numero].nouveau(usager)


class Hasard(Choix):
    """Choix d'une file au hasard."""

    keyword = "hasard"

    def entre(self, usager):
        self.files[random.randint(0, len(self.files) - 1)].nouveau(usager)
