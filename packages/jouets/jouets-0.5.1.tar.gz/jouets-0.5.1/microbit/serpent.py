# Copyright 2023 Louis Paternault
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

"""Jeu de serpent, qui joue au hasard (en évitant autant que possible les murs)."""

# pylint: disable=non-ascii-name, consider-using-f-string

import random

from microbit import *  # pylint: disable=wildcard-import, unused-wildcard-import


class Direction:
    """Direction de déplacement du serpent."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def plus(self, départ):
        """Renvoit les coordonnées de la nouvelle position, en partant de départ.

        Il aurait été plus propre d'utiliser __radd__,
        mais cela ne semble pas supporté par micropython.
        """
        return (départ[0] + self.x, départ[1] + self.y)

    def opposé(self):
        """Renvoit la direction opposée à la direction courante.

        Il aurait été plus propre d'utiliser __neg__,
        mais cela ne semble pas supporté par micropython.
        """
        return Direction(-self.x, -self.y)

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


DIRECTIONS = (
    Direction(-1, 0),
    Direction(1, 0),
    Direction(0, -1),
    Direction(0, 1),
)


def nouvelle_pomme(serpent):
    """Affiche et renvoit les coordonnées d'une nouvelle pomme."""
    pomme = random.choice(
        tuple((x, y) for x in range(5) for y in range(5) if (x, y) not in serpent)
    )
    display.set_pixel(pomme[0], pomme[1], 9)
    return pomme


def libre(serpent, direction):
    """Renvoit True si et seulement si le serpent peut avancer dans la direction donnée."""
    prochain = direction.plus(serpent[0])
    return (prochain not in serpent) and 0 <= prochain[0] <= 4 and 0 <= prochain[1] <= 4


def clignote():
    """Fait clignoter l'écran"""
    screen = [[display.get_pixel(x, y) for y in range(5)] for x in range(5)]
    for _ in range(10):
        display.clear()
        sleep(500)
        for x in range(5):
            for y in range(5):
                display.set_pixel(x, y, screen[x][y])
        sleep(500)


def partie():
    """Initialise une partie de Serpent, et joue jusqu'à la défaite."""
    display.clear()

    serpent = [(random.randint(0, 4), random.randint(0, 4))]
    display.set_pixel(serpent[0][0], serpent[0][1], random.randint(2, 7))

    pomme = nouvelle_pomme(serpent)
    direction = random.choice(tuple(DIRECTIONS))

    while True:
        # Changement de direction ?
        candidats = tuple(
            candidat
            for candidat in DIRECTIONS
            if libre(serpent, candidat) and candidat != direction.opposé()
        )
        if not candidats:
            clignote()
            return
        if (not libre(serpent, direction)) or (random.random() < 0.4):
            direction = random.choice(candidats)

        # Mouvement
        serpent.insert(0, direction.plus(serpent[0]))
        display.set_pixel(serpent[0][0], serpent[0][1], random.randint(2, 7))

        # Pomme
        if serpent[0] == pomme:
            pomme = nouvelle_pomme(serpent)
        else:
            display.set_pixel(serpent[-1][0], serpent[-1][1], 0)
            serpent.pop()
        sleep(500)


while True:
    partie()
