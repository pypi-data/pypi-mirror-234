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

"""Calcul des probabilités de victoire au jeu du verger"""

import functools
import os
import random

VERSION = "0.1.0"


def panier_max(arbres):
    """Choisir l'arbre le moins vide (contenant le plus de fruits)."""
    if len(arbres) == 1:
        return [arbres[0] - 2]
    if arbres[-1] == 1 or arbres[-1] == arbres[-2]:
        return sorted(
            (
                fruits
                for fruits in (list(arbres[:-2]) + [arbres[-2] - 1] + [arbres[-1] - 1])
                if fruits
            )
        )
    return sorted(
        (fruits for fruits in (list(arbres[:-1]) + [arbres[-1] - 2]) if fruits)
    )


def panier_min(arbres):
    """Choisir l'arbre le plus vide (contenant le moins de fruits)."""
    if len(arbres) == 1:
        return [arbres[0] - 2]
    if arbres[0] == 1:
        return sorted(
            (fruits for fruits in ([arbres[1] - 1] + list(arbres[2:])) if fruits)
        )
    return sorted((fruits for fruits in ([arbres[0] - 2] + list(arbres[1:])) if fruits))


def panier_random(arbres):
    """Choisir l'arbre au hasard."""
    copie = list(arbres)
    for _ in range(2):
        indice = random.randint(0, len(copie) - 1)
        copie[indice] -= 1
        if not copie[indice]:
            del copie[indice]
    return sorted(copie)


#: Stratégies disponibles lorsqu'un « panier » est obtenu au dé.
STRATEGIES = {"max": panier_max, "min": panier_min, "random": panier_random}

CACHESIZE_ENV = "VERGER_CACHE_SIZE"


def cache_size():
    """Renvoit la taille du cache.

    Celle-ci est lue depuis la variable d'environnement `CACHESIZE_ENV`:

    - si elle est définie à une chaîne vide, elle est infinie (valeur `None`) ;
    - sinon, si elle est définie à une chaîne pouvant être
      interprétée comme un nombre entier, ce nombre désigne la
      taille du cache ;
    - sinon, si la variable d'environnement n'est pas définie, ou
      si elle est définie à une chaîne non vide non reconnue comme
      un nombre, la taille est :math:`2^{20}`.
    """
    cachesize_str = os.getenv(CACHESIZE_ENV)
    if cachesize_str == "":
        return None
    try:
        return int(cachesize_str)
    except (ValueError, TypeError):
        return 2**20


@functools.lru_cache(cache_size())
def probabilite(corbeau, panier, *arbres):
    """Renvoit la probabilité de victoire pour une partie.

    :param int corbeau: Nombre de pièces du puzzle restant au corbeau.
    :param function panier: Stratégie à utiliser, comme une valeur de :data:`STRATEGIES`.
    :param list arbres: Nombre de fruits sur chacun des arbres,
        comme une liste décroissante d'entiers strictement
        positifs.  Les arbres vides ne sont pas représentés
        (puisque la probabilité de gagner dans un jeu à quatre
        arbres dont deux vides est égale à celle de gagner dans un
        jeu à deux arbres).
    """
    # Conditions de victoire et de défaite
    if sum(arbres) == 0:
        return 1
    if corbeau == 0:
        return 0

    # Appel récursif
    proba = 0

    # Corbeau
    proba += probabilite(corbeau - 1, panier, *arbres)

    # Fruit
    for i in range(len(arbres)):
        copie = list(arbres)
        copie[i] -= 1
        if not copie[i]:
            del copie[i]
        proba += probabilite(corbeau, panier, *sorted(copie))

    # Panier
    if sum(arbres) <= 2:
        proba += 1
    else:
        proba += probabilite(corbeau, panier, *panier(arbres))

    return proba / (len(arbres) + 2)
