# Copyright 2020-2021 Louis Paternault
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

"""Quelques graphiques"""

import collections
import csv
import functools
import itertools
import os
import random

import matplotlib.pyplot as plt
import numpy as np
import seaborn

from jouets.utils import plugins, stats
from jouets.utils.cache import SeveralFilesCache

from . import Salle
from . import choix as modulechoix
from . import discipline as modulediscipline
from .choix.default import Personnes
from .discipline.default import FIFO
from .loiproba.default import Exponentielle, Normale
from .sortie import Sortie


class TempsAttente(Sortie):
    """Enregistre la liste des temps d'attente."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attentes = collections.Counter()

    def suivant(self, usager):
        if not usager.initial:
            self.attentes[usager.heure_fin_queue - usager.heure_debut_queue] += 1


class Cache(SeveralFilesCache):
    """Cache des données des simulations de file d'attente."""

    module = "attente"
    cachename = "attente-{}.csv"

    @classmethod
    def lscache(cls, _):
        raise NotImplementedError()

    @classmethod
    def est_sauvegardee(cls, **kwargs):
        return os.path.exists(cls.fichier(cls.format_cachename(**kwargs)))

    @classmethod
    def format_cachename(cls, **kwargs):
        """Renvoit le nom du fichier contenant (ou non) les données mises en cache."""
        options = []
        for key, value in kwargs.items():
            if isinstance(value, functools.partial):
                options.append(
                    key[0]
                    + value.func.__name__
                    + "".join(";" + str(arg) for arg in value.args)
                )
            else:
                options.append(key[0] + str(value))
        return cls.cachename.format("-".join(sorted(options)))

    @classmethod
    def write_cache(cls, data, **kwargs):
        with open(
            cls.fichier(cls.format_cachename(**kwargs)), mode="w", encoding="utf8"
        ) as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            for row in sorted(data.items()):
                writer.writerow(row)

    @classmethod
    def read_cache(cls, **kwargs):
        """Lit dans un fichier les résultats de la simulation sauvegardée.

        Lève une erreur moche si cette simulation n'a pas été sauvegardée.
        """
        effectifs = collections.Counter()
        with open(
            cls.fichier(cls.format_cachename(**kwargs)), encoding="utf8"
        ) as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for row in reader:
                effectifs[int(row[0])] = int(row[1])
        return effectifs


#: Options par défaut pour les simulations
OPTIONS = {
    "guichets": 5,
    "usagers": 1000000,
    "files": 5,
    "arrivee": functools.partial(Exponentielle, 7),
    "service": functools.partial(Normale, 30, 10),
    "discipline": FIFO,
    "choix": Personnes,
    "sortie": TempsAttente,
    "initial": 0,
    "changement": True,
}


@Cache.intercepte()
def simulation(**args):
    """Simule la venue d'usagers.

    Les options utilisées sont celles de la variable :data:`OPTIONS`,
    complétées avec celles données en argument.
    """
    random.seed("1729")
    options = OPTIONS.copy()
    options.update(args)

    with Salle(**options) as salle:
        # pylint: disable=no-member
        while not salle.fini:
            salle.tictac()
        return salle.sortie.attentes


def histogramme_attente():
    """Crée un histogramme des temps d'attente (avec 1 ou 5 files)."""
    attentes1 = simulation(files=1)
    attentes5 = simulation(files=5)

    xlim = (1, 100)
    ylim = (
        0,
        max(
            y
            for x, y in itertools.chain(attentes1.items(), attentes5.items())
            if xlim[0] <= x <= xlim[1]
        ),
    )

    attentes1 = list(zip(*sorted(attentes1.items())))
    attentes5 = list(zip(*sorted(attentes5.items())))

    fig, (axe1, axe2) = plt.subplots(nrows=2, sharey=True)

    # Graphique complet
    axe1.step(x=attentes1[0], y=attentes1[1], label="Une file partagée.")
    axe1.step(x=attentes5[0], y=attentes5[1], label="Une file par guichet.")
    axe1.legend()
    axe1.grid()
    axe1.set(
        xlabel="Temps d'attente (unité arbitraire)",
        ylabel="Effectifs",
    )
    axe1.grid(True)

    # Zoom
    axe2.step(x=attentes1[0], y=attentes1[1], label="Une file partagée.")
    axe2.step(x=attentes5[0], y=attentes5[1], label="Une file par guichet.")
    axe2.legend()
    axe2.grid()
    axe2.set(
        xlabel="Temps d'attente (unité arbitraire)",
        ylabel="Effectifs",
    )
    axe2.grid(True)
    axe2.set_xlim(xlim)
    axe2.set_ylim(ylim)

    fig.suptitle(
        "Temps d'attente des usagers (les changements de files sont autorisés)."
    )
    plt.show()


def heatmap_nombre():
    """Crée une carte "heat map" pour comparer les effets du nombre de files et guichets."""

    moyennes = [[np.nan] * 10 for _ in range(10)]
    ecarttypes = [[np.nan] * 10 for _ in range(10)]
    for guichets in range(1, 11):
        for files in range(1, guichets + 1):
            moyennes[guichets - 1][files - 1] = stats.moyenne(
                simulation(
                    files=files,
                    guichets=guichets,
                    service=functools.partial(Normale, 6 * guichets, 2 * guichets),
                ).items()
            )
            ecarttypes[guichets - 1][files - 1] = stats.ecarttype(
                simulation(
                    files=files,
                    guichets=guichets,
                    service=functools.partial(Normale, 6 * guichets, 2 * guichets),
                ).items()
            )

    seaborn.set()
    fig, (axe1, axe2) = plt.subplots(ncols=2, sharey=True, figsize=(12, 5))

    # Moyennes
    axes = seaborn.heatmap(
        moyennes,
        annot=True,
        xticklabels=range(1, 11),
        yticklabels=range(1, 11),
        fmt=".1f",
        ax=axe1,
    )
    axes.set(
        xlabel="Nombre de files",
        ylabel="Nombre de guichets",
        title="Moyenne",
    )
    axes.invert_yaxis()

    # Écart-type
    axes = seaborn.heatmap(
        ecarttypes,
        annot=True,
        xticklabels=range(1, 11),
        yticklabels=range(1, 11),
        fmt=".1f",
        ax=axe2,
    )
    axes.set(
        xlabel="Nombre de files",
        ylabel="Nombre de guichets",
        title="Écart-type",
    )
    axes.invert_yaxis()

    fig.suptitle("Temps d'attente en fonction du nombre de files et de guichets.")
    plt.show()


def heatmap_strategies():
    """Crée une carte "heat map" pour comparer les différentes stratégies."""
    seaborn.set()

    dictdisciplines = {
        classe.keyword: classe
        for classe in plugins.iter_classes(
            modulediscipline, modulediscipline.Discipline
        )
        if hasattr(classe, "keyword")
    }
    dictchoix = {
        classe.keyword: classe
        for classe in plugins.iter_classes(modulechoix, modulechoix.Choix)
        if hasattr(classe, "keyword")
    }

    data = [
        [
            simulation(
                choix=functools.partial(dictchoix[choix]),
                discipline=functools.partial(dictdisciplines[discipline]),
            )
            for discipline in sorted(dictdisciplines)
        ]
        for choix in sorted(dictchoix)
    ]

    moyennes = [
        [stats.moyenne(attentes.items()) for attentes in ligne] for ligne in data
    ]
    ecarttypes = [
        [stats.ecarttype(attentes.items()) for attentes in ligne] for ligne in data
    ]

    fig, (axe1, axe2) = plt.subplots(ncols=2, sharey=True)

    # Moyennes
    axes = seaborn.heatmap(
        moyennes,
        annot=True,
        xticklabels=sorted(dictdisciplines),
        yticklabels=sorted(dictchoix),
        fmt=".0f",
        ax=axe1,
    )
    axes.set(
        xlabel="Discipline",
        ylabel="Choix",
        title="Moyenne",
    )
    axes.invert_yaxis()

    # Écarts-type
    axes = seaborn.heatmap(
        ecarttypes,
        annot=True,
        xticklabels=sorted(dictdisciplines),
        yticklabels=sorted(dictchoix),
        fmt=".0f",
        ax=axe2,
    )
    axes.set(
        xlabel="Discipline",
        ylabel="Choix",
        title="Écart-type",
    )
    axes.invert_yaxis()

    fig.suptitle("Temps d'attente en fonction des choix et types de files.")
    plt.show()


if __name__ == "__main__":
    histogramme_attente()
    heatmap_nombre()
    heatmap_strategies()
