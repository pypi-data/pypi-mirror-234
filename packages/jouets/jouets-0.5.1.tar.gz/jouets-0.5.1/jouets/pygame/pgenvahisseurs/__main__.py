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

"""Jeu : Repousser les envahisseurs."""

# pylint: disable=invalid-name, unused-wildcard-import, wildcard-import

import datetime
import itertools
import textwrap
from math import cos, pi, sin
from random import randint

import pygame
from pygame.locals import *

from ..common import affiche_score, datafile, textbox

################################################################################
# Quelques constantes

BLEUCLAIR = (0, 127, 255)
JAUNE = (255, 255, 0)
GRIS = (64, 64, 64)

GRAVITE = 50

################################################################################
# Quelques petites fonctions


def couleur_canon(deltatemps):
    """Renvoit la couleur du canon.

    En fonction de l'intervalle de temps écoulé depuis le dernier tir.
    """
    return (255, int(min(255, 255 * deltatemps)), 0)


def distance_carree(coord1, coord2):
    """Renvoit le carré de la distance entre les deux coordonnées.

    La distance (qui correspond à la racine carrée de cette fonction) n'est pas
    calculée, car il est plus rapide d'élever au carré la distance à laquelle
    on veut comparer le résultat de cette fonction, que de calculer cette
    fonction. Mais il est tout à fait possible que cette optimisation soit
    inutile : je n'ai pas testé sans…
    """
    return (coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2


def score(valeur1, valeur2):
    """Renvoit la chaîne de caractères affichant le score."""
    return f"Arrêtés : {valeur1} / Passés : {valeur2}"


def main():
    """Fonction principale"""
    # pylint: disable=too-many-locals, too-many-branches, too-many-statements

    ################################################################################
    # Initialisation de pygame
    pygame.init()
    fenetre = pygame.display.set_mode((800, 600))
    fenetre.fill(BLEUCLAIR)
    pygame.display.flip()
    font = pygame.font.SysFont(None, 25)
    clock = pygame.time.Clock()

    ################################################################################
    # Chargement des images
    IMGOVNI = pygame.image.load(datafile("pgenvahisseurs", "ovni.png")).convert_alpha()
    IMGALIEN = pygame.image.load(
        datafile("pgenvahisseurs", "alien.png")
    ).convert_alpha()
    IMGCANON = pygame.image.load(
        datafile("pgenvahisseurs", "canon.png")
    ).convert_alpha()

    ################################################################################
    # Initialisation du jeu

    # Angle du canon, en radians
    angle_canon = pi / 4

    # Ensemble des envahisseurs
    envahisseurs = set()

    # Ensemble des boulets tirés par le joueur
    boulets = set()

    # Score : Nombre d'envahisseurs passés et arrêtés.
    passes = 0
    arretes = 0

    # Niveau (le plus bas est le plus difficile). Cela correspond en fait au temps
    # (en seconde) entre deux arrivées d'envahisseurs.
    niveau = 5

    # Date de la dernière apparition d'un envahisseur, ou du dernier tir au canon.
    dernierenvahisseur = datetime.datetime.fromtimestamp(0)
    derniertir = datetime.datetime.fromtimestamp(0)

    textbox(
        fenetre,
        textwrap.dedent(
            """\
            ENVAHISSEURS

            - Flèches haut et bas pour contrôler le canon.
            - Espace pour tirer.
            - ÉCHAP pour quitter.

            La partie s'arrête quand vous avez laissé
            passé dix fois plus d'envahisseurs que vous
            n'en avez arrêtés.

            Appuyez sur une touche pour commencer.
            """
        ),
    )

    ################################################################################
    # Initialisation des graphiques
    fenetre.fill(BLEUCLAIR)
    affiche_score(fenetre, font, BLEUCLAIR, score(arretes, passes))
    pygame.display.flip()
    maintenant = datetime.datetime.now()

    ################################################################################
    # Boucle principale

    poursuivre = True
    while poursuivre:
        avant = maintenant
        maintenant = datetime.datetime.now()
        delta = (maintenant - avant).total_seconds()

        # On efface la fenêtre
        fenetre.fill(BLEUCLAIR)

        # Gestion des touches
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                poursuivre = False
        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            angle_canon = min(pi / 2, angle_canon + delta * 2)
        if keys[K_DOWN]:
            angle_canon = max(0, angle_canon - delta * 2)
        if keys[K_SPACE]:
            if (maintenant - derniertir).total_seconds() > 0.5:
                # Tir d'un boulet
                derniertir = maintenant
                boulets.add(
                    (
                        100 * cos(angle_canon),
                        600 - 100 * sin(angle_canon),
                        320 * cos(angle_canon),
                        -320 * sin(angle_canon),
                    )
                )

        affiche_score(fenetre, font, BLEUCLAIR, score(arretes, passes))

        # Collisions
        boulets_disparus = set()
        envahisseurs_disparus = set()
        for boulet, envahisseur in itertools.product(boulets, envahisseurs):
            if (
                distance_carree(
                    (boulet[0], boulet[1]), (envahisseur[0] + 15, envahisseur[1] + 15)
                )
                < 900
            ):
                arretes += 1
                boulets_disparus.add(boulet)
                envahisseurs_disparus.add(envahisseur)
        boulets -= boulets_disparus
        envahisseurs -= envahisseurs_disparus

        # Rotation et affichage du canon
        canon = pygame.transform.rotate(IMGCANON, 180 * angle_canon / pi)
        canon_rect = canon.get_rect()
        canon_rect.center = (
            int(50 * cos(angle_canon)),
            int(600 - 50 * sin(angle_canon)),
        )
        fenetre.blit(canon, canon_rect)
        pygame.draw.circle(
            fenetre,
            couleur_canon((maintenant - derniertir).total_seconds() / 0.5),
            (0, 600),
            50,
        )

        # Ajout éventuel d'un nouvel envahisseur
        if (maintenant - dernierenvahisseur).total_seconds() > niveau:
            dernierenvahisseur = maintenant
            vitesse = randint(50, 200)
            niveau = max(0.75, niveau - 0.2)
            if vitesse < 100:
                envahisseurs.add((810, randint(0, 500), vitesse, IMGALIEN))
            else:
                envahisseurs.add((810, randint(0, 500), vitesse, IMGOVNI))

        # Déplacement des monstres
        suivants = set()
        for x, y, vitesse, dessin in envahisseurs:
            x -= vitesse * delta
            fenetre.blit(dessin, (int(x), int(y)))
            if x > -30:
                suivants.add((x, y, vitesse, dessin))
            else:
                passes += 1
        envahisseurs = suivants

        # Déplacement des boulets
        suivants = set()
        for x, y, vx, vy in boulets:
            x += vx * delta * 5
            y += vy * delta * 5
            vy += GRAVITE * delta * 10
            pygame.draw.circle(fenetre, GRIS, (int(x), int(y)), 10)
            if y < 610:
                suivants.add((x, y, vx, vy))
        boulets = suivants

        # Fin de partie ?
        if 10 * passes > arretes:
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
        ).format(arretes),
    )

    pygame.quit()


if __name__ == "__main__":
    main()
