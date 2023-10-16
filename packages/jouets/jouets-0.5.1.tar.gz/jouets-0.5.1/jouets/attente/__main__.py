#!/usr/bin/env python3

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

"""Simulation de files d'attente"""

import argparse
import functools
import random
import re

from jouets.utils import aargparse, plugins

from . import VERSION, Salle, choix, discipline, loiproba, sortie

RE_CLASSE_ARGUMENT = re.compile(r"^(?P<classe>\w+)(:(?P<argument>.*))?$")


def _type_naturel_etoile(texte):
    message = "L'argument est un nombre entier strictement positif."
    try:
        nombre = int(texte)
    except ValueError as error:
        raise argparse.ArgumentTypeError(message) from error
    if nombre <= 0:
        raise argparse.ArgumentTypeError(message)
    return nombre


def _type_sousclasse(module, classe):
    def _type_generique(texte):
        message = "Aucune option trouvée avec ce nom là."
        match = RE_CLASSE_ARGUMENT.match(texte)
        if not match:
            raise argparse.ArgumentTypeError(message)
        groups = match.groupdict()
        name, args = groups["classe"], groups["argument"]
        if args is None:
            args = []
        else:
            args = args.split(":")

        for obj in plugins.iter_classes(module, classe):
            if not hasattr(obj, "keyword"):
                continue
            if obj.keyword.startswith(name):
                return functools.partial(obj, *args)
        raise argparse.ArgumentTypeError(message)

    return _type_generique


def _decrit_options(module, classe):
    options = []
    for obj in plugins.iter_classes(module, classe):
        if not hasattr(obj, "keyword"):
            continue
        options.append((obj.keyword, plugins.get_description(obj)))
    return "\n".join(f"- {name} : {doc}" for name, doc in sorted(options))


def analyse():
    """Renvoie un analyseur de la ligne de commande."""
    # pylint: disable=line-too-long
    parser = aargparse.analyseur(
        version=VERSION,
        prog="attente",
        description="Simulation de files d'attente",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "-g",
        "--guichets",
        type=_type_naturel_etoile,
        help="Nombre de guichets (défaut : 5).",
        default=5,
    )

    parser.add_argument(
        "-u",
        "--usagers",
        type=_type_naturel_etoile,
        help="Nombre d'usagers (défaut : 1000).",
        default=1000,
    )

    parser.add_argument(
        "-f",
        "--files",
        type=_type_naturel_etoile,
        help="Nombre de files d'attente (doit être inférieur ou égal au nombre de guichets ; défaut : 3).",
        default=3,
    )

    parser.add_argument(
        "-r",
        "--random",
        type=str,
        help="Graine du générateur aléatoire (la même graine génèrera les mêmes usagers).",
        default=None,
    )

    parser.add_argument(
        "-a",
        "--arrivee",
        type=_type_sousclasse(loiproba, loiproba.LoiProba),
        help="Loi de probabilité définissant l'arrivée d'un nouvel usager (depuis l'ancien).\n"
        + _decrit_options(loiproba, loiproba.LoiProba),
        default="exp:7",
    )

    parser.add_argument(
        "-s",
        "--service",
        type=_type_sousclasse(loiproba, loiproba.LoiProba),
        help="Loi de probabilité définissant la durée du service.\n"
        + _decrit_options(loiproba, loiproba.LoiProba),
        default="normale:30:10",
    )

    parser.add_argument(
        "-c",
        "--choix",
        type=_type_sousclasse(choix, choix.Choix),
        help="Algorithme de choix d'une file par un usager.\n"
        + _decrit_options(choix, choix.Choix),
        default="personnes",
    )
    parser.add_argument(
        "-d",
        "--discipline",
        type=_type_sousclasse(discipline, discipline.Discipline),
        help="Algorithme de choix du prochain usager dans une file.\n"
        + _decrit_options(discipline, discipline.Discipline),
        default="fifo",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="sortie",
        type=_type_sousclasse(sortie, sortie.Sortie),
        help="Type de données à afficher.\n" + _decrit_options(sortie, sortie.Sortie),
        default="moyenne",
    )

    parser.add_argument(
        "-i",
        "--initial",
        type=int,
        help="Nombre d'usagers dans chaque file au début de la simulation. Ces usagers ne sont pas comptabilisés dans les statistiques.",
        default=0,
    )

    parser.add_argument(
        "-C",
        "--changement",
        type=aargparse.yesno,
        help="Les usagers peuvent changer de file si un guichet est disponible.",
        default=False,
    )

    return parser


def main():
    """Fonction principale."""
    options = vars(analyse().parse_args())

    if options["random"] is not None:
        random.seed(options["random"])
    options.pop("random")

    with Salle(**options) as salle:
        # pylint: disable=no-member
        while not salle.fini:
            salle.tictac()


if __name__ == "__main__":
    main()
