..
   Copyright 2018 Louis Paternault
   
   Cette œuvre de Louis Paternault est mise à disposition selon les termes de
   la licence Creative Commons Attribution - Partage dans les Mêmes Conditions
   4.0 International (CC-BY-SA). Le texte complet de la licence est disponible
   à l'adresse : http://creativecommons.org/licenses/by-sa/4.0/deed.fr

.. _traitementimage_transformations:

***************
Transformations
***************

.. currentmodule:: jouets.traitementimage

Cette page présente l'ensemble des transformations d'images qui sont mise en œuvre par :ref:`traitementimage <traitementimage>`. Chaque transformation est accompagnée d'une image d'exemple, du code qui l'implémente, et d'une rapide explication.

L'ensemble des transformations prend la forme d'un traitement pixel par pixel. Selon la `documentation de PIL <https://pillow.readthedocs.io/en/latest/reference/PixelAccess.html>`__ (ma traduction) :

    L'accès individuel à chaque pixel est plutôt lent.
    Si vous faites une boucle sur l'ensemble des pixels d'une image,
    il existe probablement une méthode plus rapide en utilisant d'autres fonctions du module.

Donc les implémentations présentées ici ne sont pas optimales. Mais le but n'est pas d'écrire du code optimal, mais d'illustrer simplement quelques transformations d'image.

L'image de départ est `PNG transparency demonstration 24bit PNG with 8bit alpha layer <https://commons.wikimedia.org/wiki/File:PNG_transparency_demonstration_1.png>`__, de `Ed_g2s <https://commons.wikimedia.org/wiki/User:Ed_g2s>`__.

La liste des transformations est listée dans le menu à gauche de cette page.

Couleurs de pixels
==================

Noir et blanc
-------------

.. image:: ../_images/traitementimage/exemple-transformation_noir_et_blanc.jpg

Chaque pixel prend la couleur la plus proche parmi les couleurs blanche et noire.

.. literalinclude:: ../../jouets/traitementimage/__main__.py
   :linenos:
   :pyobject: transformation_noir_et_blanc
   :emphasize-lines: 8-13

Niveaux de gris
---------------

.. image:: ../_images/traitementimage/exemple-transformation_niveaux_de_gris.jpg

La moyenne des trois trames de chaque pixel est calculée, et ce pixel se voit affecter une couleur dont la valeur de chaque trame est égale à cette moyenne.

Puisque qu'une couleur dont les trois trames sont identiques est grise (au sens large : du blanc au noir), cela donne une image en niveaux de gris.

.. literalinclude:: ../../jouets/traitementimage/__main__.py
   :linenos:
   :pyobject: transformation_niveaux_de_gris
   :emphasize-lines: 8-10


Extraction de la trame rouge
----------------------------

.. image:: ../_images/traitementimage/exemple-transformation_extrait_rouge.jpg

Les trames bleue et verte sont réduite à zéro ; la trame rouge est conservée.

.. literalinclude:: ../../jouets/traitementimage/__main__.py
   :linenos:
   :pyobject: transformation_extrait_rouge
   :emphasize-lines: 8-10


Extraction de la trame verte
----------------------------

.. image:: ../_images/traitementimage/exemple-transformation_extrait_vert.jpg

Les trames rouge et bleue sont réduite à zéro ; la trame verte est conservée.

.. literalinclude:: ../../jouets/traitementimage/__main__.py
   :linenos:
   :pyobject: transformation_extrait_vert
   :emphasize-lines: 8-10


Extraction de la trame bleue
----------------------------

.. image:: ../_images/traitementimage/exemple-transformation_extrait_bleu.jpg

Les trames rouge et verte sont réduite à zéro ; la trame bleue est conservée.

.. literalinclude:: ../../jouets/traitementimage/__main__.py
   :linenos:
   :pyobject: transformation_extrait_bleu
   :emphasize-lines: 8-10


Éclaircir
---------

.. image:: ../_images/traitementimage/exemple-transformation_eclaircir.jpg

Chaque pixel est rapproché de la couleur blanche (à mi-chemin entre la couleur initiale et la couleur blanche).

.. literalinclude:: ../../jouets/traitementimage/__main__.py
   :linenos:
   :pyobject: transformation_eclaircir
   :emphasize-lines: 8-12


Assombrir
---------

.. image:: ../_images/traitementimage/exemple-transformation_assombrir.jpg

Chaque pixel est rapproché de la couleur noire (à mi-chemin entre la couleur initiale et la couleur noire).

.. literalinclude:: ../../jouets/traitementimage/__main__.py
   :linenos:
   :pyobject: transformation_assombrir
   :emphasize-lines: 8-9


Permuter les couleurs
---------------------

.. image:: ../_images/traitementimage/exemple-transformation_permuter.jpg

Les trames de chaque pixel sont permutées.
Ceci est facilement visible sur cet exemple puisque les couleurs des trois dés sont (à peu près) les couleurs primaires rouge, vert, bleu. Les couleurs de ces trois dés sont donc permutées.

.. literalinclude:: ../../jouets/traitementimage/__main__.py
   :linenos:
   :pyobject: transformation_permuter
   :emphasize-lines: 8-9


Augmenter le contraste
----------------------

.. image:: ../_images/traitementimage/exemple-transformation_contraste.jpg

Les couleurs claires (plus proches du blanc que du noir) sont éclaircies ; les couleurs sombres (plus proches du noir) sont assombries.

.. literalinclude:: ../../jouets/traitementimage/__main__.py
   :linenos:
   :pyobject: transformation_contraste
   :emphasize-lines: 8-14


Couleurs psychédéliques
-----------------------

.. image:: ../_images/traitementimage/exemple-transformation_psychedelique.jpg

A priori, n'importe quelle bijection (ou pas) de l'intervalle des entiers :math:`[0; 255]` dans lui-même convient, à condition qu'il y ait peu de points de discontinuité, pour que l'image de départ puisse tout de même être devinée.

.. literalinclude:: ../../jouets/traitementimage/__main__.py
   :linenos:
   :pyobject: transformation_psychedelique
   :emphasize-lines: 8-11


Réduire le nombre de couleurs
-----------------------------

.. image:: ../_images/traitementimage/exemple-transformation_reduit_couleurs.jpg

L'image utilise moins de couleur : cela se voit à la perte de détails.

Plutôt qu'autoriser chacun des entiers de 0 à 255 pour représenter chaque trame, seules trois valeurs sont autorisées : 0, 128, 255. Pour arriver à cela, chaque valeur est divisée par 128 (arrondie à l'entier le plus proche), ce qui produit les valeurs 0, 1, 2, puis le résultat est multiplié par 128 pour obtenir les valeurs souhaitées.

.. literalinclude:: ../../jouets/traitementimage/__main__.py
   :linenos:
   :pyobject: transformation_reduit_couleurs
   :emphasize-lines: 8-11


Inverser les couleurs
---------------------

.. image:: ../_images/traitementimage/exemple-transformation_inverse.jpg

La valeur de chaque trame se voit appliquer une symétrie par rapport au nombre 128 (ce qui correspond à la transformation affine :math:`x\mapsto 255-x`.

.. literalinclude:: ../../jouets/traitementimage/__main__.py
   :linenos:
   :pyobject: transformation_inverse
   :emphasize-lines: 8-11


Déplacement de pixels
=====================

Symétrie gauche-droite
----------------------

.. image:: ../_images/traitementimage/exemple-transformation_symetrie_gauchedroite.jpg

Symétrie par rapport à l'axe des ordonnées.

L'ordonnée de chaque pixel est conservée ; à l'abscisse on applique une symétrie par rapport à la moitié de la largeur de l'image (ce qui correspond à la transformation affine :math:`x\mapsto L-x-1` (où :math:`L` est la largeur).

.. literalinclude:: ../../jouets/traitementimage/__main__.py
   :linenos:
   :pyobject: transformation_symetrie_gauchedroite
   :emphasize-lines: 8-10


Symétrie haut-bas
-----------------

.. image:: ../_images/traitementimage/exemple-transformation_symetrie_hautbas.jpg

Symétrie par rapport à l'axe des abscisses.

L'abscisse de chaque pixel est conservée ; à l'ordonnée on applique une symétrie par rapport à la moitié de la hauteur de l'image (ce qui correspond à la transformation affine :math:`x\mapsto h-x-1` (où :math:`h` est la hauteur).

.. literalinclude:: ../../jouets/traitementimage/__main__.py
   :linenos:
   :pyobject: transformation_symetrie_hautbas
   :emphasize-lines: 8


Rotation
--------

.. image:: ../_images/traitementimage/exemple-transformation_rotation90.jpg

Rotation d'angle :math:`\frac{\pi}{2}` (90°).

Chaque pixel de coordonnées :math:`(x; y)` est déplacé aux coordonnées :math:`(L-1-y; x)` (où :math:`L` est la largeur de l'image).

.. literalinclude:: ../../jouets/traitementimage/__main__.py
   :linenos:
   :pyobject: transformation_rotation90
   :emphasize-lines: 8


Autre
=====

Ajouteur un cadre
-----------------

.. image:: ../_images/traitementimage/exemple-transformation_ajouter_cadre.jpg

Les dimensions de l'image sont agrandies, et une couleur est affectée aux pixels des bords de l'image.

.. literalinclude:: ../../jouets/traitementimage/__main__.py
   :linenos:
   :pyobject: transformation_ajouter_cadre
   :emphasize-lines: 8-19


Réduire l'image (version rapide)
--------------------------------

.. image:: ../_images/traitementimage/exemple-transformation_reduire1.jpg

Chaque carrée de quatre pixels est réduit à un unique pixel égal au coin supérieur gauche du carré. Les autres pixels sont ignorés.

.. literalinclude:: ../../jouets/traitementimage/__main__.py
   :linenos:
   :pyobject: transformation_reduire1
   :emphasize-lines: 8


Réduire l'image (version précise)
---------------------------------

.. image:: ../_images/traitementimage/exemple-transformation_reduire2.jpg

Chaque carrée de quatre pixels est réduit à un unique pixel égal à la moyenne des quatre pixels.

.. literalinclude:: ../../jouets/traitementimage/__main__.py
   :linenos:
   :pyobject: transformation_reduire2
   :emphasize-lines: 8-19

