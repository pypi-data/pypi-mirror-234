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

"""Recherche d'anagrammes avec un dictionnaire arborescent : Ligne de commande."""

import argparse
import textwrap

import argdispatch

from jouets.utils.aargparse import type_intervalle, yesno

from . import VERSION, DictionnaireArborescent, Intervalle, clique, shell


def analyse_search():
    """Renvoit un analyseur de ligne de commande pour la commande `search`."""
    parser = argparse.ArgumentParser(
        prog="anagrammes.search",
        description=textwrap.dedent("Recherche des anagrammes."),
        epilog=textwrap.dedent(
            """
        # Intervalles

        Les intervalles sont de la forme :
        - `2:4` : entre 2 et 4 (inclus) ;
        - `:4` : moins de 4 ;
        - `2:` : au moins 2 ;
        - `3` : exactement 3;
        - `:` : indifférent.
        """
        ),
        formatter_class=argdispatch.RawDescriptionHelpFormatter,
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
        "--mots",
        type=type_intervalle,
        default=None,
        help="Nombres de mots de l'anagramme, sous forme d'intervalle (par défaut : autant que le nombre de mots donnés en argument).",  # pylint: disable=line-too-long
    )
    parser.add_argument(
        "-l",
        "--lettres",
        type=type_intervalle,
        default=":",
        help="Nombres de lettres de chaque mot, sous forme d'intervalle.",
    )
    parser.add_argument(
        "-d",
        "--dict",
        type=str,
        required=True,
        action="append",
        help="Dictionnaire dans lequel aller chercher les mots, sous la forme d'un fichier de mots séparés par des espaces ou des sauts de ligne. Les autres caractères sont ignorés. Accepte aussi des arguments sous la forme 'aspell://fr', qui charge tous les mots de la langue 'fr' connus du dictionnaire Aspell.",  # pylint: disable=line-too-long
    )
    parser.add_argument(
        "alphabet",
        type=str,
        nargs="+",
        help="Lettres (ou mots) dont on cherche des anagrammes.",
    )

    return parser


def commande_search(args):
    """Recherche des anagrammes."""

    arguments = analyse_search().parse_args(args)
    if arguments.mots is None:
        arguments.mots = [len(arguments.alphabet)] * 2

    dico = DictionnaireArborescent()
    for fichier in arguments.dict:
        dico.charge(fichier)

    options = {
        "accents": arguments.accents,
        "mots": Intervalle(*arguments.mots),
        "lettres": Intervalle(*arguments.lettres),
    }
    for anagramme in dico.anagrammes(arguments.alphabet, options):
        print(" ".join(anagramme))


def commande_tree(args):
    """Produit le code `dot` dessinant le dictionnaire sous la forme d'un arbre."""
    parser = argparse.ArgumentParser(
        prog="anagrammes.tree",
        description=textwrap.dedent(
            "Affiche le code graphviz de l'arbre arborescent des dictionnaires passés en argument."
        ),
        epilog="Pour visualiser le dictionnaire arborescent, utilisez : `anagrammes.tree DICT | dot -Tpdf > arbre.pdf`",  # pylint: disable=line-too-long
    )
    parser.add_argument(
        "-a",
        "--accents",
        type=yesno,
        default=True,
        help="Considère les lettres accentuées comme distinctes des lettres non accentuées.",
    )
    parser.add_argument(
        "dict",
        type=str,
        nargs="+",
        help="Dictionnaire dans lequel aller chercher les mots, sous la forme d'un fichier de mots séparés par des espaces ou des sauts de ligne. Les autres caractères sont ignorés. Accepte aussi des arguments sous la forme 'aspell://fr', qui charge tous les mots de la langue 'fr' connus du dictionnaire Aspell.",  # pylint: disable=line-too-long
    )

    options = parser.parse_args(args)

    dico = DictionnaireArborescent()
    for dictionnaire in options.dict:
        dico.charge(dictionnaire, accents=options.accents)

    print(dico.dot())


def analyse():
    """Renvoit un analyseur de ligne de commande."""
    parser = argdispatch.ArgumentParser(
        prog="anagrammes",
        description=textwrap.dedent("Recherche des anagrammes."),
        # formatter_class=argdispatch.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {VERSION}"
    )
    subparsers = parser.add_subparsers(dest="commande")
    subparsers.required = True

    subparsers.add_function(commande_tree, command="tree")
    subparsers.add_function(commande_search, command="search")
    subparsers.add_function(shell.main, command="shell")
    subparsers.add_function(clique.main, command="clique")
    return parser


def main():
    """Fonction principale."""
    analyse().parse_args()


if __name__ == "__main__":
    main()
