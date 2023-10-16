#!/usr/bin/env python3

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

"""Affiche des représentations graphiques des durées des parties de bataille."""

import argparse
import textwrap

import matplotlib.pyplot as plt

from jouets import bataille
from jouets.utils.aargparse import yesno


def histogramme(couleurs, valeurs, nombre, *, titre=None, etendue=10):
    """Affiche l'histogramme des durées."""
    dictionnaire = bataille.simule(nombre=nombre, couleurs=couleurs, valeurs=valeurs)
    durees, effectifs = list(zip(*sorted(dictionnaire.items())))

    plt.hist(
        x=durees,
        weights=effectifs,
        histtype="stepfilled",
        bins=range(min(durees), max(durees), etendue),
    )
    plt.grid()
    if titre is None:
        plt.title(
            f"Durées de {nombre} de parties de bataille ({couleurs} couleurs de {valeurs} cartes)"
        )
    else:
        plt.title(titre)
    plt.xlabel("Durée (en nombre de tours)")
    plt.ylabel("Effectifs")
    plt.grid(True)
    plt.show()


def pairimpair(couleurs, valeurs, nombre, *, titre=None):
    """Affiche les courbes des durées paires et impaires."""
    effectifs = bataille.simule(nombre=nombre, couleurs=couleurs, valeurs=valeurs)
    pair = list(zip(*((d, e) for (d, e) in sorted(effectifs.items()) if d % 2 == 0)))
    impair = list(zip(*((d, e) for (d, e) in sorted(effectifs.items()) if d % 2 == 1)))
    if not pair:
        pair = [(), ()]
    if not impair:
        impair = [(), ()]
    plt.step(x=pair[0], y=pair[1], label="Pair")
    plt.step(x=impair[0], y=impair[1], label="Impair")

    plt.legend()
    plt.grid()
    if titre is None:
        plt.title(
            f"Durées de {nombre} de parties de bataille ({couleurs} couleurs de {valeurs} cartes)"
        )
    else:
        plt.title(titre)
    plt.xlabel("Durée (en nombre de tours)")
    plt.ylabel("Effectifs")

    plt.grid(True)
    plt.show()


def affiche(args):
    """Affiche un graphique des durées des parties."""

    parser = argparse.ArgumentParser(
        prog="bataille.plot",
        description=textwrap.dedent(
            """\
    Simule des parties, et affiche un graphique des durées des parties obtenues.
    """
        ),
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
    parser.add_argument(
        "-e",
        "--etendue",
        type=int,
        default=10,
        help="Étendue des classes (pour `parite=no` uniquement).",
    )
    parser.add_argument(
        "-p",
        "--parite",
        type=yesno,
        default=False,
        help="Sépare les durées paires des durées impaires.",
    )

    options = parser.parse_args(args)

    if options.parite:
        pairimpair(options.couleurs, options.valeurs, options.number)
    else:
        histogramme(
            options.couleurs, options.valeurs, options.number, etendue=options.etendue
        )
