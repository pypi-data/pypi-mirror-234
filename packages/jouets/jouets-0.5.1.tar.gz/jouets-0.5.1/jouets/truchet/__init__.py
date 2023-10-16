# Copyright 2023 Louis Paternault
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

"""Génère des tuiles de Truchet généralisées."""

# pylint: disable=consider-using-f-string

import functools
import itertools
import math
import random

import jinja2

from ..utils.erreurs import ErreurUtilisateur

VERSION = "0.1.0"


@functools.cache
def tuiles(n):
    """Renvoit la liste de toutes les tuiles de Truchet possibles.

    :param int n: Nombre d'arêtes de la tuile.

    Chaque tuile est au format `[1, -1, 3, 1, -1, -3]`, qui signifie:
    - la première arête avance d'un sommet ;
    - la seconde arête recule d'un sommet (c'est en fait la même que la précédente) ;
    - la troisième arête avance de trois sommets ;
    - etc.
    """
    if n == 0:
        return [[]]
    return [
        [i] + x + [-i] + y
        for i in range(1, 2 * n, 2)
        for x, y in itertools.product(
            tuiles((i - 1) // 2),
            tuiles((2 * n - i - 1) // 2),
        )
    ]


class Tuiles:
    """Ensemble de tuiles.

    :param int arêtes: Nombre d'arêtes des tuiles.
    :param str mode: Mode de génération des tuiles : `"random"`, `"liste"`, ou `"tri"`.
    :param int nombre: Nombre de tuiles du sac.

    À l'initialisation, un sac de `nombre` tuiles est pioché parmi toutes les tuiles disponibles.
    Si `nombre` est plus grand que le nombre de tuiles disponibles, il y aura des répétitions ;
    sinon, chaque tuile est unique.
    Cas particuliers :
    - en mode `liste`, si `nombre` est nul :
      le sac contient exactement une fois chaque tuile disponible.
    - en mode `random`, si `nombre` est nul :
      il n'y a pas de sac, chaque tuile est totalement aléatoire.

    Puis, à chaque appel de `Tuiles.next()`, une tuile est piochée dans le sac et renvoyée.
    Quand le sac est vide, il est re-rempli aux valeurs initiales.

    Les tuiles sont renvoyées selon le mode :
    - `random` : les tuiles sont piochées au hasard dans le sac ;
    - `liste` : les tuiles sont mélangées une seule fois, puis prises toujours dans le même ordre.
    - `tri` : les tuiles sont prises toujours dans le même ordre, trié.
    """

    def __init__(self, arêtes, mode, nombre):
        disponibles = tuiles(arêtes)
        if mode == "random" and nombre == 0:
            self._mode = "random0"
        else:
            self._mode = mode
        if nombre == 0:
            nombre = len(disponibles)
        # Si le nombre demandé est supérieur au nombre de tuiles disponibles,
        # on pioche dans plusieurs sacs.
        if self._mode == "tri":
            self._disponibles = list(sorted(disponibles))
        else:
            self._disponibles = random.sample(
                disponibles * math.ceil(nombre / len(disponibles)), nombre
            )
        self._sac = []

    def next(self):
        """Renvoit une nouvelle tuile. Cette méthode peut être appelée une infinité de fois."""
        if self._mode == "random0":
            return random.choice(self._disponibles)
        if not self._sac:
            # Remplit le sac
            if self._mode == "random":
                self._sac = random.sample(self._disponibles, len(self._disponibles))
            elif self._mode in ("liste", "tri"):
                self._sac = self._disponibles.copy()
        return self._sac.pop()

    def __len__(self):
        return len(self._disponibles)


################################################################################
# Fonctions gérérant du code LaTeX


def vérifie(booléen, message=None):
    """Léve une exception si la condition est fausse.

    À utiliser dans un template.
    """
    if not booléen:
        raise ErreurUtilisateur(message)
    return ""


def calcule_dureté(dureté, saut, arêtes):
    """Calcule la dureté effective

    En fonction de la dureté donnée en argumennt et de la taille de l'arête.

    Cette fonction pourrait être *grandement* améliorée en tenant compte de la
    distance entre les deux extrémités, et de l'angle relatif de leur tangente.
    Mais j'ai déjà passé assez de temps sur ce programme.
    """
    if saut > arêtes:
        saut -= 2 * arêtes
    elif saut < -arêtes:
        saut += 2 * arêtes
    return 0.5 * dureté * math.log(abs(saut) + 1)


def _rayon(n):
    """Renvoit le rayon du cercle circonscrit à un polygone à `n` côtés de côté 1."""
    if n % 2:  # Nombre de côtés impairs
        return 1 / (math.cos(math.pi / n) + 1)
    # Nombre de côtés pairs
    return 0.5 / math.cos(math.pi / n)


@jinja2.pass_environment
def polygone(env, côtés, graphe, *, durete, pairimpair=None):
    """Génère le code TikZ pour tracer une tuile de Truchet dans un polygone régulier.

    :param int côtés: Nombre de côtés du polygone.
    :param list graphe: La tuile à tracer.
    :param float durete: La dureté du tracé.
    :param bool pairimpair: Indique le style d'un des coins du polygones.
    """
    if pairimpair is None:
        pairimpair = random.choice((True, False))
    latex = ""

    # Clip
    latex += env.templates["clip"].render(côtés=côtés, rayon=_rayon)

    # Remplissages
    for reste in range(2):
        à_faire = list(i for i in range(len(graphe)) if i % 2 == reste)
        sommet = 0
        arcs = []
        while True:
            if sommet in à_faire:
                à_faire.remove(sommet)
            else:
                if reste ^ pairimpair:
                    style = "pair"
                else:
                    style = "impair"
                latex += rf"\path[{style}]" + " -- ".join(arcs) + " -- cycle;\n"
                try:
                    sommet = à_faire.pop(0)
                    arcs = []
                except IndexError:
                    break
            arcs.append(
                env.templates["arc"].render(
                    durete=durete,
                    sommets=len(graphe),
                    côtés=côtés,
                    sommet=sommet,
                    saut=graphe[sommet],
                )
            )
            sommet = (sommet + graphe[sommet] + 1) % len(graphe)
            if sommet % (len(graphe) // côtés) == 0:
                # pylint: disable=line-too-long
                arcs.append(
                    f"({360//côtés*(sommet // (len(graphe)//côtés)) + 360/(2*côtés)}:{ _rayon(côtés) })"
                )

    # Arêtes
    latex += env.templates["arête"].render(
        graphe=graphe,
        sommets=len(graphe),
        durete=durete,
        côtés=côtés,
    )

    # Cadre
    latex += env.templates["bord"].render(côtés=côtés, rayon=_rayon)

    return latex


def coordonnées_sommet(côtés, i, sommets):
    """Renvoit les coordonnées du sommet.

    :param int côtés: Nombre de côtés du polygone.
    :param int i: Indice du sommet en cours.
    :param int sommets: Nombre total de sommets.
    """
    # Longueur d'un côté
    if côtés % 2:  # Nombre impair de côtés
        longueur = 2 * math.sin(math.pi / côtés) / (1 + math.cos(math.pi / côtés))
    else:
        longueur = math.tan(math.pi / côtés)
    return "(${} + {}$)".format(
        "({}:{})".format(
            360 // côtés * (i // (sommets // côtés)) + 360 / (2 * côtés),
            _rayon(côtés),
        ),
        "({}:{})".format(
            360 // côtés * (i // (sommets // côtés)) + 360 / côtés + 90,
            longueur * (i % (sommets // côtés) + 1) / (sommets // côtés + 1),
        ),
    )


def tangente(côtés, i, sommets):
    """Renvoit l'angle de la tangente.

    :param int côtés: Nombre de côtés du polygone.
    :param int i: Indice du sommet en cours.
    :param int sommets: Nombre total de sommets.
    """
    return 360 // côtés * (1 + (i // (sommets // côtés)))


@jinja2.pass_environment
def cercle(env, graphe, *, durete):
    """Génère le code TikZ pour tracer une tuile de Truchet dans un cercle.

    :param list graphe: La tuile à tracer.
    :param float durete: La dureté du tracé.
    """
    # pylint: disable=line-too-long
    return env.templates["cercle"].render(
        graphe=graphe,
        n=len(graphe) // 2,
        durete=durete,
    )


def environment():
    """Construit et renvoit l'environnement Jinja2."""
    env = jinja2.Environment(
        loader=jinja2.ChoiceLoader(
            [
                jinja2.FileSystemLoader("."),
                jinja2.PackageLoader("jouets.truchet"),
            ]
        ),
    )
    env.globals["random"] = random
    env.globals["len"] = len
    env.globals["polygone"] = polygone
    env.globals["cercle"] = cercle
    env.globals["_sommet"] = coordonnées_sommet
    env.globals["_tangente"] = tangente
    env.globals["_durete"] = calcule_dureté
    env.globals["vérifie"] = vérifie

    # Pré-compilation des templates pour gagner *beaucoup* de temps
    # pylint: disable=line-too-long
    env.templates = {}
    env.templates["arc"] = env.from_string(
        r"""
            {{ _sommet(côtés, sommet, sommets) }}
            .. controls
            +({{ _tangente(côtés, sommet, sommets) }}:-{{ _durete(durete, saut, sommets//2) }})
            and
            +({{ _tangente(côtés, sommet + saut, sommets) }}:-{{ _durete(durete, saut, sommets//2) }})
            ..
            {{ _sommet(côtés, sommet + saut, sommets) }}"""
    )
    env.templates["arête"] = env.from_string(
        r"""
    {% for saut in graphe %}
    {%- if saut > 0 %}
    \path[aretes]
        {{ _sommet(côtés, loop.index0, sommets) }}
        .. controls
        +({{ _tangente(côtés, loop.index0, sommets) }}:-{{ _durete(durete, saut, sommets//2) }})
        and
        +({{ _tangente(côtés, loop.index0 + saut, sommets) }}:-{{ _durete(durete, saut, sommets//2) }})
        ..
        {{ _sommet(côtés, loop.index0 + saut, sommets) }};
    {%- endif -%}
    {% endfor %}
    """
    )
    env.templates["clip"] = env.from_string(
        r"""
    \clip
        {%- for i in range(côtés) -%}
        ({{360//côtés*i + 360/(2*côtés)}}:{{ rayon(côtés) }}) --
        {%- endfor -%}
        cycle;
    """
    )
    env.templates["bord"] = env.from_string(
        r"""
    \path[bord]
        {%- for i in range(côtés) -%}
        ({{360//côtés*i + 360/(2*côtés)}}:{{ rayon(côtés) }}) --
        {%- endfor -%}
        cycle;
    """
    )
    env.templates["cercle"] = env.from_string(
        r"""\
    \clip (0, 0) circle (1);
    \draw[bord] (0, 0) circle (1);
    {% for saut in graphe %}
        {% if saut > 0 %}
            \path[aretes]
                ({180*{{loop.index}}/{{n}} }:1) % Point de départ
                .. controls
                +({180*{{loop.index}}/{{n}} }:{-{{_durete(durete, saut, n)}} }) % Tangente de départ
                and
                +({180*{{loop.index + saut}}/{{n}} }:{-{{_durete(durete, saut, n)}} }) % Tangente d'arrivée
                ..
                ({180*{{loop.index + saut}}/{{n}} }:1) % Point d'arrivée
                ;
        {% endif %}
    {% endfor %}
    """
    )

    return env
