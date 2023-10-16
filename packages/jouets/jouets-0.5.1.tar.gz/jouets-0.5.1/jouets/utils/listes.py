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

"""Quelques fonctions utiles manipulant listes et objets apparentés."""

from jouets.utils.erreurs import ErreurInterne


def autre(couple, element):
    """Renvoie l'autre élément du couple.

    :param tuple couple: Couple d'objets.
    :param element: Élement.
    :raises `jouets.utils.erreurs.ErreurInterne`: Si ``element`` n'est pas un
      des deux éléments de ``couple``.
    """
    if couple[0] == element:
        return couple[1]
    if couple[1] == element:
        return couple[0]
    raise ErreurInterne()
