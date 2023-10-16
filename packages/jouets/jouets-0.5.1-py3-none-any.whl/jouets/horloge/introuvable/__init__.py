# Copyright 2020 Louis Paternault
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

"""Horloge introuvable (avec position aléatoire des heures). Ligne de commande."""

import datetime
import math

import pygame

COULEURS = {
    "chiffres": (0, 0, 0),
    "fond": (255, 255, 255),
    "heures": (0, 0, 0),
    "minutes": (0, 0, 0),
    "secondes": (255, 0, 0),
}


class Horloge:
    """Horloge introuvable : les positions des heures sont mélangées."""

    # pylint: disable=too-many-instance-attributes

    def __init__(self, angles, *, couleurs=None, taille=None, vitesse=1):
        self.visibles = {heure: (angle - 90) % 360 for heure, angle in angles.items()}

        self.heures2angles = self.visibles.copy()
        for heure in range(12):
            if heure not in self.heures2angles:
                if heure < min(self.heures2angles):
                    avant = max(self.heures2angles) - 12
                else:
                    avant = max(h for h in self.heures2angles if h < heure)
                avantangle = self.heures2angles[avant % 12] % 360
                if heure > max(self.heures2angles):
                    apres = min(self.heures2angles) + 12
                else:
                    apres = min(h for h in self.heures2angles if h > heure)
                apresangle = self.heures2angles[apres % 12] % 360
                if abs(apresangle - avantangle) > 180:
                    if apresangle > avantangle:
                        apresangle -= 360
                    else:
                        apresangle += 360
                self.heures2angles[heure] = (
                    (apresangle - avantangle) * heure
                    + apres * avantangle
                    - avant * apresangle
                ) / (apres - avant)

        if couleurs is None:
            self.couleurs = COULEURS
        else:
            self.couleurs = COULEURS.copy()
            self.couleurs.update(couleurs)

        pygame.init()

        if taille is None:
            info = pygame.display.Info()
            taille = min(info.current_w, info.current_h)
        self.rayon = None
        self.taille = None

        self.vitesse = vitesse
        self.debut = datetime.datetime.now()

        self.init_pygame((taille, taille))

    def init_pygame(self, taille):
        """Initialisation de l'horloge.

        Cette fonction peut être appelée plusieurs fois,
        notamment si la taille de la fenêtre a changé.
        """
        self.taille = taille
        self.rayon = round(0.4 * min(self.taille))
        self.fenetre = pygame.display.set_mode(self.taille, pygame.RESIZABLE)
        self.fenetre.fill(self.couleurs["fond"])
        pygame.mouse.set_visible(False)
        font = pygame.font.SysFont(None, 25)

        for hour in self.visibles:
            if hour == 0:
                hour = 12
            text = font.render(str(hour), True, self.couleurs["chiffres"])
            rectangle = text.get_rect(
                center=self.angle2coord(self.heures2angles[hour % 12])
            )
            self.fenetre.blit(text, rectangle)

        pygame.display.flip()

    def angles(self, hour, minute, second):
        """Renvoit les angles des trois aiguilles."""
        return (
            self.angle(60 * 60 * hour + 60 * minute + second, 12 * 60 * 60),
            self.angle(60 * minute + second, 60 * 60),
            self.angle(second, 60),
        )

    def angle(self, hand, total):
        """Renvoit l'angle d'une aiguille.

        Arguments :
        - `hand` : nombre d'unités de temps écoulées ;
        - `total` : nombre total d'unités de temps sur un tour de cadrant.

        Par exemple :
        - pour afficher l'aiguille des secondes s'il est 12h34'56'', alors `hand=56, total=60` ;
        - pour afficher l'aiguille des minutes s'il est 12h34'56'',
          alors `hands=(34*60+56), total=60*60` ;
        - etc.
        """
        exact = (12 * hand) / total
        lower, upper = math.floor(exact), math.ceil(exact) % 12
        if lower == upper:
            return self.heures2angles[lower]

        relative = exact - lower
        upperangle = self.heures2angles[upper]
        lowerangle = self.heures2angles[lower]

        widthangle = (upperangle - lowerangle + 180) % 360 - 180
        if widthangle == -180:
            widthangle = 180

        return (lowerangle + relative * widthangle) % 360

    def angle2coord(self, angle, radius=1):
        """Convertit un angle en coordonnées.

        L'argument `radius` n'est pas un rayon absolu,
        mais relatif au rayon de l'horloge `self.rayon`.
        """
        radius = round(0.9 * self.rayon * radius)
        return (
            self.taille[0] // 2 + round(radius * math.cos(math.pi * angle / 180)),
            self.taille[1] // 2 + round(radius * math.sin(math.pi * angle / 180)),
        )

    def tictac(self, hour, minute, second):
        """Dessine une position de l'horloge."""
        hour, minute, second = self.angles(hour, minute, second)
        pygame.draw.line(
            self.fenetre,
            self.couleurs["heures"],
            (self.taille[0] // 2, self.taille[1] // 2),
            self.angle2coord(hour, 0.5),
            3,
        )
        pygame.draw.line(
            self.fenetre,
            self.couleurs["minutes"],
            (self.taille[0] // 2, self.taille[1] // 2),
            self.angle2coord(minute, 0.8),
            2,
        )
        pygame.draw.line(
            self.fenetre,
            self.couleurs["secondes"],
            (self.taille[0] // 2, self.taille[1] // 2),
            self.angle2coord(second, 0.7),
            1,
        )
        pygame.display.update()
        pygame.draw.line(
            self.fenetre,
            self.couleurs["fond"],
            (self.taille[0] // 2, self.taille[1] // 2),
            self.angle2coord(hour, 0.5),
            3,
        )
        pygame.draw.line(
            self.fenetre,
            self.couleurs["fond"],
            (self.taille[0] // 2, self.taille[1] // 2),
            self.angle2coord(minute, 0.8),
            2,
        )
        pygame.draw.line(
            self.fenetre,
            self.couleurs["fond"],
            (self.taille[0] // 2, self.taille[1] // 2),
            self.angle2coord(second, 0.7),
            1,
        )

    def loop(self):
        """Affiche l'horloge en continu jusqu'à ce que l'utilisateur·ice quitte l'application."""
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.VIDEORESIZE:
                    self.init_pygame(event.dict["size"])

            heure = self.debut + (self.vitesse * (datetime.datetime.now() - self.debut))
            self.tictac(heure.hour % 12, heure.minute, heure.second)
            clock.tick(self.vitesse)
