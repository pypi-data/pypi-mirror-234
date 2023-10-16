# Copyright 2016 Louis Paternault
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

"""Calcul de probabilités pour le jeu mafia."""

from functools import lru_cache, wraps

VERSION = "0.1.1"

CACHE_SIZE = 1024**2


def arguments_positifs(func):
    """Décorateur qui renvoit 0 si un des arguments est négatif."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Fonction renvoyée par le décorateur."""
        for arg in list(args) + list(kwargs.values()):
            if arg < 0:
                return 0
        return func(*args, **kwargs)

    return wrapper


@lru_cache(CACHE_SIZE)
@arguments_positifs
def proba_matin(mafieux, innocents, detectives):
    """Calcule la probabilité que les innocents gagnent, le matin.

    Les arguments décrivent les joueurs restant un matin donné.
    """
    if mafieux == 0:
        return 1.0
    if mafieux >= innocents + detectives:
        return 0.0
    total = mafieux + innocents + detectives
    return (
        mafieux / total * proba_soir(mafieux - 1, innocents, detectives)
        + innocents / total * proba_soir(mafieux, innocents - 1, detectives)
        + detectives / total * proba_soir(mafieux, innocents, detectives - 1)
    )


@lru_cache(CACHE_SIZE)
@arguments_positifs
def proba_soir(mafieux, innocents, detectives):
    """Calcule la probabilité que les innocents gagnent, le soir.

    Les arguments décrivent les joueurs restant un soir donné.
    """
    if mafieux == 0:
        return 1.0
    if detectives == 0:
        return proba_matin(mafieux, innocents - 1, 0)
    # pylint: disable=line-too-long
    return (
        innocents
        / (detectives + innocents)
        * mafieux
        / (mafieux + innocents)
        * proba_matin(mafieux - 1, innocents - 1, detectives)
        + innocents
        / (detectives + innocents)
        * innocents
        / (mafieux + innocents)
        * proba_matin(mafieux, innocents - 1, detectives)
        + detectives
        / (detectives + innocents)
        * mafieux
        / (mafieux + innocents)
        * proba_matin(mafieux - 1, innocents, detectives - 1)
        + detectives
        / (detectives + innocents)
        * innocents
        / (mafieux + innocents)
        * proba_matin(mafieux, innocents, detectives - 1)
    )
