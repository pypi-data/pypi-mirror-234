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

"""Quelques outils statistiques"""

import math


def moyenne(serie):
    """Calcul de la moyenne d'une série statistiques.

    La série est un itérable de coubles `(valeur, effectif)`.
    """
    somme = 0
    total = 0
    for valeur, effectifs in serie:
        total += effectifs
        somme += valeur * effectifs
    return somme / total


def variance(serie):
    """Calcul de la variance d'une série statistiques.

    La série est au même format que celle de :func:`moyenne`.
    """
    return (
        moyenne((valeur**2, effectifs) for valeur, effectifs in serie)
        - moyenne(serie) ** 2
    )


def ecarttype(serie):
    """Calcul de l'écart-type d'une série statistiques.

    La série est au même format que celle de :func:`moyenne`.
    """
    return math.sqrt(variance(serie))
