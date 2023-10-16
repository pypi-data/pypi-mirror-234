# Copyright 2014-2020 Louis Paternault
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

"""Crible d'Érathostène optimisé en mémoire"""

import collections
import itertools

VERSION = "0.3.0"


def premiers():
    """Itère sur l'ensemble des nombres premiers."""
    yield 2
    prochains = {}

    for n in itertools.count(3, 2):
        if n not in prochains:
            yield n
            prochains[n**2] = n
            continue

        for i in itertools.count(n, 2 * prochains[n]):
            if i not in prochains:
                prochains[i] = prochains[n]
                del prochains[n]
                break


def est_premier(nombre):  # pylint: disable=inconsistent-return-statements
    """Renvoie ``True`` si le nombre donné en argument est premier."""
    for i in premiers():
        if i < nombre:
            continue
        if i == nombre:
            return True
        if i > nombre:
            return False
