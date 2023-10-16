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

"""Modules implémentant différents algorithmes pour le jeu de base.
"""

import argparse
import sys

from jouets.utils import plugins


def argparse_type_algo(texte):
    """Vérifie que l'option choisie par l'utilisateur·ice est valide."""
    for algo in plugins.iter_classes(sys.modules[__name__], MemobbleAlgo):
        if algo.keyword == texte:
            return algo()
    raise argparse.ArgumentTypeError(f"Le type de sortie '{texte}' n'est pas reconnu.")


class MemobbleAlgo:
    """Classe abstraite pour définir des algorithmes de création de jeux."""

    # pylint: disable=too-few-public-methods

    def genere(self, num):
        """Génère la représentation du jeu (une chaîne de caractère)."""
        raise NotImplementedError()
