# Copyright 2018 Louis Paternault
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

"""Résolution de l'énigme : UN+UN+DEUX+CINQ=NEUF"""

# pylint: disable=invalid-name, too-many-nested-blocks, too-many-boolean-expressions, too-many-branches

import itertools
import multiprocessing

VERSION = "0.1.0"


def addition1():
    """Force brute, naïve."""
    for C in range(10):
        for D in range(10):
            for E in range(10):
                for F in range(10):
                    for I in range(10):
                        for N in range(10):
                            for Q in range(10):
                                for U in range(10):
                                    for X in range(10):
                                        if (
                                            C != D
                                            and C != E
                                            and C != F
                                            and C != I
                                            and C != N
                                            and C != Q
                                            and C != U
                                            and C != X
                                            and D != E
                                            and D != F
                                            and D != I
                                            and D != N
                                            and D != Q
                                            and D != U
                                            and D != X
                                            and E != F
                                            and E != I
                                            and E != N
                                            and E != Q
                                            and E != U
                                            and E != X
                                            and F != I
                                            and F != N
                                            and F != Q
                                            and F != U
                                            and F != X
                                            and I != N
                                            and I != Q
                                            and I != U
                                            and I != X
                                            and N != Q
                                            and N != U
                                            and N != X
                                            and Q != U
                                            and Q != X
                                            and U != X
                                        ):
                                            if (10 * U + N) + (10 * U + N) + (
                                                1000 * C + 100 * I + 10 * N + Q
                                            ) + (
                                                1000 * D + 100 * E + 10 * U + X
                                            ) == 1000 * N + 100 * E + 10 * U + F:
                                                yield (C, D, E, F, I, N, Q, U, X)


def addition2():
    """Manière un peu plus élégante de s'assurer que les lettres sont toutes différentes."""
    for C in range(10):
        for D in range(10):
            for E in range(10):
                for F in range(10):
                    for I in range(10):
                        for N in range(10):
                            for Q in range(10):
                                for U in range(10):
                                    for X in range(10):
                                        if len(set((C, D, E, F, I, N, Q, U, X))) == 9:
                                            if (10 * U + N) + (10 * U + N) + (
                                                1000 * C + 100 * I + 10 * N + Q
                                            ) + (
                                                1000 * D + 100 * E + 10 * U + X
                                            ) == 1000 * N + 100 * E + 10 * U + F:
                                                yield (C, D, E, F, I, N, Q, U, X)


def addition3():
    """N'énumère que les cas où les valeurs des lettres sont toutes différentes."""
    for C in range(10):
        for D in range(10):
            if D == C:
                continue
            for E in range(10):
                if E in (C, D):
                    continue
                for F in range(10):
                    if F in (C, D, E):
                        continue
                    for I in range(10):
                        if I in (C, D, E, F):
                            continue
                        for N in range(10):
                            if N in (C, D, E, F, I):
                                continue
                            for Q in range(10):
                                if Q in (C, D, E, F, I, N):
                                    continue
                                for U in range(10):
                                    if U in (C, D, E, F, I, N, Q):
                                        continue
                                    for X in range(10):
                                        if X in (C, D, E, F, I, N, Q, U):
                                            continue
                                        if (10 * U + N) + (10 * U + N) + (
                                            1000 * C + 100 * I + 10 * N + Q
                                        ) + (
                                            1000 * D + 100 * E + 10 * U + X
                                        ) == 1000 * N + 100 * E + 10 * U + F:
                                            yield (C, D, E, F, I, N, Q, U, X)


def addition4():
    """Utilisation de `itertools.permutations`."""
    for C, D, E, F, I, N, Q, U, X in itertools.permutations(range(10), 9):
        if (10 * U + N) + (10 * U + N) + (1000 * C + 100 * I + 10 * N + Q) + (
            1000 * D + 100 * E + 10 * U + X
        ) == 1000 * N + 100 * E + 10 * U + F:
            yield (C, D, E, F, I, N, Q, U, X)


def addition5():
    """Réduction du nombre de multiplications."""
    for C, D, E, F, I, N, Q, U, X in itertools.permutations(range(10), 9):
        if 1000 * (C + D - N) + 100 * I + 10 * (2 * U + N) + (2 * N + Q + X - F) == 0:
            yield (C, D, E, F, I, N, Q, U, X)


def _sousfonction6(C):
    solutions = set()
    for D, E, F, I, N, Q, U, X in itertools.permutations(
        itertools.chain(range(0, C), range(C + 1, 10)), 8
    ):
        if 1000 * (C + D - N) + 100 * I + 10 * (2 * U + N) + (2 * N + Q + X - F) == 0:
            solutions.add((C, D, E, F, I, N, Q, U, X))
    return solutions


def addition6():
    """Parallélisation."""
    with multiprocessing.Pool() as pool:
        yield from itertools.chain(*pool.imap_unordered(_sousfonction6, range(10)))
