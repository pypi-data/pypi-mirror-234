# Copyright 2020-2021 Louis Paternault
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

"""Quelques affichages au cours de la simulation de file d'attente."""

import statistics

import numpy

from . import Sortie


class MoyenneEcarttype(Sortie):
    """Moyenne et Écart-type"""

    keyword = "moyenne"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._attentes = []

    def suivant(self, usager):
        if not usager.initial:
            self._attentes.append(usager.heure_fin_queue - usager.heure_debut_queue)

    def fin(self):
        print(statistics.mean(self._attentes), statistics.pstdev(self._attentes))


class MedianeQuartiles(MoyenneEcarttype):
    """Médiane et Écart interquartile"""

    keyword = "mediane"

    def fin(self):
        quartiles = numpy.percentile(self._attentes, [25, 75])
        print(statistics.median(self._attentes), quartiles[1] - quartiles[0])


class TempsAttente(Sortie):
    """Affiche la liste des temps d'attente"""

    keyword = "attente"

    def suivant(self, usager):
        if not usager.initial:
            print(usager.heure_fin_queue - usager.heure_debut_queue)
