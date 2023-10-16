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

"""Calcul de la durée d'un jeu de bataille."""

import argparse
import collections
import csv
import functools
import itertools
import multiprocessing
import os
import random
import sys
import textwrap

from jouets.utils.cache import SeveralFilesCache

VERSION = "0.1.0"


class Perdu(Exception):
    """Exception levée lorsqu'une joueuse perd la partie."""


class Cache(SeveralFilesCache):
    """Mise en cache des résultats de simulation"""

    module = "bataille"
    cachename = "bataille-{couleurs}-{valeurs}-{nombre}.csv"

    @classmethod
    def write_cache(cls, data, **kwargs):
        with open(
            cls.fichier(cls.cachename.format(**kwargs)), mode="w", encoding="utf8"
        ) as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            for row in data.items():
                writer.writerow(row)

    @classmethod
    def read_cache(cls, **kwargs):
        """Lit dans un fichier les résultats de la simulation sauvegardée.

        Lève une erreur moche si cette simulation n'a pas été sauvegardée.
        """
        effectifs = {}
        with open(
            cls.fichier(cls.cachename.format(**kwargs)), encoding="utf8"
        ) as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for row in reader:
                effectifs[int(row[0])] = int(row[1])
        return effectifs


class Joueuse:
    """Une joueuse de bataille (et son tas de cartes)."""

    def __init__(self, cartes):
        self.cartes = list(cartes)

    def pioche(self):
        """Supprime la première carte du jeu de la joueuse, et la renvoit.

        :raise Perdu: Lorsque la joueuse n'a plus de cartes à piocher.
        """
        try:
            return self.cartes.pop(0)
        except IndexError as error:
            raise Perdu() from error

    def ramasse(self, cartes):
        """Ajoute les cartes à la fin du tas de la joueuse, dans un ordre aléatoire."""
        random.shuffle(cartes)
        self.cartes.extend(cartes)

    def __bool__(self):
        return bool(self.cartes)


class Progression:
    """Affiche la progression (nombre de parties jouées sur nombre de partie total)."""

    def __init__(self, maximum):
        super().__init__()
        self.maximum = maximum
        self.formatstr = f"{{}}/{self.maximum}"

    def tick(self, i):
        """Affiche la progression."""
        if not (i % 1000):  #  pylint: disable=superfluous-parens
            texte = self.formatstr.format(i)
            sys.stderr.write(texte + "\r" * len(texte))

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        # pylint: disable=arguments-differ
        sys.stderr.write(" " * (len(str(self.maximum)) * 2 + 1))
        sys.stderr.write("\r" * (len(str(self.maximum)) * 2 + 1))
        sys.stderr.flush()


@functools.lru_cache()
def paquet(couleurs=4, valeurs=13):
    """Crée un paquet de cartes."""
    return list(itertools.chain.from_iterable(range(valeurs) for _ in range(couleurs)))


def partie(  # pylint: disable=inconsistent-return-statements
    _=None, couleurs=4, valeurs=13
):
    """Joue une partie de bataille, et renvoit sa durée (en nombre de tours)."""

    # Les couleurs ne sont pas différenciées (c'est inutile pour la suite).
    melange = random.sample(paquet(couleurs, valeurs), k=couleurs * valeurs)
    joueuse1 = Joueuse(melange[: len(melange) // 2])
    joueuse2 = Joueuse(melange[len(melange) // 2 :])

    for tour in itertools.count(1):
        try:
            # Les joueuses piochent une carte
            table = []
            carte1 = joueuse1.pioche()
            carte2 = joueuse2.pioche()
            while carte1 == carte2:
                # Bataille
                # Les joueuses posent leur carte sur la table,
                # ainsi qu'une autre carte de leur jeu.
                table.append(carte1)
                table.append(carte2)
                table.append(joueuse1.pioche())
                table.append(joueuse2.pioche())
                # Les joueuses piochent une nouvelle carte.
                carte1 = joueuse1.pioche()
                carte2 = joueuse2.pioche()
            # Les deux cartes des joueuses sont différentes.
            # Le gagnant ramasse les cartes
            # (et celles qui ont été posées sur la table en cas de bataille.).
            if carte1 > carte2:
                joueuse1.ramasse([carte1, carte2] + table)
            else:
                joueuse2.ramasse([carte1, carte2] + table)
            if (not joueuse1) or (not joueuse2):
                raise Perdu()
        except Perdu:
            # Un des deux jouers doit piocher une carte, mais son jeu est vide.
            # La partie est terminée : on renvoit le nombre de tours joués.
            return tour


@Cache.intercepte()
def simule(*, nombre, couleurs=4, valeurs=13):
    """Simule `nombre` parties de bataille, et renvoit un dictionnaire des résultats.

    Le dictionnaire est de la forme `durée: effectif`, signifiant :
    « `effectif` parties de bataille ont duré `durée` tours ».
    """
    effectifs = collections.defaultdict(int)

    mapartie = functools.partial(partie, couleurs=couleurs, valeurs=valeurs)
    try:
        processes = max(1, int(os.environ.get("WORKERS")))
    except TypeError:
        processes = None

    with Progression(nombre) as progres:
        with multiprocessing.Pool(processes=processes) as pool:
            for i, duree in enumerate(pool.imap_unordered(mapartie, range(nombre))):
                progres.tick(i)
                effectifs[duree] += 1

    return effectifs


def affiche_brut(args):
    """Calcule les durées de plusieurs parties, et affiche les données brutes au format CSV."""
    parser = argparse.ArgumentParser(
        prog="bataille.brut",
        description="""Simule des parties, et affiche, sous forme d'un tableau CSV, la liste des paires `(duree, effectif)` : par exemple, `17, 29` signifie que sur l'échantillon, 29 parties se sont arrêtées en 17 plis.""",  # pylint: disable=line-too-long
    )
    parser.add_argument(
        "-n", "--number", type=int, default=1000, help="Number of games to play."
    )
    parser.add_argument(
        "-c",
        "--couleurs",
        type=int,
        default=4,
        help="Nombre de couleurs du jeu de cartes.",
    )
    parser.add_argument(
        "-v",
        "--valeurs",
        type=int,
        default=13,
        help="Nombre de cartes dans chaque couleurs.",
    )
    options = parser.parse_args(args)
    effectifs = simule(
        nombre=options.number, couleurs=options.couleurs, valeurs=options.valeurs
    )

    for duree in sorted(effectifs.keys()):
        print(f"{duree}, {effectifs[duree]}")
