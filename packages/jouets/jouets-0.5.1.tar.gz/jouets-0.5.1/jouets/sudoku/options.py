# Copyright 2012-2023 Louis Paternault
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

"""Analyse de la ligne de commande."""

import argparse
import multiprocessing
import os
import sys
import textwrap
import time

from ..utils import erreurs
from ..utils.aargparse import analyseur as analyseur_base
from .version import VERSION


def analyseur():
    """Renvoit un analyseur de ligne de commandes."""
    parser = analyseur_base(VERSION, prog="sudoku", description="Un solveur de Sudoku")
    parser.add_argument(
        "fichier",
        nargs="?",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help=textwrap.dedent(
            """\
            File containing the starting array. If absent, array is read from
            standard input.
            """
        ),
    )
    parser.add_argument(
        "-f",
        "--format",
        action="store",
        dest="format_fichier",
        type=str,
        choices=["short", "long"],
        default="long",
        help=textwrap.dedent(
            """\
            Input file format: "short" (...232....4....1) or long (lines of ". . . 2 3").
            """
        ),
    )
    parser.add_argument(
        "-j",
        "--jobs",
        action="store",
        dest="processus",
        type=int,
        default=os.cpu_count(),
        help="Number of jobs to run simultaneously. Default is the number of cpu cores.",
    )
    parser.add_argument(
        "-a",
        "--actions",
        action="store",
        dest="actions",
        type=str,
        default="p",
        help=textwrap.dedent(
            """\
            Action to perform on solved arrays. This argument is a combination
            of letters 'p' (print solution), 'c' (count solutions), and 't'
            (time solutions).
            """
        ),
    )
    return parser


def analyse(ligne_de_commande):
    """Analyse la ligne de commande, et renvoie un namedtuple:

    - traitement : liste de ce qui doit etre effectue sur les solutions (objet
      de type Action).
    - format_fichier : "short" ou "long"
    - fichier : fichier (deja ouvert) dans lequel lire la grille (entree
      standart autorisee).
    - processus : nombre de processus concurrents a utiliser.
    """
    options = analyseur().parse_args(ligne_de_commande)

    options.traitement = Action()
    for char in options.actions:
        if char == "c":
            options.traitement.compte(True)
        elif char == "t":
            options.traitement.chronometre(True)
        elif char == "p":
            options.traitement.affiche(True)
        else:
            raise erreurs.ErreurUtilisateur(
                f"Letter {char} not recognized as an argument to --actions."
            )
    del options.actions

    return options


class Action:
    """Gestion des actions a effectuer avant, pendant et apres la resolution."""

    # Ensemble des fonctions a executer avant la resolution. Ces fonctions ne
    # prennent pas d'argemnt.
    __actions_initiales = set()
    # Ensemble des fonctions a executer pour chaque grille resolue. Ces
    # fonctions prennent un argement : la grille en question.
    __actions_courantes = set()
    # Ensemble des fonctions a executer apres la resolution. Ces fonctions ne
    # prennent pas d'argemnt.
    __actions_finales = set()

    # Heure de depart
    __chronometre_depart = 0

    def __init__(self):
        # pylint: disable=no-member

        # Lock pour que deux processus n'affichent pas le resultat en meme
        # temps.
        self.__affiche_lock = multiprocessing.Lock()

        # Nombre de grilles resolues
        self.__compte_valeur = multiprocessing.Value("i", 0)

    @staticmethod
    def __definit(ensemble, fonction, oui):
        """Ajoute ou enleve une fonction d'un ensemble

        :arg set ensemble: Ensemble à manipuler
        :arg func  fonction: Fonction à manipuler
        :arg bool oui: Si `True`, ajoute la fonction; sinon, l'enlève.
        """
        if oui:
            ensemble.add(fonction)
        else:
            ensemble.discard(fonction)

    def execute_initial(self):
        """Execute l'ensemble des fonctions initiales"""
        for fonction in self.__actions_initiales:
            fonction()

    def execute_courant(self, argument):
        """Execute l'ensemble des fonctions a lancer pour chaque grille trouvee"""
        for fonction in self.__actions_courantes:
            fonction(argument)

    def execute_final(self):
        """Execute l'ensemble des fonctions finales"""
        for fonction in self.__actions_finales:
            fonction()

    # Compte
    def compte(self, oui):
        """Definit s'il faut compter le nombre de solutions trouvees."""
        self.__definit(self.__actions_courantes, self.__compte_incremente, oui)
        self.__definit(self.__actions_finales, self.__compte_affiche, oui)

    def __compte_incremente(self, __ignore__):
        """Augmente le nombre de grilles trouvees"""
        with self.__compte_valeur.get_lock():
            self.__compte_valeur.value += 1

    def __compte_affiche(self):
        """Affiche le nombre de grilles trouvees"""
        print(f"{self.__compte_valeur.value} solutions\n")

    # Affiche
    def affiche(self, oui):
        """Definit si oui ou non il faut afficher les grilles trouvees"""
        self.__definit(self.__actions_courantes, self.__affiche, oui)

    def __affiche(self, argument):
        """Affiche la grille"""
        with self.__affiche_lock:
            print(argument.pretty_print())

    # Chronometre
    def chronometre(self, oui):
        """Definit si oui ou non il faut chronometrer le temps de resolution"""
        self.__definit(self.__actions_initiales, self.__chronometre_debut, oui)
        self.__definit(self.__actions_finales, self.__chronometre_fin, oui)

    def __chronometre_debut(self):
        """Enregistre l'heure de depart"""
        self.__chronometre_depart = time.perf_counter()

    def __chronometre_fin(self):
        """Affiche le temps mis."""
        # pylint: disable=consider-using-f-string
        print(
            "{:.2f} secondes".format(
                float(time.perf_counter() - self.__chronometre_depart)
            )
        )
