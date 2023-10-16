#!/usr/bin/env python3

# Copyright 2018-2021 Louis Paternault
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

"""Résolution de l'énigme : UN+UN+DEUX+CINQ=NEUF --- Interface en ligne de commandes."""

# pylint: disable=invalid-name, too-many-arguments

import sys
import timeit

from . import addition1, addition2, addition3, addition4, addition5, addition6

# Nombre d'appels à chaque fonction
RECHERCHES = 1

# Affichage des solutions
AFFICHAGE = """
+   {U}{N}
+   {U}{N}
+ {D}{E}{U}{X}
+ {C}{I}{N}{Q}
------
= {N}{E}{U}{F}
"""


def _affiche_solution(C, D, E, F, I, N, Q, U, X):
    print(AFFICHAGE.format(C=C, D=D, E=E, F=F, I=I, N=N, Q=Q, U=U, X=X))


def chronometre(fonction):
    """Chronomètre et affiche le temps d'exécution de la fonction donnée en argument."""
    print(f"{fonction.__name__} : ", end="")
    sys.stdout.flush()
    print(
        # pylint: disable=consider-using-f-string
        "{0:.1f} secondes.".format(
            timeit.timeit(
                f"list({fonction.__name__}())",
                globals=globals(),
                number=RECHERCHES,
            )
        )
    )


def main():
    """Fonction principale."""
    print("Affichage des solutions")
    for solution in addition6():
        _affiche_solution(*solution)

    print(f"Exécution de {RECHERCHES} recherches.")
    for fonction in (addition1, addition2, addition3, addition4, addition5, addition6):
        chronometre(fonction)


if __name__ == "__main__":
    main()
