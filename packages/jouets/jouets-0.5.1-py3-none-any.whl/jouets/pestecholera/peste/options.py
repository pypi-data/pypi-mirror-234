# Copyright 2014-2017 Louis Paternault
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

"""Gestion des options"""

import argparse

from jouets.pestecholera.common import analyse
from jouets.utils.aargparse import yesno


def analyse_peste():
    """Renvoit un analyseur de ligne de commande."""
    analyseur_specifique = argparse.ArgumentParser(add_help=False)
    analyseur_specifique.add_argument(
        "-t",
        "--turtle",
        help="Enable or disable graphical display",
        metavar="BOOLEAN",
        type=yesno,
        default=True,
    )
    return analyse(prog="peste", parents=[analyseur_specifique])
