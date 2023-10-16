# Copyright 2018-2023 Louis Paternault
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

"""Logiciel de traitement d'image."""

from PIL import Image

from ..utils.aargparse import analyseur
from ..utils.erreurs import ErreurInterne

VERSION = "0.1.0"


def docstring(fonction):
    """Extrait la docstring d'une fonction."""
    if not fonction.__doc__.strip():
        raise ErreurInterne(f"La fonction '{fonction.__name__}' n'a pas de docstring.")
    return fonction.__doc__.strip().split("\n")[0]


def transformation_niveaux_de_gris(source, destination):
    """Convertir l'image en niveaux de gris."""
    source = Image.open(source).convert("RGB")
    dest = Image.new("RGB", source.size)

    for x in range(source.width):
        for y in range(source.height):
            couleur = source.getpixel((x, y))
            moyenne = (couleur[0] + couleur[1] + couleur[2]) // 3
            dest.putpixel((x, y), (moyenne, moyenne, moyenne))

    dest.save(destination)


def transformation_noir_et_blanc(source, destination):
    """Convertir l'image en noir et blanc."""
    source = Image.open(source).convert("RGB")
    dest = Image.new("RGB", source.size)

    for x in range(source.width):
        for y in range(source.height):
            couleur = source.getpixel((x, y))
            if sum(couleur) > 3 * 127:
                nouvelle = (255, 255, 255)
            else:
                nouvelle = (0, 0, 0)
            dest.putpixel((x, y), nouvelle)

    dest.save(destination)


def transformation_extrait_rouge(source, destination):
    """Extraire la couleur rouge de l'image"""
    source = Image.open(source).convert("RGB")
    dest = Image.new("RGB", source.size)

    for x in range(source.width):
        for y in range(source.height):
            original = source.getpixel((x, y))
            nouvelle = (original[0], 0, 0)
            dest.putpixel((x, y), nouvelle)

    dest.save(destination)


def transformation_extrait_vert(source, destination):
    """Extraire la couleur vert de l'image"""
    source = Image.open(source).convert("RGB")
    dest = Image.new("RGB", source.size)

    for x in range(source.width):
        for y in range(source.height):
            original = source.getpixel((x, y))
            nouvelle = (0, original[1], 0)
            dest.putpixel((x, y), nouvelle)

    dest.save(destination)


def transformation_extrait_bleu(source, destination):
    """Extraire la couleur bleu de l'image"""
    source = Image.open(source).convert("RGB")
    dest = Image.new("RGB", source.size)

    for x in range(source.width):
        for y in range(source.height):
            original = source.getpixel((x, y))
            nouvelle = (0, 0, original[2])
            dest.putpixel((x, y), nouvelle)

    dest.save(destination)


def transformation_symetrie_gauchedroite(
    source, destination
):  # pylint: disable=invalid-name
    """Effectuer la symérie gauche-droite"""
    source = Image.open(source).convert("RGB")
    dest = Image.new("RGB", source.size)

    for x in range(source.width):
        for y in range(source.height):
            dest.putpixel((source.width - x - 1, y), source.getpixel((x, y)))

    dest.save(destination)


def transformation_symetrie_hautbas(source, destination):
    """Effectuer la symérie haut-bas"""
    source = Image.open(source).convert("RGB")
    dest = Image.new("RGB", source.size)

    for x in range(source.width):
        for y in range(source.height):
            dest.putpixel((x, source.height - y - 1), source.getpixel((x, y)))

    dest.save(destination)


def transformation_ajouter_cadre(source, destination):
    """Ajouter un cadre"""
    source = Image.open(source).convert("RGB")
    bord = 5  # Épaisseur du cadre
    couleur = (122, 119, 184)
    dest = Image.new("RGB", (source.width + 2 * bord, source.height + 2 * bord))

    for x in range(source.width):
        for y in range(source.height):
            dest.putpixel((x + bord, y + bord), source.getpixel((x, y)))
    for x in range(source.width + 2 * bord):
        for y in range(source.height + 2 * bord):
            if (
                x <= bord
                or x >= source.width + bord
                or y <= bord
                or y >= source.height + bord
            ):
                dest.putpixel((x, y), couleur)

    dest.save(destination)


def transformation_reduire1(source, destination):
    """Réduire l'image de moitié (version rapide)"""
    source = Image.open(source).convert("RGB")
    dest = Image.new("RGB", (source.width // 2, source.height // 2))

    for x in range(source.width // 2):
        for y in range(source.height // 2):
            dest.putpixel((x, y), source.getpixel((2 * x, 2 * y)))

    dest.save(destination)


def transformation_reduire2(source, destination):
    """Réduire l'image de moitié (version plus précise)"""
    source = Image.open(source).convert("RGB")
    dest = Image.new("RGB", (source.width // 2, source.height // 2))

    for x in range(source.width // 2):
        for y in range(source.height // 2):
            dest.putpixel(
                (x, y),
                tuple(
                    sum(l) // 4
                    for l in zip(
                        source.getpixel((2 * x, 2 * y)),
                        source.getpixel((2 * x, 2 * y + 1)),
                        source.getpixel((2 * x + 1, 2 * y)),
                        source.getpixel((2 * x + 1, 2 * y + 1)),
                    )
                ),
            )

    dest.save(destination)


def transformation_eclaircir(source, destination):
    """Éclaircir l'image"""
    source = Image.open(source).convert("RGB")
    dest = Image.new("RGB", source.size)

    for x in range(source.width):
        for y in range(source.height):
            couleur = source.getpixel((x, y))
            dest.putpixel(
                (x, y),
                (couleur[0] // 2 + 128, couleur[1] // 2 + 128, couleur[2] // 2 + 128),
            )

    dest.save(destination)


def transformation_assombrir(source, destination):
    """Assombrir l'image"""
    source = Image.open(source).convert("RGB")
    dest = Image.new("RGB", source.size)

    for x in range(source.width):
        for y in range(source.height):
            couleur = source.getpixel((x, y))
            dest.putpixel((x, y), (couleur[0] // 2, couleur[1] // 2, couleur[2] // 2))

    dest.save(destination)


def transformation_permuter(source, destination):
    """Permuter les couleurs"""
    source = Image.open(source).convert("RGB")
    dest = Image.new("RGB", source.size)

    for x in range(source.width):
        for y in range(source.height):
            couleur = source.getpixel((x, y))
            dest.putpixel((x, y), (couleur[1], couleur[2], couleur[0]))

    dest.save(destination)


def transformation_rotation90(source, destination):
    """Pivoter la photo de 90° vers la gauche"""
    source = Image.open(source).convert("RGB")
    dest = Image.new("RGB", (source.height, source.width))

    for x in range(source.height):
        for y in range(source.width):
            dest.putpixel((x, y), source.getpixel((source.width - 1 - y, x)))

    dest.save(destination)


def transformation_contraste(source, destination):
    """Augmenter le contraste"""
    source = Image.open(source).convert("RGB")
    dest = Image.new("RGB", source.size)

    for x in range(source.width):
        for y in range(source.height):
            couleur = list(source.getpixel((x, y)))
            for compteur in range(3):
                if couleur[compteur] < 128:
                    couleur[compteur] = couleur[compteur] // 2
                else:
                    couleur[compteur] = couleur[compteur] // 2 + 128
            dest.putpixel((x, y), tuple(couleur))

    dest.save(destination)


def transformation_inverse(source, destination):
    """Inverser les couleurs"""
    source = Image.open(source).convert("RGB")
    dest = Image.new("RGB", source.size)

    for x in range(source.width):
        for y in range(source.height):
            couleur = source.getpixel((x, y))
            dest.putpixel(
                (x, y), (255 - couleur[0], 255 - couleur[1], 255 - couleur[2])
            )

    dest.save(destination)


def transformation_psychedelique(source, destination):
    """Produire une version psychédélique de l'image"""
    source = Image.open(source).convert("RGB")
    dest = Image.new("RGB", source.size)

    for x in range(source.width):
        for y in range(source.height):
            couleur = list(source.getpixel((x, y)))
            for compteur in range(3):
                couleur[compteur] = 16 * (couleur[compteur] % 16)
            dest.putpixel((x, y), tuple(couleur))

    dest.save(destination)


def transformation_reduit_couleurs(source, destination):
    """Réduire le nombre de couleurs"""
    source = Image.open(source).convert("RGB")
    dest = Image.new("RGB", source.size)

    for x in range(source.width):
        for y in range(source.height):
            couleur = list(source.getpixel((x, y)))
            for compteur in range(3):
                couleur[compteur] = 128 * round(couleur[compteur] / 128)
            dest.putpixel((x, y), tuple(couleur))

    dest.save(destination)


TRANSFORMATIONS = [
    transformation_noir_et_blanc,
    transformation_niveaux_de_gris,
    transformation_extrait_rouge,
    transformation_extrait_vert,
    transformation_extrait_bleu,
    transformation_symetrie_gauchedroite,
    transformation_symetrie_hautbas,
    transformation_ajouter_cadre,
    transformation_reduire1,
    transformation_reduire2,
    transformation_eclaircir,
    transformation_assombrir,
    transformation_permuter,
    transformation_rotation90,
    transformation_contraste,
    transformation_psychedelique,
    transformation_reduit_couleurs,
    transformation_inverse,
]


def choix_transformation():
    """Propose à l'utilisateur la liste des transformations, et renvoit le choix."""
    print("#" * 80)
    print("# Choix de la transformation #")
    # Création d'une liste triée de transformations
    transformations = sorted(
        (docstring(fonction), fonction) for fonction in TRANSFORMATIONS
    )
    for compteur, transformation in enumerate(transformations):
        print(f"[{compteur}] {transformation[0]}")
    while True:
        choix = input("Quelle transformation effectuer ? ")
        try:
            if 0 <= int(choix) < len(transformations):
                print()
                return transformations[int(choix)][1]
        except ValueError:
            pass
        print(f"Veuillez choisir un nombre entre 0 et {len(transformations) - 1}.")


def analyse():
    """Renvoie un analyseur de la ligne de commande."""
    parser = analyseur(
        VERSION, prog="traitementimage", description="Image manipulation program"
    )
    parser.add_argument("source", type=str, help="Source file.")
    parser.add_argument("destination", type=str, help="Destination file.")
    return parser


def main():
    """Fonction principale."""
    options = analyse().parse_args()
    transformation = choix_transformation()
    transformation(options.source, options.destination)


if __name__ == "__main__":
    main()
