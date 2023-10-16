# Copyright 2014-2021 Louis Paternault
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

"""Recherche d'anagrammes : classes principales."""

import collections
import copy
import logging
import math
import re
import subprocess
import textwrap

from unidecode import unidecode

VERSION = "0.1.0"


class Alphabet:
    """Ensemble de lettres avec répétition.

    Cet ensemble est stocké dans l'attribut :attr:`Alphabet._elements`,
    qui est un dictionnaire dont les clefs sont les lettres,
    et les valeurs sont le nombre d'occurence de ces lettres.
    Les lettres qui ont une occurence nulle sont considérées comme absentes,
    et ignorées dans la plupart des méthodes.

    >>> alpha = Alphabet("aabc")
    >>> alpha -= "ab"
    >>> alpha
    Alphabet("ac")
    >>> ("a" in alpha, "b" in alpha, "c" in alpha)
    (True, False, True)
    >>> alpha += "ad"
    >>> alpha
    Alphabet("aacd")
    >>> (alpha["a"], alpha["d"], alpha["X"])
    (2, 1, 0)
    """

    def __init__(self, initial=None):
        if isinstance(initial, dict):
            self._elements = collections.defaultdict(int, initial)
        elif isinstance(initial, collections.abc.Iterable):
            self._elements = collections.defaultdict(int)
            for i in initial:
                self._elements[i] += 1
        else:
            self._elements = collections.defaultdict(int)

    def __contains__(self, value):
        return self._elements.get(value, 0) != 0

    def __sub__(self, other):
        newelements = copy.copy(self._elements)
        for char in other:
            newelements[char] -= 1
        return self.__class__(newelements)

    def __add__(self, other):
        newelements = copy.copy(self._elements)
        for char in other:
            newelements[char] += 1
        return self.__class__(newelements)

    def __isub__(self, other):
        return self - other

    def __iadd__(self, other):
        return self + other

    def __str__(self):
        return str(dict(self._elements))

    def keys(self):
        """Itére sur les lettres présentes."""
        yield from (key for key, value in self._elements.items() if value)

    def __bool__(self):
        return sum(count for count in self._elements.values()) > 0

    def __getitem__(self, key):
        return self._elements.get(key, 0)

    def items(self):
        """Itère sur les couples ``(lettre, effectif)`` (uniquement pour les effectifs non nuls)."""
        for key in self._elements.keys():
            yield key, self[key]

    def __repr__(self):
        # pylint: disable=consider-using-f-string
        return """{}("{}")""".format(
            self.__class__.__name__,
            "".join(key * value for key, value in sorted(self.items())),
        )


class Intervalle:
    """Intervalle (borne minimale et maximale).

    Ajouter ou soustraire un nombre à l'intervalle applique cette opération aux deux bornes.

    >>> Intervalle(0, 2)
    Intervalle(0, 2)
    >>> Intervalle(-math.inf, 2)
    Intervalle(-math.inf, 2)
    >>> Intervalle(3, 5) + 2
    Intervalle(5, 7)
    >>> Intervalle(-math.inf, 5) - 2
    Intervalle(-math.inf, 3)
    >>> str(Intervalle(2, math.inf))
    '2:'
    >>> Intervalle(2, math.inf).pprint()
    '[2 ; +∞['
    """

    def __init__(self, mini, maxi):
        if mini is None:
            self.mini = -math.inf
        else:
            self.mini = mini
        if maxi is None:
            self.maxi = math.inf
        else:
            self.maxi = maxi

    def __add__(self, other):
        return self.__class__(self.mini + other, self.maxi + other)

    def __sub__(self, other):
        return self.__class__(self.mini - other, self.maxi - other)

    def __str__(self):
        texte = ""
        if self.mini != -math.inf:
            texte += str(self.mini)
        texte += ":"
        if self.maxi != math.inf:
            texte += str(self.maxi)
        return texte

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.mini == other.mini and self.maxi == other.maxi

    def __repr__(self):
        if self.mini == -math.inf:
            strmini = "-math.inf"
        else:
            strmini = str(self.mini)
        if self.maxi == math.inf:
            strmaxi = "math.inf"
        else:
            strmaxi = str(self.maxi)
        return f"{self.__class__.__name__}({strmini}, {strmaxi})"

    def pprint(self):
        """Représentation mathématique de l'intervalle.

        Au moment où j'écris ces mots, je ne l'utilise pas, mais je trouvais ça élégant.
        """
        if self.mini == -math.inf:
            strmini = "]-∞"
        else:
            strmini = "[" + str(self.mini)
        if self.maxi == math.inf:
            strmaxi = "+∞["
        else:
            strmaxi = str(self.maxi) + "]"
        return f"{strmini} ; {strmaxi}"


def _iter_mots_brut(dictionnaire):
    if dictionnaire.startswith("aspell://"):
        with subprocess.Popen(
            ["aspell", "-d", dictionnaire[len("aspell://") :], "dump", "master"],
            stdout=subprocess.PIPE,
            universal_newlines=True,
        ) as proc:
            yield from proc.stdout.readlines()
    else:
        with open(dictionnaire, encoding="utf8") as fichier:
            yield from fichier.readlines()


def iter_mots(dictonnaire, *, accents=True):
    """Itère tous les mots du dictionnaire.

    :param str dictionnaire:
      Un fichier à ouvrir pour y lire les mots (un par ligne)
      ou alors, si cet argument commence par `aspell://`,
      charge, avec aspell, le dictionnaire donné
      (par exemple `aspell://fr` pour le dictionnaire français).
    :param bool accents:
      Si vrai, renvoit les mots avec accents.
      Sinon, enlève les accents avant de les renvoyer.
    """
    for ligne in _iter_mots_brut(dictonnaire):
        for match in re.compile(r"\w+").finditer(ligne):
            mot = match.group()
            if accents:
                yield mot
            else:
                yield unidecode(mot)


class DictionnaireArborescent:
    """Dictionnaire arborescent."""

    def __init__(self):
        self.mot = False
        self.suffixes = {}

    def charge(self, nom, *, accents=False):
        """Charge un dictionnaire.

        :param str nom: Nom du fichier contenant le dictionnaire
            (sous la forme d'une liste de mots séparés par des espaces ou sauts de lignes).
            Si ce nom commence par ``aspell://``,
            le dictionnaire aspell de la langue donnée est utilisé à la place.
        """
        for mot in iter_mots(nom, accents=accents):
            self.ajoute(mot.lower())

    def clean(self):
        """Supprime tous les mots du dictionnaire."""
        for branche in self.suffixes.values():
            branche.clean()
        self.suffixes = {}
        self.mot = False

    def ajoute(self, lettres):
        """Ajoute un mot au dictionnaire

        Les dictionnaires suffixes sont créés si nécessaire.
        """
        if not lettres:
            self.mot = True
            return

        if lettres[0] not in self.suffixes:
            self.suffixes[lettres[0]] = DictionnaireArborescent()
        self.suffixes[lettres[0]].ajoute(lettres[1:])

    def itere_mots(self):
        """Itérateur sur les mots de cet arbre."""
        if self.mot:
            yield ""
        for lettre, branche in sorted(self.suffixes.items()):
            for suffixe in branche.itere_mots():
                yield lettre + suffixe

    def anagrammes(self, alphabet, options):
        """Itérateur sur les anagrammes.

        :param list alphabet: Lettres (sous la forme d'une liste de mots)
            dont on recherche les anagrammes.
        :param dict options: Options de la recherche.

        Les options sont :
            - ``options['accents']`` : Booléen : les accents sont-ils pris en compte, ou ignorés.
            - ``options['mots']`` :
              Intervalle (sous la forme d'un tuple ``(min, max)``) :
              nombre de mots acceptés (entre `min` et `max`).
            - ``options['lettres']`` :
              Intervalle (sous la forme d'un tuple ``(min, max)``) :
              chaque mot doit avoir entre `min` et `max` lettres.
        """
        alphabet = "".join(alphabet)
        if not options.get("accents", True):
            alphabet = unidecode(alphabet)
        yield from self._multi_anagrammes(
            Alphabet(alphabet.lower()),
            mots=options.get("mots", Intervalle(None, None)),
            lettres=options.get("lettres", Intervalle(None, None)),
        )

    def _multi_anagrammes(self, alphabet, mots, lettres, *, apres=None):
        """Recherche de plusieurs mots formant une anagramme à l'argument `alphabet`.

        :param Alphabet alphabet: Lettres à utiliser pour former les anagrammes.
        :param Intervalle mots: Nombre de mots acceptés.
        :param Intervalle lettres: Nombre de lettres (par mot) acceptées.
        :param str apres: Si différent de ``None``,
            les anagrammes doivent être plus grandes que cet argument
            (dans l'ordre lexicographique).
        """

        if not alphabet:
            # Plus de lettres disponibles :
            # - soit on a trouvé une anagramme,
            # - soit on abandonne.
            if mots.mini <= 0:
                yield []
            return

        # Si l'on continue, nous auront plus de mots que la limite à respecter.
        # On abandonne.
        if mots.maxi == 0:
            return

        # Recherche d'anagrammes
        for mot, reste in self._anagrammes(alphabet, lettres, apres=apres):
            # Pour chacun des anagrammes trouvées,
            # on cherche des anagrammes avec les lettres restantes.
            for suite in self._multi_anagrammes(reste, mots - 1, lettres, apres=mot):
                yield [mot] + suite

    def _anagrammes(self, alphabet, lettres, *, apres=None):
        """Recherche d'un seul mot formant une anagramme à `alphabet`.

        Cette fonction est une fonction similaire à :meth:`DictionnaireArborescent.anagramme`,
        mais de plus bas niveau.

        :param Alphabet alphabet: Lettres à utiliser pour former l'anagramme.
        :param Intervalle lettres: Nombre de lettres (par mot) acceptées.
        :param str apres: Si différent de ``None``,
            les anagrammes doivent être plus grandes que cet argument
            (dans l'ordre lexicographique).
        """
        if self.mot and lettres.mini <= 0:
            # On a trouvé un mot, qui est assez grand.
            yield ("", alphabet)
        if lettres.maxi < 0:
            # Le mot courant est trop long ; on ne trouvera plus de mot assez court.
            return

        if not apres:
            # Si ``apres`` n'est pas défini, on lui assigne une valeur arbitraire,
            # plus petite que toutes les autres qui seront rencontrées plus tard.
            # Tous les mots seront donc supérieurs à ``apres``.
            apres = [chr(0)]

        # Pour chacune des lettres possibles
        for debut in sorted(self.suffixes):
            # On exclut les cas impossibles :
            if debut not in alphabet:
                # La lettre n'est pas disponible dans l'aphabet
                continue
            if debut < apres[0]:
                # Le mot serait situé trop tôt dans le dictionnaire
                continue

            # Construction du mot après lequel on peut chercher
            if debut == apres[0]:
                suivant = apres[1:]
            else:
                suivant = None

            # Recherche des anagrammes dans les suffixes
            for mot, reste in self.suffixes[  # pylint: disable=protected-access
                debut
            ]._anagrammes(alphabet - debut, lettres - 1, apres=suivant):
                yield (debut + mot, reste)

    def dot(self, prefixe=""):
        """Renvoie le code Graphviz correspondant à l'objet."""
        texte = ""
        for lettre, suivant in self.suffixes.items():
            if prefixe:
                noeud = prefixe
            else:
                noeud = "#root#"
            texte += f""""{noeud}" -> "{prefixe + lettre}";\n"""
            texte += suivant.dot(prefixe + lettre)

        if prefixe:  # pylint: disable=no-else-return
            if self.mot:
                forme = "doublecircle"
            else:
                forme = "circle"
            return texte + f""""{prefixe}"[label="{prefixe[-1]}", shape={forme}];\n"""
        else:
            return textwrap.dedent(
                """
            digraph {{
                "{}" [label="", shape=point];
                {}
            }}
            """
            ).format(noeud, texte)
