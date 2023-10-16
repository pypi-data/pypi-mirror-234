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

"""Génère les images d'exemples pour la documentation de `traitementimage`."""

import os
import sys

from PIL import Image

try:
    import jouets.traitementimage.__main__ as traitementimage
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    import jouets.traitementimage.__main__ as traitementimage

os.chdir(os.path.dirname(__file__))

SRCNAME = "source.png"
TMPNAME = "temp.png"
GAP = 20


def vertical_offset(thisheight, otherheight):
    if thisheight >= otherheight:
        return 0
    return (otherheight - thisheight) // 2


def genere_exemple(fonction):
    print("Generating example for function '{}'…".format(fonction.__name__))
    fonction(SRCNAME, TMPNAME)

    srcimg = Image.open(SRCNAME)
    tmpimg = Image.open(TMPNAME)

    exemple = Image.new(
        "RGB",
        (srcimg.size[0] + GAP + tmpimg.size[0], max(srcimg.size[1], tmpimg.size[1])),
        (255, 255, 255),
    )

    exemple.paste(srcimg, (0, vertical_offset(srcimg.size[1], tmpimg.size[1])))
    exemple.paste(
        tmpimg, (srcimg.size[0] + GAP, vertical_offset(tmpimg.size[1], srcimg.size[1]))
    )

    exemple.save("exemple-{}.jpg".format(fonction.__name__))


def main():
    for fonction in traitementimage.TRANSFORMATIONS:
        genere_exemple(fonction)


if __name__ == "__main__":
    main()
