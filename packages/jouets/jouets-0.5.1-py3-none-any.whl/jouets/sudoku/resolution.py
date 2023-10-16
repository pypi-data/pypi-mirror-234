# Copyright 2010-2014 Louis Paternault
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

"""Fonctions de resolution de sudokus.
"""

# pylint: disable=no-member

import multiprocessing


def solveur(candidats, fonction):
    """Essaye de résoudre l'ensemble des candidats.

    Boucle infinie qui prend des candidats dans la queue, tente de les
    resoudre, et applique la fonction quand ils sont resolu.
    """
    while True:
        grille = candidats.get()
        grille.remplit()
        if grille.resolu:
            fonction(grille)
        elif grille.impossible:
            pass
        else:
            (x, y) = grille.cherche_plus_proche()
            for valeur in grille.possible_case[x][y]:
                copie = grille.copy()
                copie.affecte((x, y), valeur)
                candidats.put(copie)
        candidats.task_done()


def resout(grille, fonction, nombre_processus):
    """Résout le sudoku, avec plusieurs threads.

    :arg func fonction: Fonction appellee sur les solutions trouvées.
    """
    candidats = multiprocessing.JoinableQueue()
    candidats.put(grille)

    # Préparation et lancement des travailleurs
    processus = [
        multiprocessing.Process(
            target=solveur,
            kwargs={"candidats": candidats, "fonction": fonction},
            daemon=True,
        )
        for __numero in range(nombre_processus)
    ]
    for process in processus:
        process.start()

    # On attent que le travail soit fait
    candidats.join()

    # Et on détruit les travailleurs.
    for process in processus:
        process.terminate()
