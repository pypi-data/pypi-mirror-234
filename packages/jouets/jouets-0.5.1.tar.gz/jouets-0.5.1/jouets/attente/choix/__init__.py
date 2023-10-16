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

"""Stratégies de choix d'une file par un nouvel usager entrant dans la salle."""


class Choix:
    """Stratégie de choix d'une file par un nouvel usager.

    C'est aussi cet objet qui contient la liste des files de la salle.
    """

    def __init__(self, horloge, files, guichets, changement):
        self.horloge = horloge
        self.files = files
        self.guichets = guichets
        self.changement = changement

    def entre(self, usager):
        """Assigne le nouvel usager à une file."""
        raise NotImplementedError()

    def plusproches(self, numero):
        """Itère les numéros de toutes les files (sauf `numero`).

        L'ordre est : les files les plus proches de `numero` en premier.
        """
        for i in range(1, 1 + max(abs(len(self.files) - numero), numero)):
            if numero + i < len(self.files):
                yield numero + i
            if 0 <= numero - i:
                yield numero - i

    def suivant(self, numeroguichet):
        """Renvoit la prochaine personne de la file correspondant au guichet.

        Cette personne est enlevée de la file.

        Cette personne peut provenir d'une autre file si `self.changement` est `True`.
        """
        numerofile = numeroguichet * len(self.files) // len(self.guichets)
        suivant = self.files[numerofile].suivant()
        # La file contenait un usager,
        # ou n'en contenait pas, mais les usagers ne changent pas de file
        if (suivant is not None) or (not self.changement):
            return suivant

        # La file ne contenait pas d'usager,
        # et les usagers peuvent changer de file.
        for numero in self.plusproches(numerofile):
            suivant = self.files[numero].suivant()
            if suivant is not None:
                return suivant

        # Toutes les files sont vides
        return None

    @property
    def vide(self):
        """Renvoit `True` si toutes les files sont vides."""
        for file in self.files:
            if not file.vide:
                return False
        return True

    def __iter__(self):
        yield from self.files

    def __len__(self):
        return len(self.files)

    def __getitem__(self, item):
        return self.files[item]
