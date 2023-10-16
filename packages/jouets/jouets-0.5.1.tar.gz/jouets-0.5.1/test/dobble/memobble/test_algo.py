# Copyright 2015-2021 Louis Paternault
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

"""Tests du module :mod:`dobble.memobble`."""

import collections
import itertools
import random
import unittest

from jouets.dobble import Carte
from jouets.dobble import genere_jeu as genere_dobble
from jouets.dobble.memobble import Jeu
from jouets.dobble.memobble import algo as memobblealgo
from jouets.dobble.memobble import errors
from jouets.utils import plugins


class Graphe:
    """Graphe non orienté"""

    def __init__(self):
        self.noeuds = []
        self.aretes = collections.defaultdict(list)

    @classmethod
    def from_jeu(cls, jeu):
        """Génère le graphe correspondant à un jeu.

        Les nœuds sont les cartes du jeu ; une arête existe entre deux nœuds si
        et seulement si les cartes correspondantes ont un symbole en commun.
        """
        graphe = cls()
        graphe.noeuds = jeu.cartes.copy()
        for carte1, carte2 in itertools.combinations(jeu.cartes, 2):
            if len(set(carte1.symboles) & set(carte2.symboles)) == 1:
                graphe.ajoute_arete(carte1, carte2)
        return graphe

    def ajoute_arete(self, noeud1, noeud2):
        """Ajoute une arête entre les deux nœuds au graphe.

        Précondition: les deux nœuds ont déjà été ajoutés au graphe.
        """
        self.aretes[noeud1].append(noeud2)
        self.aretes[noeud2].append(noeud1)

    @property
    def nb_noeuds(self):
        """Renvoit le nombre de nœuds du graphe."""
        return len(self.noeuds)

    def supprime_noeud(self, noeud):
        """Supprime un nœud, et les arêtes correspondantes"""
        self.noeuds.remove(noeud)
        del self.aretes[noeud]
        for origine in self.aretes:
            try:
                self.aretes[origine].remove(noeud)
            except ValueError:
                pass

    def pprint(self):
        """Affiche le graphe."""
        for origine in self.aretes:
            for extremite in self.aretes[origine]:
                print(f"{origine} <-> {extremite}")

    def joue(self):
        """Supprime des arêtes jusqu'à épuisement des nœuds.

        Renvoit une exception si le jeu bloque (si restent des nœuds sans
        arêtes).
        """
        while self.nb_noeuds > 0:
            noeud1 = random.choice(self.noeuds)
            noeud2 = random.choice(self.aretes[noeud1])
            self.supprime_noeud(noeud1)
            self.supprime_noeud(noeud2)
        return True


class _TestAlgo(unittest.TestCase):
    """Test un algorithme de génération de jeu de Mémobble."""

    fixtures = []
    seeds = []
    algo = None

    @property
    def _get_algo(self):
        for algo in plugins.iter_classes(memobblealgo, memobblealgo.MemobbleAlgo):
            if algo.keyword == self.algo:
                return algo()
        raise KeyError(f"No algorithm named '{self.algo}'.")

    def genere(self, argument):
        """Génère un jeu."""
        if self.algo is None:
            raise NotImplementedError()
        return self._get_algo.genere(argument)

    def iter_jeux(self):
        """Itérateur sur les jeux à tester."""
        for argument in self.fixtures:
            for seed in self.seeds:
                random.seed(seed)
                yield (
                    self.genere(argument),
                    {"algo": self.algo, "argument": argument, "seed": seed},
                )


class _TestValide(_TestAlgo):
    """Jeu valide, et devant terminer."""

    def test_jeu(self):
        """Test la génération, et la résolution d'un jeu."""
        for jeu, kwargs in self.iter_jeux():
            with self.subTest(**kwargs):
                graphe = Graphe.from_jeu(jeu)

                # Vérification que le jeu est valide
                self.assertTrue(jeu.valide())

                # Vérification que le jeu termine
                self.assertTrue(graphe.joue())


class TestBipartite(_TestValide):
    """Test de l'algorithme avec un graphe bipartite complet."""

    fixtures = [4, 6, 8]
    seeds = [0, 1]
    algo = "bipartite"


class TestComplet(_TestValide):
    """Test de l'algorithme utilisant un graphe complet."""

    fixtures = [4, 6, 8]
    seeds = [0, 1]
    algo = "complet"


class TestErreurGeneration(_TestAlgo):
    """Erreur de génération du jeu"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generateurs = {
            algo.keyword: algo().genere
            for algo in plugins.iter_classes(memobblealgo, memobblealgo.MemobbleAlgo)
        }

    def test_bipartite_impair(self):
        """Bipartite: Le nombre de cartes doit être pair."""
        self.assertRaises(errors.TailleNonGeree, self.generateurs["bipartite"], 3)

    def test_bipartite_deux(self):
        """Bipartite: Le nombre de cartes doit être supérieur (strictement) à deux."""
        self.assertRaises(errors.TailleNonGeree, self.generateurs["bipartite"], 2)

    def test_complet_impair(self):
        """Complet: Le nombre de cartes doit être pair."""
        self.assertRaises(errors.TailleNonGeree, self.generateurs["complet"], 3)


class TestJeuNonJouable(_TestAlgo):
    """Jeux non jouables (qui peuvent se bloquer)."""

    def test_dobble(self):
        """Jeu de Dobble: ne fonctionne pas car le nombre de cartes est impair."""
        graphe = Graphe.from_jeu(genere_dobble(7))
        self.assertRaises(Exception, graphe.joue)

    def test_diamant(self):
        """Test d'une configuration en diamant.

        Cette configuration consiste en un cycle de quatre nœuds
        A-B-C-D, et une arête liant B à D.
        """

        def diamant():
            """Génère un graphe en diamant."""
            return Graphe.from_jeu(
                Jeu([Carte([1, 4]), Carte([1, 2, 5]), Carte([2, 3]), Carte([3, 4, 5])])
            )

        with self.subTest(random=0):
            random.seed(0)
            self.assertRaises(Exception, diamant().joue)

        with self.subTest(random=2):
            random.seed(2)
            self.assertTrue(diamant().joue())
