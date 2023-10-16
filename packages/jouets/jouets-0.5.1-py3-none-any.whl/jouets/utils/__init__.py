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

"""Quelques outils utiles pour jouets."""

import contextlib
import sys


@contextlib.contextmanager
def smartopen(filename):
    """Contexte pour ouvrir un fichier, ou la sortie standard si l'argument est `None`."""
    if filename is None:
        filehandle = sys.stdout
    else:
        filehandle = open(filename, mode="w", encoding="utf8")

    try:
        yield filehandle
    finally:
        if filehandle is not sys.stdout:
            filehandle.close()
