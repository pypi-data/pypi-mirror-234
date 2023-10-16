..
   Copyright 2023 Louis Paternault
   
   Cette œuvre de Louis Paternault est mise à disposition selon les termes de
   la licence Creative Commons Attribution - Partage dans les Mêmes Conditions
   4.0 International (CC-BY-SA). Le texte complet de la licence est disponible
   à l'adresse : http://creativecommons.org/licenses/by-sa/4.0/deed.fr

.. _latex:

******************************************
`LaTeX` — Bouts de codes amusants en LaTeX
******************************************

J'aime beaucoup utiliser `PGF/TikZ <https://www.ctan.org/pkg/pgf>`__ pour tracer mes figures en :math:`\LaTeX`, car cela me permet :

- en tant qu'informaticien, de programmer mes figures ;
- en tant que mathématicien, d'utiliser un programme de construction pour dessiner.

Voici quelques images, construites en utilisant quelques calculs mathématiques (surtout de la géométrie cartésienne et de la trigonométrie).

.. contents::
   :local:

Étoiles
=======

J'avais besoin d'une étoile à cinq branches pour illustrer un projet. J'ai écrit la fonction ``\etoile{rayon}{sommets}{décalage}`` :

- ``rayon`` : rayon du cercle dans lequel est inscrit l'étoile ;
- ``sommets`` : nombre de pointes de l'étoile (en fait, il s'agit du nombre de sommets du polygone régulier utilisé pour construire l'étoile) ;
- ``décalage`` : deux pointes de l'étoile sont reliées par un segment (tronqué) ; cet argument donne le nombre de pointes situées entre deux sommets (dans le sens direct).

Voici quelques exemples, et `quelques explications supplémentaires <latex/etoiles>`__

+---------------------------------+----------------------+
| .. image:: latex/etoiles-01.svg | ``\etoile{1}{5}{2}`` |
+---------------------------------+----------------------+
| .. image:: latex/etoiles-02.svg | ``\etoile{1}{6}{2}`` |
+---------------------------------+----------------------+
| .. image:: latex/etoiles-03.svg | ``\etoile{1}{7}{2}`` |
+---------------------------------+----------------------+
| .. image:: latex/etoiles-04.svg | ``\etoile{1}{7}{3}`` |
+---------------------------------+----------------------+
| .. image:: latex/etoiles-05.svg | ``\etoile{1}{8}{2}`` |
+---------------------------------+----------------------+
| .. image:: latex/etoiles-06.svg | ``\etoile{1}{8}{3}`` |
+---------------------------------+----------------------+

.. collapse:: Voir le code source

   .. literalinclude:: ../latex/etoiles.tex
      :language: latex

Nœuds 1
=======

J'ai vu une courte vidéo d'un dessin à la main sur un réseau social quelconque, et j'ai eu envie de le reproduire en :math:`\LaTeX`. Je n'ai pas pu m'empêcher de généraliser.

La commande ``\noeud{sommets}{rayon}{épaisseur}`` dessine un nœud avec :

- ``sommets`` : le nombre de sommets du polygone régulier sur lequel est construit le nœud ;
- ``rayon`` : le rayon du cercle circonscrit au polygone régulier susnommé ;
- ``épaisseur`` : l'épaisseur de la « corde ».

Voici quelques exemples, et `quelques explications supplémentaires <latex/noeuds1>`__

+---------------------------------+-----------------------+
| .. image:: latex/noeuds1-01.svg | ``\noeud{3}{1}{1}``   |
+---------------------------------+-----------------------+
| .. image:: latex/noeuds1-02.svg | ``\noeud{4}{1}{.5}``  |
+---------------------------------+-----------------------+
| .. image:: latex/noeuds1-03.svg | ``\noeud{5}{1}{.3}``  |
+---------------------------------+-----------------------+
| .. image:: latex/noeuds1-04.svg | ``\noeud{6}{1}{.15}`` |
+---------------------------------+-----------------------+
| .. image:: latex/noeuds1-05.svg | ``\noeud{7}{1}{.1}``  |
+---------------------------------+-----------------------+
| .. image:: latex/noeuds1-06.svg | ``\noeud{9}{1}{.05}`` |
+---------------------------------+-----------------------+

Mes calculs supposaient que la corde serait assez fine pour ne pas déborder de la boucle voisine. Je m'attendais à une catastrophe, mais vu la manière dont sont construites ces figures, à ma grande surprise, cela produit des tresses.

+---------------------------------+-----------------------+
| .. image:: latex/noeuds1-07.svg | ``\noeud{5}{1}{.7}``  |
+---------------------------------+-----------------------+
| .. image:: latex/noeuds1-08.svg | ``\noeud{6}{1}{.5}``  |
+---------------------------------+-----------------------+
| .. image:: latex/noeuds1-09.svg | ``\noeud{7}{1}{.4}``  |
+---------------------------------+-----------------------+
| .. image:: latex/noeuds1-10.svg | ``\noeud{8}{1}{.3}``  |
+---------------------------------+-----------------------+

.. collapse:: Voir le code source

   .. literalinclude:: ../latex/noeuds1.tex
      :language: latex

Nœuds 2
=======

Après avoir réalisé les nœuds précédents, je suis tombé sur le paquet `fiziko <https://habr.com/en/articles/454376/>`__ (de Sergey Slyusarev), qui réalise mieux en moins de lignes de code. J'ai donc cherché à améliorer ces nœuds, en remplaçant les cercles par des courbes de Bézier. Le résultat est ici.

La commande ``\noeud{sommets}{saut}{rayon1}{rayon2}{épaisseur}{dureté}`` dessine un nœud avec :

- ``sommets`` : le nombre de sommets du polygone régulier sur lequel est construit le nœud ;
- ``saut`` : indique le nombre d'arêtes que « saute » une courbe issue d'un sommet du polygone avant de rejoindre le sommet suivant ;
- ``rayon1`` : le rayon du cercle inscrit dans le polygone régulier central ;
- ``rayon2`` : le rayon des extrémités des courbes (sans compter l'épaisseur) ;
- ``épaisseur`` : l'épaisseur de la « corde » ;
- ``dureté`` : indique à quel point les courbes doivent êtres « pointues » ou « arrondies ».

Voici quelques exemples, et `quelques explications supplémentaires <latex/noeuds2>`__

Tresses
-------

+---------------------------------+------------------------------------+
| .. image:: latex/noeuds2-01.svg | ``\noeud{20}{15}{2}{2.2}{.08}{1}`` |
+---------------------------------+------------------------------------+
| .. image:: latex/noeuds2-02.svg | ``\noeud{40}{5}{2}{2.4}{.07}{.4}`` |
+---------------------------------+------------------------------------+

Rosaces
-------

+---------------------------------+------------------------------------+
| .. image:: latex/noeuds2-03.svg | ``\noeud{20}{20}{2}{2.2}{.08}{1}`` |
+---------------------------------+------------------------------------+
| .. image:: latex/noeuds2-04.svg | ``\noeud{20}{25}{2}{2.2}{.08}{1}`` |
+---------------------------------+------------------------------------+

Inclassables
------------

+---------------------------------+------------------------------------+
| .. image:: latex/noeuds2-05.svg | ``\noeud{20}{30}{2}{2.2}{.08}{1}`` |
+---------------------------------+------------------------------------+
| .. image:: latex/noeuds2-06.svg | ``\noeud{5}{1}{1}{.8}{.2}{.4}``    |
+---------------------------------+------------------------------------+
| .. image:: latex/noeuds2-07.svg | ``\noeud{7}{3}{1}{2}{.2}{3}``      |
+---------------------------------+------------------------------------+

Nœuds serrés
------------

+---------------------------------+------------------------------------+
| .. image:: latex/noeuds2-08.svg | ``\noeud{3}{1}{1}{2}{1}{1}``       |
+---------------------------------+------------------------------------+
| .. image:: latex/noeuds2-09.svg | ``\noeud{4}{1}{1}{1.5}{.5}{.6}``   |
+---------------------------------+------------------------------------+
| .. image:: latex/noeuds2-10.svg | ``\noeud{5}{1}{1}{1.5}{.5}{.4}``   |
+---------------------------------+------------------------------------+
| .. image:: latex/noeuds2-11.svg | ``\noeud{6}{1}{1}{1.5}{.5}{.4}``   |
+---------------------------------+------------------------------------+
| .. image:: latex/noeuds2-12.svg | ``\noeud{8}{1}{1}{1.25}{.25}{.2}`` |
+---------------------------------+------------------------------------+

Nœuds avec du jeu
-----------------

+---------------------------------+------------------------------------+
| .. image:: latex/noeuds2-13.svg | ``\noeud{5}{1}{1}{1.5}{.2}{.4}``   |
+---------------------------------+------------------------------------+
| .. image:: latex/noeuds2-14.svg | ``\noeud{6}{1}{1}{1.5}{.2}{.4}``   |
+---------------------------------+------------------------------------+

Nœuds avec beaucoup de jeu ; Cercles
------------------------------------

+---------------------------------+------------------------------------+
| .. image:: latex/noeuds2-15.svg | ``\noeud{4}{3}{1}{3}{.2}{3}``      |
+---------------------------------+------------------------------------+
| .. image:: latex/noeuds2-16.svg | ``\noeud{5}{2}{1}{2}{.5}{1}``      |
+---------------------------------+------------------------------------+
| .. image:: latex/noeuds2-17.svg | ``\noeud{5}{3}{1}{3}{.2}{3}``      |
+---------------------------------+------------------------------------+
| .. image:: latex/noeuds2-18.svg | ``\noeud{5}{3}{1}{2}{.2}{1}``      |
+---------------------------------+------------------------------------+
| .. image:: latex/noeuds2-19.svg | ``\noeud{5}{2}{1}{2}{.2}{1}``      |
+---------------------------------+------------------------------------+
| .. image:: latex/noeuds2-20.svg | ``\noeud{7}{2}{1}{2}{.2}{1}``      |
+---------------------------------+------------------------------------+

Fleurs
------

+---------------------------------+------------------------------------+
| .. image:: latex/noeuds2-21.svg | ``\noeud{5}{4}{1}{2}{.5}{1}``      |
+---------------------------------+------------------------------------+
| .. image:: latex/noeuds2-22.svg | ``\noeud{5}{5}{1}{2}{.5}{1}``      |
+---------------------------------+------------------------------------+
| .. image:: latex/noeuds2-23.svg | ``\noeud{5}{6}{1}{2}{.5}{1}``      |
+---------------------------------+------------------------------------+
| .. image:: latex/noeuds2-24.svg | ``\noeud{5}{7}{1}{2}{.5}{1}``      |
+---------------------------------+------------------------------------+
| .. image:: latex/noeuds2-25.svg | ``\noeud{7}{5}{1}{2}{.2}{.5}``     |
+---------------------------------+------------------------------------+

.. collapse:: Voir le code source

   .. literalinclude:: ../latex/noeuds2.tex
      :language: latex

Explications
============

.. toctree::
   :maxdepth: 1

   latex/etoiles
   latex/noeuds1
   latex/noeuds2
