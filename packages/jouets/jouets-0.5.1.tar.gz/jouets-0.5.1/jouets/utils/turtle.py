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

"""Outils enrichissant le module turtle"""

# pylint: disable=unused-wildcard-import

from contextlib import contextmanager

try:
    # pylint: disable=wildcard-import
    from turtle import *
except ImportError:
    import os

    if os.getenv("UNITTEST", ""):
        # Turtle module is mocked
        pass
    else:
        raise


# pylint: disable=no-member
@contextmanager
def change_delay(temps):
    """Contexte pour changer localement la vitesse de tracé de turtle."""
    # pylint: disable=undefined-variable
    vieux = delay()
    delay(temps)
    yield
    delay(vieux)
