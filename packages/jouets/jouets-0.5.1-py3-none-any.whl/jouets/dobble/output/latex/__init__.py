# Copyright 2014-2023 Louis Paternault
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

"""Format de sortie lualatex."""

import colorsys
import os
import random

import jinja2
import pkg_resources

from .. import DobbleOutput

SYMBOLES = [
    r"\Circle",
    r"\Square",
    r"\UParrow",
    r"\twonotes",
    r"$\spadesuit$",
    r"$\clubsuit$",
    r"\leftmoon",
    r"\ding{212}",  # Flèche
    r"\ding{34}",  # Ciseaux
    r"\ding{170}",  # Cœur
    r"\scalebox{.7}{\smallpencil}",
    r"\scalebox{.8}{\leftthumbsup}",
    r"\scalebox{.6}{\anchor}",
    r"\scalebox{.7}{\eye}",
    r"\scalebox{.8}{\PHram}",
    r"\scalebox{.6}{\PHtunny}",
    r"\phone",
    r"\bell",
    r"\clock",
    r"\smiley",
    r"\mancube",
    r"\scalebox{.6}{\Bicycle}",
    r"\Coffeecup",
    r"\Football",
    r"\Industry",
    r"\Wheelchair",
    r"\CircledA",
    r"\Letter",
    r"\scalebox{.7}{\Bat}",
    r"\Bouquet",
    r"\Mundus",
    r"\Yinyang",
    r"\Lightning",
    r"\Radioactivity",
    r"\Stopsign",
    r"\bomb",
    r"\danger",
    r"\noway",
    r"\textxswup",
    r"\epsdice{5}",
    r"\dsagricultural",
    r"\dsheraldical",
    r"\dsjuridical",
    r"\dsliterary",
    r"\dsrailways",
    r"\dstechnical",
    r"\scalebox{.3}{\recycle}",
    r"\Info",
    r"\Gentsroom",
    r"\Ladiesroom",
    r"\MineSign",
    r"\sun",
    r"\scalebox{.5}{\gluon}",
    r"\ding{73}",  # Étoile
    r"\ding{56}",  # Croix
    r"\ding{100}",  # Flocon de neige
    r"\ding{95}",  # Fleur
    r"\dsmathematical",  # Compas
    r"?",
    r"!",
    r"\#",
    r"+",
    r"\%",
    r"A",
    r"B",
    r"C",
    r"D",
    r"E",
    r"F",
    r"G",
    r"H",
    r"I",
    r"J",
    r"K",
    r"L",
    r"M",
    r"N",
    r"O",
    r"P",
    r"Q",
    r"R",
    r"S",
    r"T",
    r"U",
    r"V",
    r"W",
    r"X",
    r"Y",
    r"Z",
]


def symboles(nombre):
    """Renvoie une permutation aléatoire de `nombre`  symboles.

    Cette liste est complétée par des nombres si la liste prédéfinie de
    symboles n'est pas suffisante.
    """
    symboles_tex = SYMBOLES[:nombre]
    if len(symboles_tex) < nombre:
        symboles_tex.extend(list(range(nombre - len(symboles_tex))))
    random.shuffle(symboles_tex)
    return symboles_tex


def randomcolor(seed=None):
    """Renvoit une couleur aléatoire."""

    # On sauvegarde la graine précédente pour que l'aléatoire reste aléatoire.
    graine_precedente = random.random()

    if seed is None:
        return "0,0,0"

    random.seed(seed)
    hsv = (random.random(), 1, 1)

    random.seed(graine_precedente)

    return ",".join([str(int(255 * num)) for num in colorsys.hsv_to_rgb(*hsv)])


class TexOutput(DobbleOutput):
    """Code lualatex"""

    # pylint: disable=too-few-public-methods

    keyword = "tex"

    def genere(self, jeu, groupe=False):
        # pylint: disable=maybe-no-member

        if groupe:
            jeux = {}
            for carte in jeu:
                if carte.groupe not in jeux:
                    jeux[carte.groupe] = []
                jeux[carte.groupe].append(carte)
        else:
            jeux = {None: jeu.cartes}

        nom = "output.tex"
        return (
            jinja2.Environment(
                loader=jinja2.FileSystemLoader(
                    os.path.dirname(
                        pkg_resources.resource_filename(
                            "jouets.dobble.output.latex",
                            os.path.join("data", "templates", nom),
                        )
                    )
                )
            )
            .get_template(nom)
            .render(
                {
                    "jeux": jeux,
                    "symboles": symboles(len(jeu.symboles)),
                    "randint": random.randint,
                    "randomcolor": randomcolor,
                }
            )
        )
