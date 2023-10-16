#!/usr/bin/env python3

# Copyright 2023 Louis Paternault
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

"""Génération de tuiles de Truchet"""

# pylint: disable=consider-using-f-string

import argparse
import logging
import random
import sys
import textwrap
from importlib import resources

from .. import truchet
from ..utils import aargparse
from ..utils.erreurs import ErreurUtilisateur
from . import VERSION, templates

DEFAULT_STYLE = {
    "bord": "draw=black, very thick",
    "aretes": "draw=black, very thick",
    "pair": "fill=black",
    "impair": "",
}

DEFAULT_TEMPLATES = list(
    file.name for file in resources.files(templates).iterdir() if file.suffix == ".tex"
)


def analyseur():
    """Renvoie un analyseur de la ligne de commande."""
    # pylint: disable=line-too-long
    parser = aargparse.analyseur(
        prog="truchet",
        description="Génère des tuiles ou des pavages de Truchet.",
        version=VERSION,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "template",
        help=textwrap.dedent(
            """\
                    Patron à utiliser : soit un de ceux fournis avec le programme ({}), soit un fichier.
                    Notez que certaines des autres options sont ignorées selon le patron utilisé.
                    """
        ).format(", ".join(DEFAULT_TEMPLATES)),
    )
    parser.add_argument(
        "--style",
        "-S",
        action="append",
        help="""Style à utiliser, de la forme "nom=arguments", où "arguments" sont des paramêtres au sens de TikZ. La valeur par défaut est équivalente à {}.""".format(  # pylint: disable=consider-using-f-string
            " ".join(f'--style="{key}={value}"' for key, value in DEFAULT_STYLE.items())
        ),
    )
    parser.add_argument(
        "--tuiles",
        "-t",
        help=textwrap.dedent(
            """\
                    Tuiles à utiliser. Peut être :
                    - random : tuiles aléatoires ;
                    - random4 (ou n'importe quel nombre strictement positif) : choisit 4 tuiles aléatoirement, et les utilises de manière aléatoire ;
                    - liste : toutes les tuiles, dans un ordre déterministe ;
                    - liste4 (ou n'importe quel nombre strictement positif) : choisit 4 tuiles aléatoirement, et les utilises toujours dans le même ordre ;
                    - tri : toutes les tuiles, triées (dans un certain ordre…).
                    Dans les deux cas, un nombre égal à zéro est équivalent à ne pas fournir de nombre (c'est-à-dire à utiliser toutes les tuiles).
                    """
        ),
        default="random",
    )
    parser.add_argument(
        "--graine",
        "-g",
        help="Graine de départ pour le générateur pseudo-aléatoire.",
        type=int,
        default=None,
    )
    parser.add_argument(
        "--durete",
        "-d",
        help="Dureté du départ et de l'arrivée des segments au bord des tuiles.",
        default=1,
        type=float,
    )
    parser.add_argument(
        "--cotes",
        "-c",
        help="""Nombre de côtés des figures. Utiliser "--cotes=1" pour utiliser un cercle.""",
        default=4,
        type=int,
    )
    parser.add_argument(
        "--sections",
        "-s",
        help="""Nombre d'arêtes traversant chacun des côtés des tuiles. Notez que pour un polygone, le produit du nombre de côtés par cet argument doit être pair ; pour un cercle, ce nombre doit être pair.""",
        default=2,
        type=aargparse.type_naturel,
    )
    parser.add_argument(
        "--taille",
        "-T",
        help="""Taille (pour les pavagaes uniquement), en nombre de répétitions, de la forme LARGEURxHAUTEUR.""",
        type=aargparse.type_produit_entiers,
        default=(5, 5),
    )

    return parser


def analyse(options):
    """Analyse les options, convertit les valeurs, et signale les éventuelles erreurs."""
    # pylint: disable=too-many-branches
    if options.graine is not None:
        random.seed(options.graine)

    if options.style is None:
        options.style = DEFAULT_STYLE
    else:
        styles = DEFAULT_STYLE
        for style in options.style:
            try:
                key, value = style.split("=", maxsplit=1)
            except ValueError as erreur:
                # pylint: disable=line-too-long
                raise ErreurUtilisateur(
                    f"""Argument "{style}" non valide : les arguments de --style sont de la forme "nom=valeur"."""
                ) from erreur
            if key not in DEFAULT_STYLE:
                raise ErreurUtilisateur(
                    """Argument "{}" non valide : les seuls noms autorisés sont : {}.""".format(
                        style,
                        ", ".join(
                            sorted(DEFAULT_STYLE.keys()),
                        ),
                    )
                )
            styles[key] = value
        options.style = styles

    if options.cotes <= 0 or options.cotes == 2:
        # pylint: disable=line-too-long
        raise ErreurUtilisateur(
            f"""Nombre de côtés "{options.cotes}" invalide : ce nombre doit être 1 (pour un cercle) ou un nombre supérieur ou égal à 3."""
        )
    if options.cotes * options.sections % 2 == 1:
        raise ErreurUtilisateur(
            "Le produit du nombre de côtés par le nombre de sections doit être pair."
        )

    if options.tuiles in ("random", "liste", "tri"):
        options.tuiles = (options.tuiles, 0)
    elif options.tuiles.startswith("random") or options.tuiles.startswith("liste"):
        if options.tuiles.startswith("random"):
            clef = "random"
        else:
            clef = "liste"
        try:
            nombre = int(options.tuiles[len(clef) :])
            if nombre < 0:
                raise ValueError()
        except ValueError as erreur:
            # pylint: disable=line-too-long
            raise ErreurUtilisateur(
                f"""Argument "{options.tuiles}" invalide: "{options.tuiles[len(clef):]}" n'est pas un nombre strictement positif."""
            ) from erreur
        options.tuiles = (clef, nombre)
    else:
        # pylint: disable=line-too-long
        raise ErreurUtilisateur(
            f"""Argument "{options.tuiles}" doit être l'un de : tri, random, liste, randomNOMBRE, listeNOMBRE (où NOMBRE est un nombre entier naturel)."""
        )

    if options.taille[0] <= 0 or options.taille[1] <= 0:
        raise ErreurUtilisateur(
            "La taille doit être un produit de nombres strictement positifs."
        )

    return options


def main():
    """Fonction principale."""

    try:
        # Analyse des options
        options = analyse(analyseur().parse_args())

        # Génération
        print(
            truchet.environment()
            .get_template(options.template)
            .render(
                sections=options.sections,
                durete=options.durete,
                tuiles=truchet.Tuiles(
                    options.cotes * options.sections // 2, *options.tuiles
                ),
                style=options.style,
                côtés=options.cotes,
                taille=options.taille,
            )
        )
    except ErreurUtilisateur as erreur:
        logging.error(str(erreur))
        sys.exit(1)


if __name__ == "__main__":
    main()
