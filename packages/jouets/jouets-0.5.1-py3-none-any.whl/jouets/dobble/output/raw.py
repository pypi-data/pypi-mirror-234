# Copyright 2014-2021 Louis Paternault
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

"""Affichage brut des cartes, comme une liste de symboles (liste de nombres)."""

from . import DobbleOutput


class RawOutput(DobbleOutput):
    """Liste brute des symboles des cartes"""

    # pylint: disable=too-few-public-methods

    keyword = "raw"

    def genere(self, jeu, groupe=False):
        """Renvoit la chaîne correspondant au jeu."""
        cartes = []
        for carte in jeu:
            symboles = []
            for symbole in carte:
                if groupe:
                    symboles.append(f"{carte.groupe}-{symbole}")
                else:
                    symboles.append(str(symbole))
            cartes.append(" ".join(symboles))
        return "\n".join(cartes)
