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

"""Génération d'un sous-jeu de base, en utilisant un graphe bipartite complet.
"""

import itertools

from jouets.dobble import Carte
from jouets.dobble.memobble import Jeu, errors
from jouets.dobble.memobble.mmath import est_pair

from . import MemobbleAlgo


class Complet(MemobbleAlgo):
    """Utilisation d'un graphe bipartite"""

    # pylint: disable=too-few-public-methods

    default = {"num": 6, "sub": 4}
    keyword = "bipartite"

    def genere(self, num):
        if not est_pair(num):
            raise errors.TailleNonGeree(f"Argument '{num}' must be even.")
        if num <= 2:
            raise errors.TailleNonGeree(f"Argument '{num}' must be greater than 2.")
        symboles = itertools.count()
        cartes1 = [Carte() for i in range(num // 2)]
        cartes2 = [Carte() for i in range(num // 2)]
        for i in cartes1:
            for j in cartes2:
                symbole = next(symboles)
                i.symboles.append(symbole)
                j.symboles.append(symbole)
        return Jeu(cartes1 + cartes2)
