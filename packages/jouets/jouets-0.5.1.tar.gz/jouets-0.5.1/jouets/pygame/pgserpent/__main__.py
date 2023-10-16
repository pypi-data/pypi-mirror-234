#!/usr/bin/env python3

# Copyright 2018-2023 Louis Paternault
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

"""Jeu de serpent."""

# pylint: disable=invalid-name, unused-wildcard-import, wildcard-import

import datetime
import textwrap
from random import randint

import pygame
from pygame.locals import *

from ..common import affiche_score, datafile, textbox

################################################################################
# Quelques constantes

BLEU = (0, 0, 255)


def jaune():
    """Renvoit une couleur jaune aléatoire."""
    rand = randint(128, 255)
    return (rand, rand, 0)


GAUCHE = (-1, 0)
DROITE = (1, 0)
HAUT = (0, -1)
BAS = (0, 1)
FLECHES = (pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT)


def nouvelle_pomme(serpent):
    """Renvoit les coordonnées d'une nouvelle pomme."""
    # pylint: disable=redefined-outer-name
    while True:
        tentative = (randint(0, 39), randint(0, 29))
        if tentative not in serpent:
            return tentative


def main():
    """Fonction principale"""
    # pylint: disable=too-many-branches, too-many-statements

    ################################################################################
    # Initialisation du jeu

    # Liste des coordonnées des morceaux de serpent.
    serpent = [(20, 20)]

    # Orientation du serpent
    direction = GAUCHE

    # Futurs déplacements
    # Cette liste a été créée car lorsque le joueur appuie très vite sur deux
    # touches (par exemple pour faire un demi-tour), il arraivait qu'une seule des
    # deux soit prise en compte (si une seule touche était prise en compte à chaque
    # passage dans la boucle), ou qu'au contraire le déplacement se fasse en une
    # seule fois (si toutes les touches étaient prises en compte à chaque passage
    # dans la boucle).
    file_directions = []

    # Position de la pomme
    pomme = nouvelle_pomme(serpent)

    # Dictionnaire des touches pressées
    pressed = {fleche: False for fleche in FLECHES}

    ################################################################################
    # Initialisation de pygame
    pygame.init()
    fenetre = pygame.display.set_mode((800, 600))
    fenetre.fill(BLEU)
    pygame.display.flip()
    font = pygame.font.SysFont(None, 25)

    ################################################################################
    # Chargement des images
    IMGPOMME = pygame.image.load(datafile("pgserpent", "pomme.png")).convert_alpha()

    ################################################################################
    # Initialisation de la fenêtre
    textbox(
        fenetre,
        textwrap.dedent(
            """\
            SERPENT
            - Flèches pour se déplacer.
            - ÉCHAP pour quitter.
            """
        ),
    )
    fenetre.fill(BLEU)
    affiche_score(fenetre, font, BLEU, 0)
    fenetre.blit(IMGPOMME, (20 * pomme[0], 20 * pomme[1]))
    pygame.display.flip()

    ################################################################################
    # Boucle principale

    poursuivre = True
    while poursuivre:
        debut_boucle = datetime.datetime.now()

        # Gestion des touches
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                poursuivre = False
            elif event.type == KEYDOWN:
                pressed[event.key] = True

        for fleche in FLECHES:
            if pressed[fleche]:
                file_directions.insert(0, fleche)
                pressed[fleche] = False

        if file_directions:
            # Une seule touche est prise en compte à chaque passage dans la boucle.
            # Les autres attendent leur tour dans la file.
            if file_directions[-1] == pygame.K_DOWN and direction in (GAUCHE, DROITE):
                direction = BAS
            if file_directions[-1] == pygame.K_UP and direction in (GAUCHE, DROITE):
                direction = HAUT
            if file_directions[-1] == pygame.K_LEFT and direction in (HAUT, BAS):
                direction = GAUCHE
            if file_directions[-1] == pygame.K_RIGHT and direction in (HAUT, BAS):
                direction = DROITE
            file_directions.pop()

        # Déplacement du serpent. On calcule les coordonnées de la nouvelle case,
        # avant de tester si elle est déjà occupée par le serpent ou la pomme.
        nouveau = (
            (serpent[0][0] + direction[0]) % 40,
            (serpent[0][1] + direction[1]) % 30,
        )

        if nouveau in serpent[:-1] or (serpent[0] == pomme and nouveau == serpent[-1]):
            # Perdu !
            poursuivre = False

        # Le serpent avance d'une case
        serpent.insert(0, nouveau)

        if serpent[0] == pomme:
            # Le serpent a mangé la pomme. Une autre apparait, et le score augmente
            pomme = nouvelle_pomme(serpent)
            fenetre.blit(IMGPOMME, (20 * pomme[0], 20 * pomme[1]))
            affiche_score(fenetre, font, BLEU, len(serpent) - 1)
        else:
            # Le serpent n'a pas mangé la pomme. Sa queue est supprimée.
            pygame.draw.rect(
                fenetre, BLEU, [20 * serpent[-1][0], 20 * serpent[-1][1], 20, 20]
            )
            serpent.pop()
        pygame.draw.rect(
            fenetre, jaune(), [20 * serpent[0][0], 20 * serpent[0][1], 20, 20]
        )

        pygame.display.flip()

        # On attend, au maximum 0,1 secondes.
        pygame.time.delay(
            max(
                0,
                int(
                    100
                    - (datetime.datetime.now() - debut_boucle).total_seconds() * 1000
                ),
            )
        )

    ################################################################################
    # Fin du jeu
    textbox(
        fenetre,
        textwrap.dedent(
            """\
        TERMINÉ

        Score : {}
        """
        ).format(len(serpent) - 1),
    )

    pygame.quit()


if __name__ == "__main__":
    main()
