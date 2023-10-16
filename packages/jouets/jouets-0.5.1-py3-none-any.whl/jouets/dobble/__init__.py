# Copyright 2014-2023 Louis Paternault
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

"""Éléments de Dobble"""

import functools
import itertools

from jouets.erathostene import est_premier

VERSION = "0.2.1"


class TailleNonGeree(Exception):
    """Le programme ne sait pas générer de jeu à cette taille."""

    def __init__(self, taille):
        super().__init__()
        self.taille = taille

    def __str__(self):
        return f"Size must be a prime number, or 1 ({self.taille} is not)."


@functools.total_ordering
class Carte:
    """Une liste de symboles"""

    # pylint: disable=too-few-public-methods

    def __init__(self, symboles=None, groupe=None):
        self.groupe = groupe
        if symboles is None:
            self.symboles = []
        else:
            self.symboles = list(symboles)

    def __iter__(self):
        for symbol in self.symboles:
            yield symbol

    def __str__(self):
        return " ".join(sorted([str(s) for s in self.symboles]))

    def __lt__(self, other):
        if not isinstance(other, Carte):
            raise TypeError()
        return sorted(self.symboles) < sorted(other.symboles)

    def __eq__(self, other):
        if not isinstance(other, Carte):
            raise TypeError()
        return sorted(self.symboles) == sorted(other.symboles)

    def __hash__(self):
        return hash(str(self))

    def __len__(self):
        return len(self.symboles)


class CarteDobble(Carte):
    """Carte de jeu de Dobble."""

    @property
    def valide(self):
        """Renvoie `True` ssi la carte est valide.

        Une carte est valide si elle ne contient pas de symbole en double.
        """
        return len(set(self.symboles)) == len(self.symboles)

    def est_compatible(self, carte):
        """Renvoie `True` si `self` est compatible avec `carte`.

        Deux cartes sont compatibles si elles ont exactement un symbole en
        commun.
        """
        return len(set(self.symboles) & set(carte.symboles)) == 1


class Jeu:
    """Une liste de cartes"""

    # pylint: disable=too-few-public-methods

    def __init__(self, cartes=None):
        if cartes is None:
            self.cartes = []
        else:
            self.cartes = list(cartes)

    def __iter__(self):
        for carte in self.cartes:
            yield carte

    def __str__(self):
        return "\n".join([str(carte) for carte in sorted(self.cartes)])

    def __eq__(self, other):
        if not isinstance(other, Jeu):
            raise TypeError()
        return sorted(self.cartes) == sorted(other.cartes)

    def __hash__(self):
        return hash(" ".join([str(hash(carte)) for carte in sorted(self)]))

    def __len__(self):
        return len(self.cartes)

    @property
    def symboles(self):
        """Renvoie l'ensemble des symboles du jeu."""
        symboles = set()
        for carte in self:
            symboles |= set(carte.symboles)
        return symboles


class JeuDobble(Jeu):
    """Jeu de Dobble"""

    def __init__(self, cartes=None):
        super().__init__(cartes)
        self._resume = {
            "_hash": None,
            "valide": None,
            "trivial": None,
            "regulier": None,
            "frequences_symboles": {},
        }

    def _calcule_resume(self):
        """Met à jour, si nécessaire, le résumé du jeu.

        Le « résumé » du jeu est :
        - ses propriétés (valide, trivial, régulier) ;
        - la fréquence d'apparition des symboles.
        """
        if hash(self) != self._resume["_hash"]:
            self._resume["_hash"] = hash(self)

        self._resume["valide"] = (not self.cartes_invalides()) and (
            not self.couples_cartes_invalides()
        )

        self._resume["trivial"] = (
            # Le jeu est valide
            self._resume["valide"]
            and (
                # Toutes les cartes ne contiennent qu'un symbole
                {len(carte) for carte in self.cartes} == {1}
                or
                # Il n'y a qu'une seule carte
                len(self.cartes) == 1
            )
        )

        frequences = {}
        for carte in self.cartes:
            for symbol in carte:
                frequences[symbol] = frequences.get(symbol, 0) + 1
        self._resume["frequences_symboles"] = frequences

        couples_symboles = list(itertools.combinations(frequences.keys(), 2))
        self._resume["regulier"] = (
            self._resume["valide"]
            and
            # Toutes les cartes ont la même taille
            len({len(carte) for carte in self.cartes}) == 1
            and
            # Les symboles apparaissent autant de fois
            len(set(self._resume["frequences_symboles"].values())) == 1
            and
            # Deux symboles quelconques apparaissent sur exactement une carte
            (
                len(frequences) == 1
                or {
                    len(
                        [
                            carte
                            for carte in self.cartes
                            if (couple[0] in carte and couple[1] in carte)
                        ]
                    )
                    for couple in couples_symboles
                }
                == {1}
            )
        )

    @property
    def valide(self):
        """Retourne `True` ssi le jeu est valide.

        Calcule à nouveau le résumé du jeu si nécessaire.
        """
        self._calcule_resume()
        return self._resume["valide"]

    @property
    def regulier(self):
        """Retourne `True` ssi le jeu est régulier.

        Calcule à nouveau le résumé du jeu si nécessaire.
        """
        self._calcule_resume()
        return self._resume["regulier"]

    @property
    def trivial(self):
        """Retourne `True` ssi le jeu est trivial.

        Calcule à nouveau le résumé du jeu si nécessaire.
        """
        self._calcule_resume()
        return self._resume["trivial"]

    @property
    def frequences_symboles(self):
        """Retourne un dictionnaire des fréquences des symboles.

        Calcule à nouveau le résumé du jeu si nécessaire.

        Les clefs du dictionnaire sont les symboles, et les valeurs sont le
        nombre d'apparition de la clef dans le je.u.
        """
        self._calcule_resume()
        return self._resume["frequences_symboles"]

    def cartes_invalides(self):
        """Retourne la liste des cartes invalides."""
        return [carte for carte in self if not carte.valide]

    def couples_cartes_invalides(self):
        """Retourne la liste des couples de cartes incompatibles."""
        return [
            (carte1, carte2)
            for (carte1, carte2) in itertools.combinations(self.cartes, 2)
            if not carte1.est_compatible(carte2)
        ]


def genere_jeu(taille):
    """Crée et retourne un jeu.

    :param int taille: Taille du jeu.
    :return: Un jeu.
    :rtype: :class:`Jeu`
    """
    # Est-ce que je sais générer un jeu de cette taille ?
    if taille != 1 and not est_premier(taille):
        raise TailleNonGeree(taille)

    # Création des `taille×taille` cartes, réparties en `taille` tas de
    # `taille` cartes.
    cartes = [[CarteDobble() for x in range(taille)] for y in range(taille)]

    dernier = 0

    # Affectation des marqueurs de tas
    marqueurs = list(range(1, taille + 1))
    for tas in range(taille):
        for carte in cartes[tas]:
            carte.symboles.append(marqueurs[tas])

    # Affectation des autres symboles des tas (sauf le dernier)
    symboles = [
        list(range(i * taille + 1, (i + 1) * taille + 1)) for i in range(1, taille + 1)
    ]
    for x in range(taille):
        for y in range(taille):
            for z in range(taille):
                cartes[x][y].symboles.append(symboles[z][(x * z + y) % taille])

    # Créations des cartes de familles de symboles
    cartes.append(
        [CarteDobble(famille + [dernier]) for famille in [marqueurs] + symboles]
    )

    # Création du jeu à partir des cartes
    return JeuDobble(itertools.chain.from_iterable(cartes))
