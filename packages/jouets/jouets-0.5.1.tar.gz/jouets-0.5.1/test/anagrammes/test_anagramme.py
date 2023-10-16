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

"""Test de anagrammes"""

import unittest

from jouets.anagrammes import DictionnaireArborescent, Intervalle

DICTIONNAIRE = ["chat", "chi", "chie", "chien", "chienne", "en", "ne", "niche"]


# pylint: disable=too-many-public-methods
class TestAnagrammes(unittest.TestCase):
    """Test de la recherche d'anagrammes."""

    def test_anagrammes(self):
        """Test de la recherche d'anagrammes."""
        dico = DictionnaireArborescent()
        for mot in DICTIONNAIRE:
            dico.ajoute(mot)

        self.assertCountEqual(
            dico.anagrammes(
                "chien",
                options={"mots": Intervalle(1, 1), "lettres": Intervalle(None, None)},
            ),
            [["chien"], ["niche"]],
        )

        self.assertCountEqual(
            dico.anagrammes(
                "chien",
                options={
                    "mots": Intervalle(None, None),
                    "lettres": Intervalle(None, None),
                },
            ),
            [["chi", "en"], ["chi", "ne"], ["chien"], ["niche"]],
        )

        self.assertCountEqual(
            dico.anagrammes(
                "chien",
                options={
                    "mots": Intervalle(2, None),
                    "lettres": Intervalle(None, None),
                },
            ),
            [["chi", "en"], ["chi", "ne"]],
        )

        self.assertCountEqual(
            dico.anagrammes(
                "chien",
                options={
                    "mots": Intervalle(3, None),
                    "lettres": Intervalle(None, None),
                },
            ),
            [],
        )

        self.assertCountEqual(
            dico.anagrammes(
                "chien",
                options={"mots": Intervalle(None, None), "lettres": Intervalle(2, 3)},
            ),
            [["chi", "en"], ["chi", "ne"]],
        )

        self.assertCountEqual(
            dico.anagrammes(
                "chien",
                options={"mots": Intervalle(None, None), "lettres": Intervalle(3, 5)},
            ),
            [["chien"], ["niche"]],
        )
