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

"""Simulation de files d'attente"""

import contextlib

VERSION = "0.1.0"


class Horloge:
    """Décompte le déroulement du temps (en unité arbitraire)."""

    # pylint: disable=too-few-public-methods

    def __init__(self):
        self.temps = 0

    def tictac(self):
        """Avance l'unité de temps arbitraire d'une unité."""
        self.temps += 1


class Usager:
    """Un usager, qui va faire la queue puis aller au guichet."""

    def __init__(self, service, horloge, *, initial=False):
        self.service = service
        self.horloge = horloge
        self.heure_debut_queue = horloge.temps
        self.heure_fin_queue = None
        self.heure_sortie = None
        self.initial = initial

    def debut(self):
        """Appelé lorsque l'usager quitte la file pour aller au guichet."""
        self.heure_fin_queue = self.horloge.temps
        self.heure_sortie = self.horloge.temps + self.service

    @property
    def fini(self):
        """Renvoit `True` si l'usager a terminé (au guichet)."""
        return self.horloge.temps == self.heure_sortie


class Entree:
    """Gère l'entrée des usagers dans la salle."""

    def __init__(self, horloge, usagers, arrivee, service):
        self.horloge = horloge
        self.arrivee = arrivee()
        self.service = service()
        self.usagers = usagers
        self.prochain = self.arrivee.random()

    @property
    def fini(self):
        """Renvoit `True` si tous les usagers sont entrés dans la salle."""
        return self.usagers == 0

    def tictac(self):
        """Fait avancer la simulation d'une unité de temps.

        Renvoit un nouvel usager s'il entre dans la salle. Renvoit `None` sinon.
        """
        self.prochain -= 1
        if self.prochain == 0 and self.usagers > 0:
            self.prochain = self.arrivee.random()
            self.usagers -= 1
            return Usager(self.service.random(), self.horloge)
        return None


class Salle(contextlib.AbstractContextManager):

    """Salle d'attent : portes d'entrée et de sortie, files et guichets."""

    # Remarque : Cette classe gagnerait probablement à être transformée en dataclass

    def __init__(
        self,
        *,
        guichets,
        usagers,
        files,
        arrivee,
        service,
        discipline,
        choix,
        sortie,
        initial,
        changement,
    ):
        # pylint: disable=too-many-arguments
        self.horloge = Horloge()
        self.guichets = [None for __ in range(guichets)]
        self.entree = Entree(self.horloge, usagers, arrivee, service)
        self.files = choix(
            self.horloge,
            [discipline() for __ in range(files)],
            self.guichets,
            changement,
        )
        self.sortie = sortie(salle=self)

        for file in self.files:
            for _ in range(initial):
                file.nouveau(
                    Usager(self.entree.service.random(), self.horloge, initial=True)
                )

    def __enter__(self):
        self.sortie.debut()
        return super().__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        self.sortie.fin()
        return super().__exit__(exc_type, exc_value, traceback)

    def tictac(self):
        """Avance le temps d'une unité.

        - Fait entrer de nouvelles personnes si nécessaire.
        - Fait sortir des gens si elles ont terminé.
        - Fait passer des usagers d'une file à un guichet s'il est libre.
        """
        usager = self.entree.tictac()
        if usager is not None:
            self.files.entre(usager)
            self.sortie.entree(usager)

        for numero, usager in enumerate(self.guichets):
            if usager is not None:
                if usager.fini:
                    self.guichets[numero] = None
                    self.sortie.sortie(usager)
                else:
                    continue

            nouveau = self.files.suivant(numero)
            if nouveau is not None:
                nouveau.debut()
                self.guichets[numero] = nouveau
                self.sortie.suivant(nouveau)

        self.sortie.tictac()
        self.horloge.tictac()

    @property
    def fini(self):
        """Renvoit `True` si et seulement si la simulation est terminée.

        C'est-à-dire si le bon nombre d'usagers est arrivé, et qu'ils sont tous sortis.
        """
        if not self.entree.fini:
            return False
        if any(self.guichets):
            return False
        return self.files.vide
