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

"""Calcule les statistiques des durées de parties de bataille."""

import argparse
import math
import numbers
import textwrap

import numpy as np

from jouets import bataille
from jouets.utils.aargparse import type_intervalle


def titre(texte):
    """Retourne un titre souligné."""
    return f"""{texte}\n{"_"*len(texte)}"""


def get_accumulated(durees, effectifs, indice):
    """Renvoit la première durée dont l'effectif cumulé croissant dépasse l'indice."""
    # pylint: disable=inconsistent-return-statements
    cumules = 0
    for duree, effectif in zip(durees, effectifs):
        cumules += effectif
        if cumules >= indice:
            return duree

    # Inutile, mais sinon Pylint se plaint.
    return durees[-1]


def moyenne(durees, effectifs):
    """Renvoit la moyenne des données."""
    return np.average(durees, weights=effectifs)


def formatte(arg):
    """Formatte l'argument (en arrondissant à 10⁻¹ les nombres)."""
    if isinstance(arg, numbers.Number):
        if math.trunc(arg) == arg:
            return str(arg)
        return f"{arg:.1f}"
    return str(arg)


def mediane(durees, effectifs):
    """Renvoit la médiane des données."""
    total = sum(effectifs)
    if total % 2 == 0:
        return (
            get_accumulated(durees, effectifs, total / 2)
            + get_accumulated(durees, effectifs, total / 2 + 1)
        ) / 2
    return get_accumulated(durees, effectifs, (total + 1) / 2)


def confiance(durees, effectifs):
    """Renvoit l'intervalle de confiance à 95% des données.

    Sous la forme d'un tuple des deux bornes.
    """
    total = sum(effectifs)
    return (
        get_accumulated(durees, effectifs, 0.025 * total),
        get_accumulated(durees, effectifs, 0.975 * total),
    )


def strconfiance(durees, effectifs):
    """Renvoit l'intervalle de confiance, sous la forme d'une chaîne de caractères."""
    # pylint: disable=consider-using-f-string
    return "[ {} ; {} ]".format(
        *(formatte(borne) for borne in confiance(durees, effectifs))
    )


def parite(durees, effectifs):
    """Renvoit la parité la plus fréquente."""
    pair = sum(eff for dur, eff in zip(durees, effectifs) if dur % 2 == 0)
    impair = sum(eff for dur, eff in zip(durees, effectifs) if dur % 2 == 1)
    if pair > 1.5 * impair:
        return "P"
    if impair > 1.5 * pair:
        return "I"
    return "≈"


def mode(durees, effectifs):
    """Renvoit le mode des données."""
    if not durees:
        return None

    return max((eff, dur) for dur, eff in zip(durees, effectifs))[1]


def formatte_tableau(tableau, *, couleurs, valeurs):
    """Renvoit le tableau au format rst.

    Précondition : Toutes les lignes du tableau font la même taille.
    """
    tableau = [
        [r"↓Couleurs \\ Valeurs→"]
        + [formatte(valeur) for valeur in range(valeurs[0], valeurs[1] + 1)]
    ] + [
        [formatte(couleurs[0] + i)] + tableau[i]
        for i in range(0, couleurs[1] - couleurs[0] + 1)
    ]

    largeurs = [
        max(len(formatte(ligne[colonne])) for ligne in tableau)
        for colonne in range(len(tableau[0]))
    ]
    ligne_separatrice = (
        "+-"
        + "-+-".join("-" * largeurs[colonne] for colonne in range(len(tableau[0])))
        + "-+"
        + "\n"
    )
    lignes = [""]
    for ligne in tableau:
        lignes.append(
            "| "
            + " | ".join(
                # pylint: disable=consider-using-f-string
                "{cellule:>{largeur}}".format(
                    cellule=formatte(ligne[colonne]), largeur=largeurs[colonne]
                )
                for colonne in range(len(ligne))
            )
            + " |"
            + "\n"
        )
    lignes.append("")
    print(ligne_separatrice.join(lignes))


def map2d(fonction, *, couleurs, valeurs, nombre):
    """Applique `fonction` à toutes les combinaisons de couleurs et valeurs.

    Couleurs et valeurs sont des intervalles (sous la forme d'un tuple `(début, fin)` ;
    `nombre` est la taille de l'échantillon.

    Les données sont calculées (par une simulation) ou cherchées dans le cache
    (ce qui est fait automatiquement lors d'un appel à :func:`simule`.
    """
    tableau = []
    for couleur in range(couleurs[0], couleurs[1] + 1):
        ligne = []
        for valeur in range(valeurs[0], valeurs[1] + 1):
            dictionnaire = bataille.simule(
                nombre=nombre, couleurs=couleur, valeurs=valeur
            )
            ligne.append(fonction(*zip(*sorted(dictionnaire.items()))))
        tableau.append(ligne)

    return tableau


INDICATEURS = [
    ("Moyennes", moyenne),
    ("Modes", mode),
    ("Médianes", mediane),
    ("Intervalles de confiance", strconfiance),
    ("Parité des durées la plus courante", parite),
]


def intervalle(debut, fin):
    """Renvoit l'intervalle, en complétant intelligemment les bornes `None`.

    Par exemple :

    >>> intervalle(None, 3)
    (0, 3)
    >>> intervalle(1, 8)
    (1, 8)
    >>> intervalle(None, None)
    (0, 1)
    """
    if debut is None:
        debut = 0
    if (fin is None) or (fin < debut):
        fin = debut + 1
    return (debut, fin)


def multistat(args):
    """Calcule les statistiques des durées des parties (plusieurs configurations)."""

    parser = argparse.ArgumentParser(
        prog="bataille.stat",
        description=textwrap.dedent(
            """\
        Calcule les statistiques des durées des parties (plusieurs configurations).
    """
        ),
    )
    parser.add_argument(
        "-n", "--number", type=int, default=1000, help="Number of games to play."
    )
    parser.add_argument(
        "-c",
        "--couleurs",
        type=type_intervalle,
        default=[1, 5],
        help="Nombre de couleurs du jeu de cartes (intervalle de la forme `DEBUT:FIN`).",
    )
    parser.add_argument(
        "-v",
        "--valeurs",
        type=type_intervalle,
        default=[1, 5],
        help="Nombre de cartes dans chaque couleurs (intervalle de la forme `DEBUT:FIN`).",
    )
    options = parser.parse_args(args)

    couleurs = intervalle(*options.couleurs)
    valeurs = intervalle(*options.valeurs)

    for nom, fonction in INDICATEURS:
        print(titre(nom))
        print()
        formatte_tableau(
            map2d(fonction, couleurs=couleurs, valeurs=valeurs, nombre=options.number),
            couleurs=couleurs,
            valeurs=valeurs,
        )
        print()


def stat(args):
    """Calcule les statistiques des durées des parties (une seule configuration)."""

    parser = argparse.ArgumentParser(
        prog="bataille.stat",
        description=textwrap.dedent(
            """\
            Calcule les statistiques des durées des parties (une seule configuration).
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
        "-f",
        "--format",
        type=str,
        default=textwrap.dedent(
            """\
                    Min : {minimum}, Max : {maximum}.
                    Moyenne : {moyenne:.1f}, Médiane : {mediane:.1f}, Mode : {mode}.
                    Intervalle de confiance : [{icmin} ; {icmax}].\
                    """
        ),
        help="""Format de la sortie ; cette chaîne peut inclure "{moyenne}", "{mediane}", "{mode}", "{minimum}", "{maximum}", "{icmin}", "{icmax}" (bornes inférieure et supérieure de l'intervalle de confiance à 95%%).""",  # pylint: disable=line-too-long
    )

    options = parser.parse_args(args)

    dictionnaire = bataille.simule(
        nombre=options.number, couleurs=options.couleurs, valeurs=options.valeurs
    )
    durees, effectifs = list(zip(*sorted(dictionnaire.items())))

    print(
        options.format.format(
            moyenne=moyenne(durees, effectifs),
            mediane=mediane(durees, effectifs),
            minimum=min(durees),
            maximum=max(durees),
            mode=mode(durees, effectifs),
            icmin=confiance(durees, effectifs)[0],
            icmax=confiance(durees, effectifs)[1],
        )
    )
