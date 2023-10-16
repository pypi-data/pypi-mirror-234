# Copyright 2020-2023 Louis Paternault
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

"""Tracé de graphiques relatifs au jeu du verger."""

import itertools

import matplotlib.pyplot as plt
import numpy
import seaborn

# pylint: disable=relative-beyond-top-level
# Voir https://github.com/PyCQA/pylint/issues/1667
from ..utils.cache import AllInOneCache
from . import STRATEGIES
from . import probabilite as _probabilite


class Cache(AllInOneCache):
    """Classe utilisée pour mettre les probabilités calculées en cache."""

    module = "verger"
    cachename = "verger.csv"

    @classmethod
    def data2row(cls, data):
        """Convertit une probabilité allant être mise en cache en une ligne CSV."""
        return [data]

    @classmethod
    def row2data(cls, row):
        """Convertit une ligne lue depuis le cache CSV en flottant."""
        return float(row[0])


@Cache.intercepte()
def probabilite(*, corbeau, panier, arbres, fruits):
    """Renvoit la probabilité de victoire pour une partie.

    Le résultat de cette simulation est mis en cache.

    :param int corbeau: Nombre de pièces du puzzle restant au corbeau.
    :param str panier: Nom de la stratégie à utiliser (comme clef de :data:`STRATÉGIE`.
    :param int arbres: Nombre d'arbres.
    :param int fruits: Nombre de fruits par arbre.
    """
    return _probabilite(corbeau, STRATEGIES[panier], *(fruits for _ in range(arbres)))


def graphique_strategies(arbres=4, fruits=10, corbeau=9):
    """Compare les différentes stratégies dans un graphique."""
    y_pos = numpy.arange(len(STRATEGIES))
    probas = [
        probabilite(corbeau=corbeau, panier=panier, fruits=fruits, arbres=arbres)
        for panier in STRATEGIES
    ]

    bars = plt.bar(y_pos, probas, align="center", alpha=0.5)
    plt.xticks(y_pos, list(STRATEGIES.keys()))
    plt.ylabel("Probabilité de victoire")
    plt.xlabel("Stratégie")

    for rect in bars:
        height = rect.get_height()
        plt.annotate(
            f"{height:.2f}",
            xy=(rect.get_x() + rect.get_width() / 2, height),
            xytext=(0, 3),  # 3 points vertical offset
            textcoords="offset points",
            ha="center",
            va="bottom",
        )

    plt.show()


def heatmap_probabilites(maxarbres=10, maxfruits=10, corbeau=9):
    """Trace un graphique montrant les probabilités de victoire

    Pour un nombre de corbeaux fixe, pour différents nombres
    d'arbres et de fruits, calcule et affiche la probabilité.
    """
    seaborn.set()
    data = [
        [
            probabilite(corbeau=corbeau, panier="max", fruits=fruits, arbres=arbres)
            for arbres in range(1, maxarbres + 1)
        ]
        for fruits in range(1, maxfruits + 1)
    ]
    axes = seaborn.heatmap(
        data,
        annot=True,
        vmin=0,
        vmax=1,
        robust=True,
        xticklabels=range(1, maxarbres + 1),
        yticklabels=range(1, maxfruits + 1),
    )
    axes.set(xlabel="Nombre d'arbres", ylabel="Nombre de fruits par arbre")
    axes.invert_yaxis()
    plt.show()


def _equiproba(arbres, fruits):  # pylint: disable=inconsistent-return-statements
    """Calcule le nombre de corbeau nécessaires pour s'approcher de l'équiprobabilité.

    Retourne le plus petit nombre de corbeaux tels que la joueuse
    ait plus d'une chance sur deux de gagner.
    """
    for corbeau in itertools.count():
        proba = probabilite(corbeau=corbeau, panier="max", fruits=fruits, arbres=arbres)
        if proba > 0.5:
            return corbeau


def heatmap_equiprobabilites(maxarbres=10, maxfruits=10):
    """Construit un graphique montrant comment s'approcher de l'équiprobabilité.

    Pour différents nombres d'arbres et de fruits par arbres,
    calcule le nombre de corbeaux pour s'approcher de
    l'équiprobabilité.
    """
    seaborn.set()
    data = [
        [_equiproba(arbres, fruits) for arbres in range(1, maxarbres + 1)]
        for fruits in range(1, maxfruits + 1)
    ]
    axes = seaborn.heatmap(
        data,
        annot=True,
        xticklabels=range(1, maxarbres + 1),
        yticklabels=range(1, maxfruits + 1),
    )
    axes.set(xlabel="Nombre d'arbres", ylabel="Nombre de fruits par arbre")
    axes.invert_yaxis()
    plt.show()


if __name__ == "__main__":
    graphique_strategies()
    heatmap_probabilites()
    heatmap_equiprobabilites()
