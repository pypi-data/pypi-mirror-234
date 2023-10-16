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

"""Jeu : Éviter les obstacles"""

# pylint: disable=invalid-name, unused-wildcard-import, wildcard-import

import datetime
import textwrap
from math import cos, pi, sin
from random import randint, random

import pygame
from pygame.locals import *

from ..common import affiche_score, textbox

################################################################################
# Quelques constantes

ROUGE = (255, 0, 0)
JAUNE = (255, 255, 0)
GRIS = (127, 127, 127)
NOIR = (0, 0, 0)

################################################################################
# Quelques fonctions


def couleur_trainee(temps):
    """Renvoit la couleur de la trainée, pour avoir un dégradé avec le temps."""
    return (int(max(0, 255 - 255 * temps)), 0, int(128 - 128 * abs(1 - temps)))


def distance_carree(coord1, coord2):
    """Renvoit le carré de la distance entre les deux coordonnées"""
    return (coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2


def main():
    """Fonction principale"""
    # pylint: disable=too-many-locals, too-many-branches, too-many-statements

    ################################################################################
    # Initialisation de pygame
    pygame.init()
    fenetre = pygame.display.set_mode((800, 600))
    fenetre.fill(NOIR)
    pygame.display.flip()
    pygame.mouse.set_visible(False)
    font = pygame.font.SysFont(None, 25)
    clock = pygame.time.Clock()

    ################################################################################
    # Initialisation du jeu
    coord_obstacles = []
    vitesse_obstacles = []
    trainee = []
    joueur = pygame.mouse.get_pos()
    cible = joueur

    textbox(
        fenetre,
        textwrap.dedent(
            """\
            SLALOM

            - Contrôlez votre boule rouge avec la souris.
            - Mangez les boules jaunes.
            - Évitez les boules grises.
            - ÉCHAP pour quitter.

            Cliquer pour commencer.
            """
        ),
        events=(MOUSEBUTTONDOWN,),
    )

    ################################################################################
    # Initialisation des graphiques
    fenetre.fill(NOIR)
    affiche_score(fenetre, font, NOIR, 0)
    pygame.display.flip()
    pygame.draw.circle(fenetre, JAUNE, cible, 10)
    maintenant = datetime.datetime.now()

    ################################################################################
    # Boucle principale

    poursuivre = True
    while poursuivre:
        avant = maintenant
        maintenant = datetime.datetime.now()

        # Efface la fenêtre
        fenetre.fill(NOIR)

        # Gestion des touches
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                poursuivre = False
            elif event.type == MOUSEMOTION:
                joueur = pygame.mouse.get_pos()
                trainee.append((joueur, maintenant))

        # Affichage et effacement des traces de la souris
        for indice, item in enumerate(trainee):
            coord, time = item
            difference = (maintenant - time).total_seconds()
            if difference > 2:
                del trainee[indice]
                continue
            pygame.draw.circle(fenetre, couleur_trainee(difference), coord, 10)

        # Le joueur a-t-il atteint la cible ?
        if distance_carree(cible, joueur) < 21**2:
            cible = (randint(10, 790), randint(10, 590))

            # Création d'un nouvel obstacle, loin du joueur
            coord_obstacles.append([(joueur[0] + 400) % 800, (joueur[1] + 300) % 600])
            angle, vitesse = 2 * pi * random(), randint(50, 200)
            vitesse_obstacles.append([vitesse * cos(angle), vitesse * sin(angle)])

        # Mise à jour du score
        affiche_score(fenetre, font, NOIR, len(coord_obstacles))

        # Déplacement des obstacles
        delta = (maintenant - avant).total_seconds()
        for indice, obstacle in enumerate(coord_obstacles):
            coord_obstacles[indice] = [
                obstacle[0] + delta * vitesse_obstacles[indice][0],
                obstacle[1] + delta * vitesse_obstacles[indice][1],
            ]
            if coord_obstacles[indice][0] < 10:
                # Collision avec le mur gauche
                coord_obstacles[indice][0] = 20 - coord_obstacles[indice][0]
                vitesse_obstacles[indice][0] = -vitesse_obstacles[indice][0]
            if coord_obstacles[indice][1] < 10:
                # Collision avec le mur haut
                coord_obstacles[indice][1] = 20 - coord_obstacles[indice][1]
                vitesse_obstacles[indice][1] = -vitesse_obstacles[indice][1]
            if coord_obstacles[indice][0] > 790:
                # Collision avec le mur droit
                coord_obstacles[indice][0] = 2 * 790 - coord_obstacles[indice][0]
                vitesse_obstacles[indice][0] = -vitesse_obstacles[indice][0]
            if coord_obstacles[indice][1] > 590:
                # Collision avec le mur bas
                coord_obstacles[indice][1] = 2 * 590 - coord_obstacles[indice][1]
                vitesse_obstacles[indice][1] = -vitesse_obstacles[indice][1]
            pygame.draw.circle(fenetre, GRIS, (int(obstacle[0]), int(obstacle[1])), 10)

        pygame.draw.circle(fenetre, JAUNE, cible, 10)

        pygame.draw.circle(fenetre, ROUGE, joueur, 10)

        # Gestion des collisions
        for obstacle in coord_obstacles:
            if distance_carree(obstacle, joueur) < 17**2:
                poursuivre = False

        pygame.display.flip()
        clock.tick(60)

    ################################################################################
    # Fin du jeu

    textbox(
        fenetre,
        textwrap.dedent(
            """\
        TERMINÉ

        Score : {}
        """
        ).format(len(coord_obstacles)),
        events=(MOUSEBUTTONDOWN, KEYDOWN),
    )

    pygame.quit()


if __name__ == "__main__":
    main()
