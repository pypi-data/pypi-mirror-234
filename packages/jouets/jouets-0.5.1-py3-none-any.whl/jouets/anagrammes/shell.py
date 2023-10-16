# Copyright 2018-2023 Louis Paternault
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

"""Interpréteur de commandes pour rechercher des anagrammes.

Permet de ne charger le dictionnaire qu'une seule fois, et faire plusieurs recherches dedans.
"""

import argparse
import inspect
import logging
import math
import shlex
import subprocess
import textwrap

try:
    import readline  # pylint: disable=unused-import
except ImportError:
    # Apparement, Python peut être compilé sans readline
    pass

from ..utils import smartopen

# pylint: disable=relative-beyond-top-level
# Voir https://github.com/PyCQA/pylint/issues/1667
from ..utils.aargparse import type_intervalle, yesno
from . import DictionnaireArborescent, Intervalle


class Shell:
    """Interpréteur de commandes pour rechercher des anagrammes."""

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.dico = DictionnaireArborescent()
        self.options = {
            "mots": Intervalle(None, None),
            "lettres": Intervalle(None, None),
            "accents": True,
        }

    def loop(self):
        """Boucle princiale du shell.

        Lit un commande de l'utilisateur, l'exécute, et recommence.
        """
        print("Recherche d'anagrammes : shell.")
        print("Tapez `help` pour afficher l'aide.")

        while True:
            # Lecture d'une ligne
            try:
                line = input("> ")
            except EOFError:
                logging.info("Terminé…")
                break

            # Décomposition en commande et arguments
            try:
                commande, *arguments = shlex.split(line.strip())
            except ValueError:
                continue

            # Cas particulier: exit
            if commande == "exit":
                logging.info("Terminé…")
                break

            # Appel de la méthode correspondant à la commande, si elle existe.
            if self.valide(commande, arguments):
                self.methode(commande)(*arguments)

    @staticmethod
    def methodname(commande):
        """Renvoit le nom de la méthode correspondant à la commande du shell."""
        return f"command_{commande}"

    def methode(self, commande):
        """Renvoit la méthode correspondant à la commande du shell."""
        return getattr(self, self.methodname(commande))

    def valide(self, name, arguments=None):
        """Renvoit si oui ou le nom (donné par l'utilisateur) est une commande valide.

        Si `arguments` n'est pas `None`,
        vérifie aussi s'ils sont corrects (si le nombre est correct actuellement).
        """
        if not hasattr(self, self.methodname(name)):
            logging.error("La commande '%s' n'existe pas.", name)
            return False
        if not inspect.ismethod(self.methode(name)):
            logging.error("La commande '%s' n'existe pas.", name)
            return False
        if arguments is None:
            return True
        parametres = inspect.signature(self.methode(name)).parameters
        if not parametres:
            maxparam = 0
        elif list(parametres.values())[-1].kind == inspect.Parameter.VAR_POSITIONAL:
            maxparam = math.inf
        else:
            maxparam = len(parametres.values())
        minparam = len(
            [
                param
                for param in parametres.values()
                if param.default == inspect.Parameter.empty
                and param.kind != inspect.Parameter.VAR_POSITIONAL
            ]
        )
        if not minparam <= len(arguments) <= maxparam:
            if minparam == maxparam:
                logging.error("Le nombre d'arguments doit être égal à %s.", minparam)
            elif maxparam == math.inf:
                logging.error(
                    "Le nombre d'arguments doit être supérieur ou égal à %s.", minparam
                )
            else:
                logging.error(
                    "Le nombre d'arguments doit être compris entre %s et %s.",
                    minparam,
                    maxparam,
                )
            logging.error("Utilisez `help %s` pour plus d'informations.", name)
            return False
        return True

    @staticmethod
    def oneline_help(methode):
        """Renvoit l'aide d'une méthode, en une ligne."""
        params = []
        for param in inspect.signature(methode).parameters.values():
            if param.default == inspect.Parameter.empty:
                params.append(param.name)
            else:
                params.append(f"[{param.name}]")
        # pylint: disable=consider-using-f-string
        return "{} {} : {}".format(
            methode.__name__[len("command_") :],
            " ".join(params),
            methode.__doc__.split("\n")[0],
        )

    def command_help(self, commande=None):
        """Affiche l'aide ; `help help` pour plus d'informations.

        - help: Affiche la liste des commandes disponibles.
        - help commande: Affiche l'aide détaillée de la commande.
        """
        if commande is None:
            for attr in sorted(dir(self)):
                methode = getattr(self, attr)
                if attr.startswith("command_") and inspect.ismethod(methode):
                    print(self.oneline_help(methode))
        else:
            if self.valide(commande):
                print(self.oneline_help(self.methode(commande)))
                print()
                print(
                    textwrap.dedent(
                        "\n".join(self.methode(commande).__doc__.split("\n")[2:])
                    )
                )

    def command_load(self, fichier):
        """Charge un dictionnaire.

        Le dictionnaire est soit un fichier texte,
        soit un dictionnaire aspell,
        sous la forme `aspell://fr` pour le français par exemple.
        """
        self.dico.charge(fichier, accents=self.options["accents"])

    def command_dump(self):
        """Affiche la liste des mots du dictionnaire.

        Au démarrage du shell, le dictionnaire est vide.
        Il faut le remplir en utilisant la commande `load`.
        """
        for mot in self.dico.itere_mots():
            print(mot)

    def command_exit(self):
        """Quitte le programme."""

    def command_option(self, nom=None, valeur=None):
        """Affiche ou définit une option.

        Les options sont :
        - `mots` et `lettres` : Nombre et longueur des mots des anagrammes recherchées,
           sous la forme d'un intervalle
           (par exemple `2:7` pour « entre 2 et 7 »,
           ou `:7` pour « inférieur à 7 »).
        - `accents` (définit si les accents sont ignorés ou non).

        Usage :
        - `option` : Affiche les valeurs des options.
        - `option mots` : Affiche la valeur de l'option `mots`.
        - `option mots 2:8` : Définit une option.
        """
        if nom is None:
            for key, value in self.options.items():
                print(f"{key} = {value}")
        elif valeur is None:
            if nom in self.options:
                print(f"{nom} = {self.options[nom]}")
            else:
                logging.error("Option '%s' inconnue.", nom)
        else:
            if nom == "accents":
                self.options["accents"] = yesno(valeur)
            elif nom in ["mots", "lettres"]:
                try:
                    self.options[nom] = Intervalle(*type_intervalle(valeur))
                except argparse.ArgumentTypeError:
                    logging.error("Valeur '%s' invalide.", valeur)
            else:
                logging.error("Option '%s' inconnue.", nom)

    def command_clean(self):
        """Efface le dictionnaire."""
        self.dico.clean()

    def command_tree(self, fichier=None):
        """Génère le code Graphviz du dictionnaire arborescent.

        Et l'enregistre éventuellement dans le fichier donné en argument.
        """
        with smartopen(fichier) as filehandle:
            filehandle.write(self.dico.dot())

    @staticmethod
    def command_ls(*chemin):
        """Affiche le contenu d'un répertoire."""
        subprocess.run(["ls"] + list(chemin), check=False)

    def command_search(self, *mots):
        """Recherche des anagrammes."""
        self.command_save(None, *mots)

    def command_save(self, fichier, *mots):
        """Recherche des anagrammes, et les enregistre dans un fichier."""
        if not mots:
            logging.error("Veuillez fournir au moins un mot…")
            return
        with smartopen(fichier) as filehandle:
            for anagramme in self.dico.anagrammes(mots, self.options):
                filehandle.write(" ".join(anagramme))
                filehandle.write("\n")


def main(_=None):
    """Lance un interpréteur de commande pour la recherche d'anagrammes.

    Les arguments de la ligne de commande sont ignorés.
    """
    Shell().loop()


if __name__ == "__main__":
    main()
