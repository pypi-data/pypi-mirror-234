#!/usr/bin/env python3

# Copyright 2014-2020 Louis Paternault
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

"""Étude d'un couple de populations proies-prédateurs

En résolvant les équations de Lotka-Volterra avec la méthode d'Euler.
"""

# pylint: disable=invalid-name, missing-function-docstring

import turtle


def main():
    # Définition de trois tortues
    t_proie = turtle.Turtle()
    t_predateur = turtle.Turtle()
    t_phase = turtle.Turtle()

    # Populations
    n_proie = 50
    n_predateur = 20
    # Vitesses de variation des populations
    v_proie = 0
    v_predateur = 0
    # Constantes des équations de Lotka Volterra
    alpha = 3
    beta = 0.1
    gamma = 2
    delta = 0.1

    t = 0
    h = 0.001

    # Initialisation des tortues
    turtle.delay(1)  # pylint: disable=no-member
    t_proie.up()
    t_proie.goto(t - 200, 5 * n_proie - 200)
    t_proie.color("green")
    t_proie.down()
    t_predateur.up()
    t_predateur.goto(t - 200, 5 * n_predateur - 200)
    t_predateur.color("red")
    t_predateur.down()
    t_phase.up()
    t_phase.goto(2 * n_proie - 400, 2 * n_predateur)
    t_phase.down()

    while True:
        t += 0.05

        n_proie, n_predateur, v_proie, v_predateur = (
            n_proie + h * v_proie,
            n_predateur + h * v_predateur,
            n_proie * (alpha - beta * n_predateur),
            n_predateur * (delta * n_proie - gamma),
        )

        t_proie.goto(t - 200, 5 * n_proie - 200)
        t_predateur.goto(t - 200, 5 * n_predateur - 200)
        t_phase.goto(2 * n_proie - 400, 2 * n_predateur)


if __name__ == "__main__":
    main()
