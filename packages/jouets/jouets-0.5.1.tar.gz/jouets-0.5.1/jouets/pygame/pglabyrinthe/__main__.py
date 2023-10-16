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

"""Jeu de labyrinthe."""

# pylint: disable=invalid-name, unused-wildcard-import, wildcard-import

import textwrap

import pygame
from pygame.locals import *

from ..common import datafile, textbox


def main():
    """Fonction principale"""

    pygame.init()

    ################################################################################
    # Quelques constantes

    NOIR = (0, 0, 0)

    # La manière de coder cette carte est une entorse à ma règle qui stipule que le
    # programme doit pouvoir être réalisé par un élève. Mais il est tellement plus
    # clair d'avoir la carte dessinée avec des 1 et des espaces, comme ci-dessous,
    # et qu'elle soit stockée comme un tableau de True et False.
    CARTE = [
        [char == "1" for char in ligne.strip()]
        for ligne in """
            1111111111111111111111111111111111111111
            1  1      11 1    1          1     1   1
            1 1111111 11 11 1  1 1111111 11111  11 1
            1 11    1 1    1 1         1      1  1 1
            1    11 1 1 11   1 1111111 1 1111111 1 1
            111 111 1  11 11     1   1 1 1       111
            1     1 1 1 1 1 1111   1 1 111 1 1  1  1
            1111111 1   1    1   1 111    111  11 11
            1       1 11  111  11 11  111     1 1  1
            11 1 1111 1       1 1 11 11 1 11111   11
            1  1        11 1111 1    1    1   1111 1
            1 1111 1 111 1 1     111 11 111 1      1
            1     111      11111 1 1   11 1 1 1 1111
            111 1  1 11 11         111 1   11 11   1
            1   1 11     11111 111   1 111     1 111
            1 1 1   1111 11  1   1 11   11 11111   1
            1 1 1 1    1  1 1 11  111 1 1  11    1 1
            1 1    111 11 1 1  11     1 11 1  11 1 1
            111 1 1  1 1  1 1 1  1 1111      1 1 1 1
            1 1 1111   1 11 1 1 11  1   11 11  1 111
            1 1    1 111111 1      11 11  11     1 1
            1 1 1 11        11 1 1111   1  1 1 1 1 1
            1   1 11 1 111 11111 11 1 1 1 11 1 1   1
            11111  111 1 1   1 1     1  1     111 11
            1         11 11 11 11 1111 1 1 11   1  1
            1 1 11111 11 1   1    1    1     11  1 1
            1 1 11  1    111 1 1111 111111 11     11
            111   1 1111 1   111    1      1  1 1  1
            1   1 1      1 1 1   1  1 1 1 1  1   1 1
            1111111111111111111111111111111111111111
            """.split(
            "\n"
        )
        if ligne.strip()
    ]
    coord_perso = (1, 1)
    coord_fin = (38, 28)

    def affiche_carte(fenetre, carte):
        """Affiche la carte."""
        # pylint: disable=redefined-outer-name, consider-using-enumerate
        for y in range(len(carte)):
            for x in range(len(carte[y])):
                if carte[y][x]:
                    fenetre.blit(IMGMUR, (20 * x, 20 * y))

    ################################################################################
    # Ouverture de la fenêtre Pygame
    fenetre = pygame.display.set_mode((800, 600))

    ################################################################################
    # Chargement des images
    IMGMUR = pygame.image.load(datafile("pglabyrinthe", "mur.png")).convert_alpha()
    IMGPERSO = pygame.image.load(datafile("pglabyrinthe", "perso.png")).convert_alpha()
    IMGEND = pygame.image.load(datafile("pglabyrinthe", "endflag.png")).convert_alpha()

    textbox(
        fenetre,
        textwrap.dedent(
            """\
            LABYRINTHE
            - Flèches pour se déplacer.
            - ÉCHAP pour quitter.
            """
        ),
    )
    fenetre.fill(NOIR)

    ################################################################################
    # Initialisation des graphiques
    affiche_carte(fenetre, CARTE)
    fenetre.blit(IMGEND, (20 * coord_fin[0], 20 * coord_fin[1]))
    pygame.display.flip()

    ################################################################################
    # Boucle principale

    pygame.event.clear()
    while True:
        # Affichage du personnage
        fenetre.blit(IMGPERSO, (20 * coord_perso[0], 20 * coord_perso[1]))
        pygame.display.update(20 * coord_perso[0], 20 * coord_perso[1], 20, 20)

        # Attente d'une touche
        event = pygame.event.wait()

        # Effacement de la dernière position du personnage
        pygame.draw.rect(
            fenetre, NOIR, (20 * coord_perso[0], 20 * coord_perso[1], 20, 20), 0
        )
        pygame.display.update(20 * coord_perso[0], 20 * coord_perso[1], 20, 20)

        # Gestion de la touche
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break
        if event.type == KEYDOWN:
            dest = coord_perso
            if event.key == K_LEFT:
                dest = (coord_perso[0] - 1, coord_perso[1])
            if event.key == K_RIGHT:
                dest = (coord_perso[0] + 1, coord_perso[1])
            if event.key == K_UP:
                dest = (coord_perso[0], coord_perso[1] - 1)
            if event.key == K_DOWN:
                dest = (coord_perso[0], coord_perso[1] + 1)
            if not CARTE[dest[1]][dest[0]]:
                # Si le joueur n'a pas foncé dans un mur, le déplacer
                coord_perso = dest
            if coord_perso == coord_fin:
                # Gagné !
                fenetre.blit(IMGPERSO, (20 * coord_perso[0], 20 * coord_perso[1]))
                pygame.display.flip()
                fenetre.fill(NOIR)
                textbox(fenetre, " BRAVO ! ", taille=100, couleur=(128, 255, 128))
                break

    ################################################################################
    # Fin du jeu

    pygame.quit()


if __name__ == "__main__":
    main()
