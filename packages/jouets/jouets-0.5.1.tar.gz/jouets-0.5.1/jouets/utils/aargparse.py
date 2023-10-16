#!/usr/bin/env python3

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

"""Outils pour l'analyse des arguments de ligne de commande"""

import argparse
import re


def yesno(texte):
    """Interprète un texte comme un booléen"""
    return texte.lower() in ["y", "yes", "1", "o", "oui"]


INTERVALLE_RE = re.compile(r"(?P<bas>\d*):(?P<haut>\d*)")


def type_intervalle(texte):
    """Interprète un texte comme un intervalle.

    >>> type_intervalle("4")
    [4, 4]
    >>> type_intervalle(":")
    [None, None]
    >>> type_intervalle("1:4")
    [1, 4]
    >>> type_intervalle(":5")
    [None, 5]
    >>> type_intervalle("4:")
    [4, None]
    >>> type_intervalle("4.4:")
    Traceback (most recent call last):
      ...
    argparse.ArgumentTypeError: "4.4:" is not in the format INT:INT.
    """
    try:
        entier = int(texte)
        if entier >= 0:
            return [entier, entier]
    except ValueError:
        pass
    match = INTERVALLE_RE.match(texte)
    if match is not None:
        bas = match.groupdict()["bas"]
        if bas:
            bas = int(bas)
        else:
            bas = None
        haut = match.groupdict()["haut"]
        if haut:
            haut = int(haut)
        else:
            haut = None
        return [bas, haut]
    raise argparse.ArgumentTypeError(f'"{texte}" is not in the format INT:INT.')


def type_naturel(texte):
    """Interprète un texte comme un entier."""
    try:
        entier = int(texte)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            f"'{texte}' must be a positive integer."
        ) from error
    if entier < 0:
        raise argparse.ArgumentTypeError(f"'{texte}' must be a positive integer.")
    return entier


def type_produit_entiers(texte):
    """Interprète un texte comme un produit d'entiers.

    >>> type_produit_entiers("4x8")
    (4, 8)
    >>> type_produit_entiers("2×0")
    (2, 0)
    """
    for séparateur in "x×":
        try:
            gauche, droite = texte.split(séparateur, maxsplit=1)
            return (int(gauche), int(droite))
        except ValueError:
            continue
    raise argparse.ArgumentTypeError(f"'{texte}' doit être de la forme ENTIERxENTIER.")


def analyseur(version, *args, **kwargs):
    """Renvoie un analyseur syntaxique

    Cet analyseur a l'option `--version`.
    """
    parser = argparse.ArgumentParser(*args, **kwargs)
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {version}",
    )
    return parser
