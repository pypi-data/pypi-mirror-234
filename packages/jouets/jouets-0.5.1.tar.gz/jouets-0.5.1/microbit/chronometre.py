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

"""Un chronètre, avec pause et temps de tour.

Usage :

- bouton B pour démarrer ; mettre en pause ; relancer ;
- bouton A pour afficher le temps de tour (afficher le temps, mais continuer
  mesurer le temps en arrière plan).
"""

from utime import ticks_ms as maintenant

from microbit import *

###############################################################################
# Création des images

GAUCHE = [
    Image("""99000:99000:99000:99000:99000"""),
    Image("""09000:09000:09000:09000:09000"""),
    Image("""99000:09000:99000:90000:99000"""),
    Image("""99000:09000:99000:09000:99000"""),
    Image("""99000:99000:99000:09000:09000"""),
    Image("""99000:90000:99000:09000:99000"""),
    Image("""99000:90000:99000:99000:99000"""),
    Image("""99000:09000:09000:09000:09000"""),
    Image("""99000:99000:00000:99000:99000"""),
    Image("""99000:99000:99000:09000:99000"""),
]

DROITE = [chiffre.shift_right(3) for chiffre in GAUCHE]


def affiche_secondes(millisecondes):
    """Affiche le nombre de sondes sur la carte."""
    secondes = int(millisecondes / 1000)
    display.show(DROITE[secondes % 10] + GAUCHE[(secondes % 100) // 10])


###############################################################################
# Création des états

INITIAL, COURSE, TOUR, PAUSE, DOUBLEPAUSE = range(5)

###############################################################################
# Boucle principale

etat = INITIAL
temps_debut = maintenant()
temps_pause = 0
temps_tour = 0

while True:
    # Changement éventuel d'état
    if button_a.was_pressed():
        if etat == COURSE:
            temps_tour = maintenant() - temps_debut
            etat = TOUR
        elif etat == TOUR:
            etat = COURSE
        elif etat == PAUSE:
            etat = INITIAL
        elif etat == DOUBLEPAUSE:
            etat = PAUSE
        else:  # etat == INITIAL
            pass
    elif button_b.was_pressed():
        if etat == COURSE:
            temps_pause = maintenant() - temps_debut
            etat = PAUSE
        elif etat == TOUR:
            temps_pause = maintenant() - temps_debut
            etat = DOUBLEPAUSE
        elif etat == PAUSE:
            temps_debut = maintenant() - temps_pause
            etat = COURSE
        elif etat == DOUBLEPAUSE:
            temps_debut = maintenant() - temps_pause
            etat = TOUR
        else:  # etat == INITIAL
            temps_debut = maintenant()
            etat = COURSE

    # Affichage
    if etat == COURSE:
        affiche_secondes(maintenant() - temps_debut)
    elif etat == DOUBLEPAUSE:
        affiche_secondes(temps_tour)
    elif etat == PAUSE:
        affiche_secondes(temps_pause)
    elif etat == INITIAL:
        affiche_secondes(0)
    elif etat == TOUR:
        affiche_secondes(temps_tour)
