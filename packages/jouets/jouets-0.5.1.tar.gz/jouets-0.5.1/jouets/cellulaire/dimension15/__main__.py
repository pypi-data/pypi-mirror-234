# Copyright 2019-2023 Louis Paternault
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

"""Automate cellulaire en dimension 1,5 : programme.

Un peu plus qu'une ligne (dimension 1), un peu moins qu'un plan (dimension 2).
"""

import argparse
import itertools
import os
import random
import sys
import textwrap
import time

try:
    import blessings

    if os.getenv("UNITTEST", ""):
        LARGEUR = 80
    else:
        LARGEUR = blessings.Terminal().width
except ImportError:
    print(
        """Installez "blessings" pour que la largeur du terminal soit automatiquement détectée.""",
        file=sys.stderr,
    )
    LARGEUR = 80

# pylint: disable=relative-beyond-top-level
# Voir https://github.com/PyCQA/pylint/issues/1667
from ...utils import aargparse
from .. import VERSION

################################################################################
# Conversion de texte vers types


def analyse_regles(text):
    """Vérifie la validité des règles (ou génère des règles aléatoires)."""
    if text == "random":
        return "".join(random.choices("=+-", k=6))
    if len(text) != 6 or not (set(text) <= {"+", "-", "="}):
        raise argparse.ArgumentTypeError(
            """La règle doit être composée de six caractères parmi "+", "-", "="."""
        )
    return text


def analyse_bords(text):
    """Renvoit deux itérateurs à partir du texte.

    Ces itérateurs, infinis, donnent la suite des cellules (vide ou
    pleine) sur chacun des deux bords gauche et droit.

    - "101001010" : Le texte est coupé en deux.
      La première moitié, bouclée, correspond au bord gauche ; la
      seconde moitié, au bord droit.
    - "random" : Bords aléatoires.
    """
    if text == "random":
        return (randominfini(), randominfini())
    if text == "":
        return None

    if not set(text) <= {"0", " ", "1", "X"}:
        raise argparse.ArgumentTypeError(
            """Le bord doit être "random", ou composé de caractères parmi "01 X"."""
        )
    if len(text) % 2 != 0:
        raise argparse.ArgumentTypeError(
            """Le bord doit avoir un nombre de caractères pair."""
        )

    gauche = text[: len(text) // 2]
    droite = text[len(text) // 2 :]
    if not gauche:
        gauche = " "
    if not droite:
        droite = " "

    return (
        itertools.cycle(iter2cellules(gauche)),
        itertools.cycle(iter2cellules(droite)),
    )


def analyse_initial(text):
    """Renvoit un couple d'itérateurs à partir du texte.

    Ces itérateurs correspondent aux deux premières lignes.
    Ils sont infinis ; ils seront tronqués par la suite.

    - "10010101" : Chaque ligne boucle sur ces cellules.
    - "101,10101" : Les deux lignes sont séparées par une virgule.
    - "random" : Lignes générées aléatoirement.
    """
    if text == "random":
        return (randominfini(), randominfini())

    if not set(text) <= {"0", " ", "1", "X", ","}:
        raise argparse.ArgumentTypeError(
            """Les lignes doivent être "random", ou composées de caractères parmi "01 X" (séparées par une virgule)."""  # pylint: disable=line-too-long
        )

    if "," not in text:
        text = text + "," + text

    return [itertools.cycle(iter2cellules(ligne)) for ligne in text.split(",")]


def randominfini():
    "Itérateur infini de booléens aléatoires." ""
    while True:
        yield random.choice([True, False])


def iter2cellules(iterateur):
    """Convertit un itérateur de caractères en un itérateur de booléens."""
    for char in iterateur:
        yield char not in "  0"


################################################################################
# Constantes


SCENARIOS = {
    "planeur": {
        "regles": analyse_regles("=-+-=+"),
        "bords": None,
        "initial": [
            iter2cellules(itertools.chain("001011111", itertools.cycle("0"))),
            iter2cellules(itertools.chain("000011101", itertools.cycle("0"))),
        ],
    },
    "random": {
        "regles": analyse_regles("random"),
        "bords": analyse_bords("random"),
        "initial": analyse_initial("random"),
    },
    "original": {
        "regles": analyse_regles("--++=-"),
        "bords": analyse_bords("  "),
        "initial": analyse_initial("random"),
    },
}
for numero, regles in enumerate(
    [
        "+++-+=",
        "++-++-",
        "++-+=-",
        "++-=+-",
        "+-++-+",
        "+-+-=-",
        "+-+-==",
        "+-+=-=",
        "+--++-",
        "+--+==",
        "+-=+-=",
        "+-=+=-",
        "+-=-++",
        "+-=-+=",
        "+-=--+",
        "+-=--=",
        "+-=-=+",
        "+-=-==",
        "+-==+-",
        "+-==-+",
        "+=+=+-",
        "+=-+--",
        "+=-+-=",
        "+=-+=-",
        "+=--++",
        "+=--+-",
        "+=--+=",
        "+=--=+",
        "+=-=+-",
        "+==-+-",
        "+==-+=",
        "-++-+=",
        "-++-=+",
        "-++-==",
        "-+-+-+",
        "-+=+=-",
        "-+=-+=",
        "-+==+-",
        "--++=-",
        "--+-+=",
        "--+=-+",
        "-=+-+=",
        "-=+-=+",
        "-=+=+-",
        "=++-+-",
        "=++-+=",
        "=+-++-",
        "=+-+-=",
        "=+-+=-",
        "=+--++",
        "=+--+=",
        "=+-=+-",
        "=+=-++",
        "=+=-+-",
        "=-++-=",
        "=-++=-",
        "=-+-++",
        "=-+-+-",
        "=-+-+=",
        "=-+=+-",
        "=-+=-+",
        "==+-+-",
        "==+--+",
        "==+-=+",
        "==-++-",
    ]
):
    SCENARIOS[str(numero)] = {"regles": analyse_regles(regles)}

################################################################################
# Analyse de la ligne de commandes


def _type_strictement_positif(text):
    try:
        entier = int(text)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            f"""L'argument '{text}' doit être un nombre strictement positif."""
        ) from error
    if entier <= 0:
        raise argparse.ArgumentTypeError(
            f"""L'argument '{text}' doit être un nombre strictement positif."""
        )
    return entier


def analyseur():
    """Renvoit un analyseur de ligne de commande."""
    parser = aargparse.analyseur(
        version=VERSION,
        prog="cellulaire.dimension15",
        description=textwrap.dedent("Automate cellulaire exécutable à la main."),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-r",
        "--regles",
        type=analyse_regles,
        default=None,
        help=textwrap.dedent(
            """\
        Règles à appliquer, sous la forme d'une suite de six caractères parmi '-=+'.
        Par exemple, '--regles="--==++"' signifie qu'une cellule
        meurt (-) si elle est entourée d'aucune ou une autre cellule vivante,
        ne change pas d'état (=) avec deux ou trois autres cellules vivantes,
        reste vivante ou naît (+) avec quatre ou cinq cellules vivantes.
        Cette valeur peut aussi être "random" pour sélectionner aléatoirement les règles.
        """
        ),
    )

    parser.add_argument(
        "-b",
        "--bords",
        type=analyse_bords,
        default=None,
        help=textwrap.dedent(
            """\
            Bords de la zone,
            sous la forme d'une suite de 0 (cellule morte) et de 1 (cellule vivante).
            Cette suite est coupée en deux,
            et définit une suite d'états répétés pour les bords gauche et droit.
            Par exemple, "--bords=0100" signifie que
            le bord gauche (01) alterne avec des cellules mortes et vivantes,
            alors que le bord droit (00) n'a que des cellules mortes.
            La valeur prise peut aussi être "random" (état aléatoire à chaque ligne),
            et "" (vide) si les deux bords se rejoignent.
            """
        ),
    )

    parser.add_argument(
        "-d",
        "--delai",
        type=float,
        default=0.1,
        help="Attente (en secondes) entre l'affichage de deux lignes consécutives.",
    )

    parser.add_argument(
        "-l",
        "--largeur",
        type=_type_strictement_positif,
        default=None,
        help="Taille de chaque ligne. Par défaut (si elle peut être déterminée), la largeur du terminal est utilisée.",  # pylint: disable=line-too-long
    )

    parser.add_argument(
        "-i",
        "--initial",
        type=analyse_initial,
        default=None,
        help=textwrap.dedent(
            """\
            Valeur initiale des lignes de cellules,
            sous la forme d'une série de 0 (état mort) et de 1 (état vivant)
            (les deux premières lignes sont identiques, et bouclent sur l'argument),
            sous la forme de deux séries de 0 et de 1 séparées par une virgule
            (définissant chacune des deux premières lignes),
            ou "random" pour deux premières lignes aléatoires.
            """
        ),
    )

    parser.add_argument(
        "-s",
        "--scenario",
        type=str,
        choices=SCENARIOS.keys(),
        help=textwrap.dedent(
            """\
            Scénario à charger.
            Voir l'option --liste pour afficher la liste des scénarios disponibles.
            """
        ),
    )

    parser.add_argument(
        "--liste", action="store_true", help="Liste les scénarios disponibles."
    )

    return parser


################################################################################

DESSINS = {
    True: {
        (False, True): "▀",
        (True, True): "▀",
        (False, False): "·",
        (True, False): "·",
    },
    False: {
        (False, False): "·",
        (True, False): "▀",
        (False, True): "▄",
        (True, True): "█",
    },
}


class BoiteAPetri:
    """Boîte à pétri sans bords.

    Les cellules à gauche et à droite sont adjacentes.
    """

    def __init__(self, options):
        self.delai = options.delai
        self.regles = options.regles
        self._pair = False

        if options.largeur is None:
            largeur = LARGEUR
        else:
            largeur = options.largeur

        # Lignes
        self.lignes = [[], list(itertools.islice(options.initial[0], largeur)), []]
        for cellule in itertools.islice(options.initial[1], largeur):
            self.ajoute(cellule)
        self.findeligne()

    def ajoute(self, cellule):
        """Ajoute une cellule à la fin de la dernière ligne."""
        self.lignes[0].append(cellule)
        self.dessine(len(self.lignes[0]) - 1)

    def dessine(self, i):
        """Dessine la cellule de la dernière ligne, d'indice `i`."""
        print(DESSINS[self._pair][self.lignes[1][i], self.lignes[0][i]], end="")
        sys.stdout.flush()

    def findeligne(self):
        """Actions effectuées à la fin de la ligne.

        Mise à jour de l'attribut `self.lignes`, retour à la ligne, etc.
        """
        self._pair = not self._pair
        self.lignes = [[], self.lignes[0], self.lignes[1]]
        time.sleep(self.delai)

        if self._pair:
            print()
        else:
            print(chr(8) * len(self), end="")

    def __len__(self):
        return len(self.lignes[1])

    def acalculer(self):
        """Itère les indices des cellules à calculer en appliquant les règles.

        Ici, toutes les cellules sont à calculer.
        """
        yield from range(len(self))

    def mainloop(self):
        """Calcule et affiche les lignes suivantes de l'automate."""
        while True:
            for i in self.acalculer():
                cellule = self.regles[
                    sum(
                        [
                            self.lignes[1][(i - 1) % len(self)],
                            self.lignes[1][(i + 1) % len(self)],
                            self.lignes[2][(i - 1) % len(self)],
                            self.lignes[2][i],
                            self.lignes[2][(i + 1) % len(self)],
                        ]
                    )
                ]
                if cellule == "-":
                    self.ajoute(False)
                elif cellule == "+":
                    self.ajoute(True)
                else:
                    self.ajoute(self.lignes[1][i])
            self.findeligne()


class BoiteAPetriAvecBords(BoiteAPetri):
    """Boîte à pétri avec bords.

    Les deux extrémités de la ligne ne se rejoignent pas :
    les cellules au bord des deux côtés obéissent à une règle spéciale.
    """

    def __init__(self, options):
        if options.largeur is None:
            largeur = LARGEUR
        else:
            largeur = options.largeur

        self.gauche, self.droite = options.bords

        options.initial = [
            [next(self.gauche)]
            + list(itertools.islice(options.initial[0], largeur - 2))
            + [next(self.droite)],
            [next(self.gauche)]
            + list(itertools.islice(options.initial[1], largeur - 2)),
        ]
        super().__init__(options)

    def findeligne(self):
        self.ajoute(next(self.droite))

        super().findeligne()

        self.ajoute(next(self.gauche))

    def __len__(self):
        return len(self.lignes[1])

    def acalculer(self):
        yield from range(1, len(self) - 1)


def main_liste():
    """Programme principal avec l'option `--liste`."""
    print("Liste des scénarios disponibles :", file=sys.stderr)
    print(" ".join(sorted(SCENARIOS.keys())))
    print(
        "Pour le détails des scénarios, consultez le code source (c'est sans doute frustrant, mais c'est plus simple comme ça).",  # pylint: disable=line-too-long
        file=sys.stderr,
    )


def main():
    """Fonction principale."""
    options = analyseur().parse_args()

    if options.liste:
        main_liste()
        sys.exit(0)

    if options.scenario is not None:
        for key in SCENARIOS[options.scenario]:
            if getattr(options, key) is None:
                setattr(options, key, SCENARIOS[options.scenario][key])
    for key in ("initial", "regles"):
        if getattr(options, key) is None:
            setattr(options, key, SCENARIOS["original"][key])

    if options.bords is None:
        boite = BoiteAPetri(options)
    else:
        boite = BoiteAPetriAvecBords(options)

    try:
        boite.mainloop()
    except KeyboardInterrupt:
        print()
        print(
            # pylint: disable=consider-using-f-string
            """Les règles utilisées étaient : "{}" """.format("".join(boite.regles)),
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
