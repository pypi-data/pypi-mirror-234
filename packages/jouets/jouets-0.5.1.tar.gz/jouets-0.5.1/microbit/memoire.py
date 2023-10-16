# Copyright 2019 Louis Paternault
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

"""Indique le nord par une flèche."""
import random

import utime

from microbit import *

HAUT, BAS, GAUCHE, DROITE, ATTENTE = range(5)

ETATS_DIRECTIONS = (HAUT, BAS, GAUCHE, DROITE)
MOUVEMENTS = ("up", "left", "right", "down")
MOUVEMENT2ETAT = {"up": HAUT, "down": BAS, "left": GAUCHE, "right": DROITE}


def affiche_direction(etat):
    if etat == HAUT:
        display.show(Image.ARROW_S)
    elif etat == BAS:
        display.show(Image.ARROW_N)
    elif etat == GAUCHE:
        display.show(Image.ARROW_W)
    elif etat == DROITE:
        display.show(Image.ARROW_E)


def clignote(image):
    for i in range(5):
        display.show(image)
        sleep(100)
        display.clear()
        sleep(100)


display.scroll("Secouer pour commencer.", wait=False, loop=True)

while True:
    # Début de partie
    mouvement = None
    while mouvement != "shake":
        mouvement = accelerometer.current_gesture()
    for i in range(3, 0, -1):
        display.show(str(i))
        sleep(1000)
    display.show("?")

    objectif = []

    # Nouvelle manche
    while True:
        # Augmentation et affichage de l'objectif
        objectif.append(random.choice(ETATS_DIRECTIONS))
        for direction in objectif:
            affiche_direction(direction)
            sleep(500)
            display.clear()
            sleep(100)
        display.show("?")

        # Lecture de la liste donnée par l'utilisateur
        etat = ATTENTE
        index = 0
        debut = 0
        while True:
            mouvement = accelerometer.current_gesture()

            # Changement d'état
            if etat == ATTENTE:
                if mouvement in MOUVEMENTS:
                    debut = utime.ticks_ms()
                    etat = MOUVEMENT2ETAT[mouvement]
            elif etat in ETATS_DIRECTIONS:
                if mouvement in MOUVEMENTS and etat != MOUVEMENT2ETAT[mouvement]:
                    debut = utime.ticks_ms()
                    etat = MOUVEMENT2ETAT[mouvement]
                elif mouvement not in MOUVEMENTS:
                    etat = ATTENTE
                elif utime.ticks_ms() - debut > 500:
                    affiche_direction(etat)
                    sleep(500)
                    if etat == objectif[index]:
                        etat = ATTENTE
                        index += 1
                        if index == len(objectif):
                            break
                        display.show("?")
                    else:
                        break

        if index == len(objectif):
            clignote(Image.HAPPY)
        else:
            break

    # La seule manière d'arriver là est d'avoir perdu
    clignote(Image.SKULL)
    display.scroll("Score: {}".format(len(objectif) - 1), loop=True, wait=False)
