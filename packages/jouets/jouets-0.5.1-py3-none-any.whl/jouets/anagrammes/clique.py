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

"""Recherche l'ensemble de lettres qui produit le plus grand nombre d'anagrammes."""

import argparse
import collections
import itertools
import sys

import unidecode

from ..utils.aargparse import yesno
from . import iter_mots


def analyseur():
    """Analyse dela ligne de commandes"""

    parser = argparse.ArgumentParser(
        prog="anagrammes.clique",
        description=(
            "Recherche l'ensemble de lettres "
            "qui produit le plus grand nombre d'anagrammes."
        ),
    )
    parser.add_argument(
        "-a",
        "--accents",
        type=yesno,
        default=True,
        help="Considère les lettres accentuées comme distinctes des lettres non accentuées.",
    )
    parser.add_argument(
        "-m",
        "--majuscules",
        type=yesno,
        default=False,
        help=(
            "Accepte (ou non) les mots commençant par une majuscule "
            "(utile pour exclure les noms propres)."
        ),
    )
    parser.add_argument(
        "dict",
        type=str,
        nargs="*",
        help="Dictionnaires dans lesquels aller chercher les mots, sous la forme de fichiers de mots séparés par des espaces ou des sauts de ligne. Les autres caractères sont ignorés. Accepte aussi des arguments sous la forme 'aspell://fr', qui charge tous les mots de la langue 'fr' connus du dictionnaire Aspell.",  # pylint: disable=line-too-long
    )

    return parser


def recherche(dictionnaire, *, accents, majuscules):
    """Recherche le plus grand groupe d'anagrammes.

    :param dictionnaire: Itérable des mots du dictionnaire.
    :param bool accents:
      Conserve (ou non) les accents.
      Si faux, les accents sont ignorés (`chine` et `chiné` sont alors le même mot).
    :param bool majuscules:
      Converse (ou non) les majuscules.
      Si faux, les mots commençant par une majuscule sont ignorés.
    """
    # Construction du dictionnaire groupes :
    # - les clefs sont des listes de lettres (triées par ordre alphabétiques) ;
    # - les valeurs sont l'ensemble des mots rencontrés constitués de ces lettres.
    groupes = collections.defaultdict(set)
    for mot in dictionnaire:
        if (not majuscules) and (mot[0].upper() == mot[0]):
            continue
        if accents:
            clef = mot
        else:
            clef = unidecode.unidecode(mot)
        clef = "".join(sorted(clef.lower()))
        groupes[clef].add(mot)

    # Recherche du plus grand groupe
    grands = []
    taille = 0
    for clef, mots in groupes.items():
        if len(mots) == taille:
            grands.append(clef)
        elif len(mots) > taille:
            taille = len(mots)
            grands = [clef]

    # Résultats
    for clef in grands:
        yield groupes[clef]


def main(args):
    """Fonction principale."""
    arguments = analyseur().parse_args(args)

    for mots in recherche(
        itertools.chain.from_iterable(
            iter_mots(dico, accents=True) for dico in arguments.dict
        ),
        accents=arguments.accents,
        majuscules=arguments.majuscules,
    ):
        print(" ".join(sorted(mots)))


if __name__ == "__main__":
    main(sys.argv[1:])
