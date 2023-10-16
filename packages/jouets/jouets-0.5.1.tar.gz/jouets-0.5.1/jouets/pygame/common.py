# Copyright 2018-2021 Louis Paternault
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

"""Quelques fonctions utiles pour les différents jeux réalisés avec pygame."""

import os

import pkg_resources
import pygame
from pygame.locals import KEYDOWN

BLANC = (255, 255, 255)


def affiche_texte(fenetre, ligne, decalage=(0, 0), couleur=BLANC, taille=25):
    """Affiche une ligne de texte dans la fenetre"""
    font = pygame.font.Font(None, taille)
    texte = font.render(ligne, True, couleur)
    texte_rect = texte.get_rect()
    texte_rect.centerx = fenetre.get_rect().centerx + decalage[0]
    texte_rect.centery = fenetre.get_rect().centery + decalage[1]
    fenetre.blit(texte, texte_rect)
    pygame.display.update(texte_rect)


def textbox(fenetre, texte, couleur=BLANC, taille=25, events=(KEYDOWN,)):
    """Afiche du texte dans la fenêtre, et attend une action de l'utilisateur."""
    for numero, ligne in enumerate(texte.split("\n")):
        affiche_texte(
            fenetre, ligne, (0, 20 * numero + 30), couleur=couleur, taille=taille
        )

    pygame.event.clear()
    while True:
        event = pygame.event.wait()
        if event.type in events:
            break


def datafile(package, filename):
    """Renvoit le chemin d'accès d'un fichier de données du module.

    Une entorse à ma règle : je n'attend pas des élèves qu'ils utilisent une
    fonction similaire. Mais pour que les jeux puissent être distribués
    correctement avec les fichiers d'images, cette fonction est nécessaire.
    """
    return pkg_resources.resource_filename(
        f"jouets.pygame.{package}", os.path.join("data", filename)
    )


def affiche_score(fenetre, font, fond, score):
    """Affiche le score."""
    # pylint: disable=redefined-outer-name
    scoref = font.render(str(score), True, (0, 255, 0))
    pygame.draw.rect(
        fenetre,
        fond,
        [
            20 - scoref.get_width() // 10,
            20 - scoref.get_height() // 10,
            scoref.get_width(),
            scoref.get_height(),
        ],
    )
    fenetre.blit(
        scoref, (20 - scoref.get_width() // 10, 20 - scoref.get_height() // 10)
    )
