# Copyright 2020 Louis Paternault
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

"""Convertit (à l'arrache) un graphe au format .dot en une matrice"""

import collections

import pydot

FICHIER = "graphe-probabiliste.dot"


def aretes():
    graphe = pydot.graph_from_dot_file(FICHIER)[0]
    for arete in graphe.get_edge_list():
        yield (arete.get_source(), arete.get_destination(), arete.get_label())


def main():
    matrice = collections.defaultdict(dict)
    for a, b, poids in aretes():
        matrice[a][b] = poids.strip('"')
    indices = "".join(matrice.keys())

    print("[")
    for i in range(len(indices)):
        print("  [", end="")
        for j in range(len(indices)):
            print(
                "  {},".format(matrice.get(indices[i], {}).get(indices[j], "0")), end=""
            )
        print("  ],\n", end="")
    print("]")


if __name__ == "__main__":
    main()
