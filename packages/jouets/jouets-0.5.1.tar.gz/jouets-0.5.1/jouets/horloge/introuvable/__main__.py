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

"""Horloge introuvable (avec position aléatoire des heures). Ligne de commande."""

import argparse
import random
import sys
import textwrap

from jouets.utils import aargparse

from . import COULEURS, Horloge

VERSION = "0.1.0"


class _ActionCouleur(argparse.Action):
    # pylint: disable=too-few-public-methods
    def __call__(self, parser, namespace, values, option_string=None):
        if (self.dest not in namespace) or (not getattr(namespace, self.dest)):
            setattr(namespace, self.dest, {})
        élément, couleur = values[0]
        getattr(namespace, self.dest)[élément] = couleur


def alea1():
    """Position aléatoire des heures 1.

    Les heures sont placées aux mêmes angles que sur une horloge classique,
    mais avec un ordre aléatoire.
    """
    return {
        heure: 30 * indice for indice, heure in enumerate(random.sample(range(12), 12))
    }


def alea2():
    """Position aléatoire des heures 2.

    Chaque heure est placée sur le cadrant suivant un angle aléatoire.
    """
    return {heure: random.randrange(360) for heure in range(12)}


def alea3():
    """Position aléatoire des heures 3.

    Sélectionne un nombre aléatoire d'heures,
    et les positionne de manière aléatoire sur le cadrant
    (toutes les heures ne sont donc pas placées).
    """
    return {
        heure: random.randrange(360)
        for heure in random.sample(range(12), random.randint(2, 12))
    }


ALEA = {fonction.__name__: fonction for fonction in (alea1, alea2, alea3)}


class _ActionHeures(argparse.Action):
    """Analyse des arguments renseignant la position des heures."""

    # pylint: disable=too-few-public-methods

    def __call__(self, parser, namespace, values, option_string=None):
        """Analyse des arguments.

        Suivant les arguments, complète un dictionnaire où :
        - les clefs sont les heures ;
        - les valeurs sont l'angle à laquelle afficher cette heure.
        """
        # pylint: disable=too-many-branches
        if len(values) == 0:
            # Aucun argument : choix au hasard
            values = ["alea"]

        if len(values) == 1:
            # Un argument : choix au hasard, ou erreur
            if values[0] == "alea":
                values = [random.choice(list(ALEA))]
            if values[0] in ALEA:
                setattr(namespace, self.dest, ALEA[values[0]]())
                return

            # Argument non reconnu : Erreur.
            raise argparse.ArgumentTypeError(
                # pylint: disable=line-too-long
                f"""Entre 2 et 12 heures doivent être données, ou une des valeurs spéciales : {", ".join(ALEA)}."""
            )

        if ":" in values[0]:
            # Plusieurs arguments. Les heures sont données avec leurs angles
            angles = {}
            for arg in values:
                try:
                    if arg.count(":") != 1:
                        raise ValueError
                    heure, angle = arg.split(":")
                    if int(heure) in angles:
                        raise argparse.ArgumentTypeError(
                            f"L'heure '{heure}' apparait (au moins) deux foix."
                        )
                    angles[int(heure) % 12] = float(angle)
                except ValueError as error:
                    raise argparse.ArgumentTypeError(
                        f"'{arg}' devrait être de la forme 'heure:angle'."
                    ) from error
        else:
            # Plusieurs arguments
            # Les heures sont données comme une suite de nombres.
            # La vérification des arguments peut se faire en une ligne,
            # mais la boucle permet de chercher les erreurs
            # et d'afficher un message clair.
            entiers = []
            for arg in values:
                try:
                    nombre = int(arg)
                    if not 1 <= nombre <= 12:
                        raise ValueError
                    if nombre in entiers:
                        raise argparse.ArgumentTypeError(
                            f"L'heure '{arg}' apparait (au moins) deux foix."
                        )
                    entiers.append(nombre)
                except ValueError as error:
                    raise argparse.ArgumentTypeError(
                        f"'{arg}' devrait être un nombre entier compris entre 1 et 12."
                    ) from error
            angles = {
                heure % 12: (360 * indice) / len(entiers)
                for indice, heure in enumerate(entiers)
            }

        setattr(namespace, self.dest, angles)


def _type_couleur(texte):
    if texte.count(":") == 3:
        élément, *couleur = texte.strip().split(":")
        if élément in COULEURS:
            try:
                return élément, tuple(int(trame) for trame in couleur)
            except ValueError:
                # Sera levée par la fin de la fonction
                pass
    raise argparse.ArgumentTypeError(
        # pylint: disable=line-too-long
        f"L'argument '{texte}' doit être de la forme 'élément:R:G:B' (par exemple 'secondes:255:0:0' pour l'aiguille des secondes en rouge)."
    )


def analyse():
    """Renvoie un analyseur de la ligne de commande."""

    # pylint: disable=line-too-long

    analyseur = aargparse.analyseur(
        VERSION,
        description="Affiche une « horloge introuvable ».",
        epilog="Cette horloge a été inventée par Jacques Carelman, dans sont « Catalogue des objets introuvables ».",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    analyseur.add_argument(
        "-c",
        "--couleur",
        type=_type_couleur,
        action=_ActionCouleur,
        nargs=1,
        help=textwrap.dedent(
            """\
            Couleurs de l'horloge, sous la forme 'heures=red'. Les paramètres à colorier (avec leur valeur par défaut) sont :
            - heures : aiguille des heures (noire) ;
            - minutes : aiguille des minutes (noire) ;
            - secondes : aiguille des secondes (rouge) ;
            - fond : couleur de fond (blanc) ;
            - chiffres : chiffres des heures (noir).
            """
        ),
    )
    analyseur.add_argument(
        "-d",
        "--decalage",
        type=float,
        default=0,
        help="Décalage des angles par rapport à leur spécification, seulement si les nombres ne sont pas définis par leurs angles.",
    )
    analyseur.add_argument(
        "-v",
        "--vitesse",
        default=1,
        type=float,
        help="Vitesse de l'horloge (défaut 1 ; l'horloge indique alors l'heure).",
    )
    analyseur.add_argument(
        "-t", "--taille", default=None, type=int, help="Taille de l'horloge en pixels."
    )
    analyseur.add_argument(
        "heures",
        action=_ActionHeures,
        nargs="*",
        help=textwrap.dedent(
            f"""\
            Position des heures. Il y a plusieurs manières de les définir :
            - [{", ".join(ALEA)}] : disposition aléatoire des heures, suivant différents algorithmes ;
            - vide ou "alea" : la position des heures est choisie au hasard, selon un des algorithmes suscités (choisi évidemment aléatoirement) ;
            - "1 2 3 4 5 6 7 8 9 10 11 12" : par la suite les heures dans le sens des aiguilles d'une montre, en terminant à la verticale (la valeur de l'option --decalage est alors définie, par défaut, pour que la dernière heure spécifiée soit en haut) ;
            - "1:30 2:60 3:90 … 12:0" : en précisant l'angle de chaque nombre.
            Dans les deux derniers cas, il est possible de ne pas indiquer toutes les heures.
            """
        ),
    )

    return analyseur


def main():
    """Fonction principale"""
    arguments = analyse().parse_args()

    for heure in arguments.heures:
        arguments.heures[heure] = (arguments.heures[heure] + arguments.decalage) % 360

    try:
        Horloge(
            couleurs=arguments.couleur,
            angles=arguments.heures,
            taille=arguments.taille,
            vitesse=arguments.vitesse,
        ).loop()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
