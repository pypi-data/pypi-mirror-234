# Copyright 2020-2021 Louis Paternault
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

"""Animation avec emojis des files d'usagers."""

import time

import termcolor

from . import Sortie

PREMIER = 7919
COULEURS = ["red", "green", "yellow", "blue", "magenta", "cyan", "white"]
PERSONNES = "👵👴🧓👱👩🧔👨🧑👧👦🧒🧍🚶🧟🧞🧝🧜🧛🧚🧙🤰👰🤵🧕👲👳👸🤴👷💂👮"


class Unicode(Sortie):
    """Tracé des files d'attente en unicode (argument: temps d'attente)."""

    keyword = "unicode"

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        if args:
            self.speed = float(args[0])
        else:
            self.speed = 0.5

    def tictac(self):
        # Clear screen
        print(chr(27) + "[2J")

        file_numero = -1
        for i, guichet in enumerate(self.salle.guichets):
            file_numero_nouveau = i * len(self.salle.files) // len(self.salle.guichets)
            if file_numero_nouveau != file_numero:
                file_numero = file_numero_nouveau
                print(80 * "─")
                print("⇒ ", end="")
                for usager in self.salle.files[file_numero]:
                    print(PERSONNES[(id(usager) % PREMIER) % len(PERSONNES)], end="")
                    termcolor.cprint(
                        usager.service,
                        color=COULEURS[(id(usager) % PREMIER) % len(COULEURS)],
                        end=" ",
                    )
                print()
            if guichet is None:
                print("✖")
            else:
                print(PERSONNES[(id(guichet) % PREMIER) % len(PERSONNES)], end="")
                termcolor.cprint(
                    guichet.heure_sortie - self.salle.horloge.temps,
                    color=COULEURS[(id(guichet) % PREMIER) % len(COULEURS)],
                )

        time.sleep(self.speed)
