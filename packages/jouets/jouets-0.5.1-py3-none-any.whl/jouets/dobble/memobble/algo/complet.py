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

"""Génération d'un sous-jeu de base, en utilisant un graphe complet.
"""

import itertools

from jouets.dobble import Carte
from jouets.dobble.memobble import Jeu, errors
from jouets.dobble.memobble.mmath import est_pair

from . import MemobbleAlgo


class Complet(MemobbleAlgo):
    """Utilisation d'un graphe complet"""

    # pylint: disable=too-few-public-methods

    default = {"num": 4, "sub": 5}
    keyword = "complet"

    def genere(self, num):
        if not est_pair(num):
            raise errors.TailleNonGeree(f"Argument '{num}' must be even.")
        symboles = itertools.count()
        cartes = [Carte() for i in range(num)]
        for i in range(num):
            for j in range(num):
                if i <= j:
                    continue
                symbole = next(symboles)
                cartes[i].symboles.append(symbole)
                cartes[j].symboles.append(symbole)
        return Jeu(cartes)
