..
   Copyright 2020-2023 Louis Paternault

   Cette œuvre de Louis Paternault est mise à disposition selon les termes de
   la licence Creative Commons Attribution - Partage dans les Mêmes Conditions
   4.0 International (CC-BY-SA). Le texte complet de la licence est disponible
   à l'adresse : http://creativecommons.org/licenses/by-sa/4.0/deed.fr

.. _doc-verger:

***************************************************
`verger` — Calcul des probabilités au jeu du verger
***************************************************

.. currentmodule:: jouets.verger

Voici `encore <bataille>`_ un programme inspiré de jeux avec ma fille.

Le jeu du `Verger <https://www.haba.de/fr_FR/le-verger--003170>`_ est un jeu coopératif classique, reposant *beaucoup* sur le hasard. J'ai écrit ce programme pour répondre à deux questions :

- quelle est la probabilité de victoire ;
- comment cette probabilité varie-t-elle suivant la stratégie utilisée ?

.. contents::
   :local:
   :depth: 1

Règle du jeu
============

Les règles données ici concernent le jeu d'origine ; les nombres donnés peuvent être paramétrés avec les options de ce programme.

Le plateau contient 4 arbres contenant 10 fruits chacun, et un puzzle de corbeau de 9 pièces (vide au départ). C'est un jeu coopératif, et les règles ne changent pas selon le nombre de joueurs, donc nous supposons ici qu'une seule personne joue.

Le dé est composé de 6 faces : une par arbre, une face panier, et une face corbeau.

À son tour de jeu, la joueuse lance le dé :

- si elle obtient un arbre, elle cueille un fruit de cet arbre (s'il en reste) ;
- si elle obtient le panier, elle cueille deux fruits au choix ;
- si elle obtient le corbeau, elle ajoute une pièce du puzzle du corbeau.

Le jeu se termine lorsqu'il ne reste plus aucun fruit sur les arbres (victoire) ou que le puzzle du corbeau est complet (défaite).

.. note::

   Dans toute la suite, nous écrirons abusivement « il reste huit corbeaux » plutôt que « il reste huit pièces de puzzle du corbeau ».

Stratégies
==========

Le seul mécanisme ne mettant pas en jeu le hasard est le choix des fruits à cueillir lorsque le dé indique le panier.
Les trois stratégies mise en œuvre sont :

- `max` : les deux fruits sont pris depuis le ou les arbres qui en contiennent le plus ;
- `min` : les deux fruits sont pris depuis le ou les arbres qui en contiennent le moins ;
- `random` : les deux fruits sont pris au hasard.

Calcul des probabilités
=======================

Remarques préliminaires
-----------------------

Quels remarques vont simplifier nos calculs.

Premièrement, les arbres sont interchangeables : s'il reste trois pommes et deux poires, la probabilité de victoire est la même que s'il restait trois prunes et deux pommes (la démonstration est laissée au lecteur patient).
La conséquence est que, dans le calcul mathématique comme dans le programme informatique, les arbres sont toujours triés (par ordre croissant ou décroissante selon le contexte).

Ensuite, les arbres vides peuvent être supprimés du jeu. Ainsi, jouer avec quatre arbres dont un vide, avec un dé à six faces (quatre arbres, un panier, un corbeau) donne la même probabilité de victoire que jouer avec trois arbres, avec un dé à cinq faces (trois arbres, un panier, un corbeau).
La démonstration est laissée au lecteur patient.
Donc dans les deux calculs (mathématique et informatique), les arbres vides sont simplement supprimés.

Calcul mathématique
-------------------

Je n'ai pas étudié mathématiquement le jeu original, mais j'ai étudié un jeu simplifié, avec au maximum deux arbres à deux fruits, et deux corbeaux.

Le graphe probabiliste suivant présente la situation :

- les états `A` à `J` correspondent à des états possibles du jeu, sous la forme ``ARBRES|CORBEAU``. Par exemple, l'état `C`, marqué ``21|2`` signifie qu'il reste deux arbres (l'un à deux fruits, l'autre à un seul fruit), et deux corbeaux ;
- les états `K` et `L` correspondent respectivement à la victoire et à la défaite.

Les poids des transitions correspondent au probabilités pour passer d'un état à l'autre.

.. graphviz:: verger/graphe-probabiliste.dot

La matrice probabiliste correspondant à ce graphe est la suivante.

.. math::

   M = \begin{bmatrix}
      0 & 1/4 & 1/2 & 0 & 0 & 1/4 & 0 & 0 & 0 & 0 & 0 & 0 \\
      0 & 0 & 0 & 1/2 & 0 & 0 & 0 & 1/4 & 0 & 0 & 1/4 & 0 \\
      0 & 0 & 0 & 1/4 & 1/4 & 1/4 & 0 & 0 & 1/4 & 0 & 0 & 0 \\
      0 & 0 & 0 & 0 & 0 & 0 & 1/4 & 1/4 & 0 & 1/4 & 1/4 & 0 \\
      0 & 0 & 0 & 0 & 0 & 0 & 1/3 & 0 & 1/3 & 0 & 0 & 1/3 \\
      0 & 0 & 0 & 0 & 0 & 0 & 0 & 1/4 & 1/2 & 0 & 0 & 1/4 \\
      0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1/3 & 1/3 & 1/3 \\
      0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1/2 & 1/4 & 1/4 \\
      0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1/3 & 0 & 2/3 \\
      0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1/3 & 2/3 \\
      0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 \\
      0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 \\
   \end{bmatrix}

.. note::

   La voici également sous une forme qu'il est possible de copier-coller pour faire vos propres manipulations avec `XCas <https://www-fourier.ujf-grenoble.fr/~parisse/giac_fr.html>`__.

          [[0, 1/4, 1/2, 0, 0, 1/4, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 1/2, 0, 0, 0, 1/4, 0, 0, 1/4, 0],
          [0, 0, 0, 1/4, 1/4, 1/4, 0, 0, 1/4, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 1/4, 1/4, 0, 1/4, 1/4, 0],
          [0, 0, 0, 0, 0, 0, 1/3, 0, 1/3, 0, 0, 1/3],
          [0, 0, 0, 0, 0, 0, 0, 1/4, 1/2, 0, 0, 1/4],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 1/3, 1/3, 1/3],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 1/2, 1/4, 1/4],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 1/3, 0, 2/3],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1/3, 2/3],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]]

Pour calculer la probabilité de victoire, et faut calculer l'état stable à partir de l'état initial `A` (correspondant à la matrice :math:`A=\begin{bmatrix}1&0&0&0&0&0&0&0&0&0&0&0\end{bmatrix}`). Ça, c'est la méthode propre.

La méthode « cracra » est de remarquer que quel que soit l'état initial, il devrait converger vers un état stable où tous les coefficients sont nuls, exceptés les deux derniers (la démonstration est laissée au lecteur patient).

Puisque l'état converge, :math:`A\times M^{1000}` devrait être très proche de l'état limite. Donc :math:`A\times M^{1000}=\begin{bmatrix}0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0,322627314815 & 0,677372685185\end{bmatrix}`, et cela signifie qu'avec deux arbres à deux fruits chacun, et deux corbeaux (état `A`), la probabilité de victoire est environ 0,677.

Voici quelques autres exemples.

.. math::

   \begin{align}
      A\times M^{1000}&=\begin{bmatrix}1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0\end{bmatrix} \times M^{1000} = \begin{bmatrix}0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0,322627314815 & 0,677372685185\end{bmatrix}\\
      B\times M^{1000}&=\begin{bmatrix}0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0\end{bmatrix} \times M^{1000} = \begin{bmatrix}0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0,628472222222 & 0,371527777778\end{bmatrix}\\
      E\times M^{1000}&=\begin{bmatrix}0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0\end{bmatrix} \times M^{1000} = \begin{bmatrix}0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0,185185185185 & 0,814814814815\end{bmatrix}\\
      F\times M^{1000}&=\begin{bmatrix}0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0\end{bmatrix} \times M^{1000} = \begin{bmatrix}0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0,159722222222 & 0,840277777778\end{bmatrix}\\
      G\times M^{1000}&=\begin{bmatrix}0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0\end{bmatrix} \times M^{1000} = \begin{bmatrix}0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0,444444444444 & 0,555555555556\end{bmatrix}\\
      H\times M^{1000}&=\begin{bmatrix}0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0\end{bmatrix} \times M^{1000} = \begin{bmatrix}0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0,416666666667 & 0,583333333333\end{bmatrix}\\
      I\times M^{1000}&=\begin{bmatrix}0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0\end{bmatrix} \times M^{1000} = \begin{bmatrix}0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0,111111111111 & 0,888888888889\end{bmatrix}\\
      J\times M^{1000}&=\begin{bmatrix}0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0\end{bmatrix} \times M^{1000} = \begin{bmatrix}0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0,333333333333 & 0,666666666667\end{bmatrix}\\
   \end{align}


Calcul informatique
-------------------

Comme dans le calcul des probabilités du `jeu de mafia <mafia>`__, le calcul est fait par récurrence. Pour :math:`n` arbres, :math:`c` corbeaux, une stratégie de choix de paniers :math:`panier`, et des arbres contenant :math:`a_1, a_2, \ldots, a_n` fruits, dans le cas général, la probabilité de victoire est :

.. math::

   \begin{align}
   P\left(n, c, (a_1, a_2, \ldots, a_n)\right)
   &= \frac{1}{n+2}\times P\left(n, c-1, (a_1, a_2, \ldots, a_n)\right) \\
   &+ \sum_{i=1}^n\frac{1}{n+2}\times P\left(n, c-1, \left(a_1, a_2, \ldots, a_i-1, \ldots, a_n\right)\right) \\
   &+ \frac{1}{n+2}\times P\left(n, c-1, panier(a_1, a_2, \ldots, a_n)\right) \\
   \end{align}


Les cas particuliers sont les suivants :

- si :math:`n=0` (tous les fruits ont été cueillis), la probabilité est 1 (victoire) ;
- si :math:`c=0` (le corbeau est complet), la probabilité est 0 (défaite) ;
- si un arbre n'a plus de fruits, il est supprimé de la liste.

Cela donne le code suivant.

.. literalinclude:: ../jouets/verger/__init__.py
    :linenos:
    :pyobject: probabilite

Validité
--------

Nos calculs sont-ils valides ? Deux indices laissent penser que c'est le cas.

1. Premièrement, les calculs effectués avec le graphe probabiliste, et avec le programme, donnent le même résultat. Je n'ai pu comparer que pour les petites valeurs (le graphe probabiliste est assez petit), mais cela laisse supposer qu'ils sont aussi corrects pour des valeurs plus grandes.

2. Ensuite, le programme informatique donne une probabilité de victoire de 0,68, ce qui est égale aux valeurs trouvées ailleurs sur la toile (voir `ici <https://fr.wikipedia.org/w/index.php?title=Le_Verger_(jeu)&oldid=155808970#Probabilit%C3%A9s_de_gagner>`__ et `là <https://github.com/jhinrichsen/Obstgarten>`__ par exemple).

Ces indices ne sont pas des preuves, mais cela permet de supposer que les résultats est correct.

Quelques graphiques
===================

Le graphique suivant compare les probabilités de victoire des stratégies étudiées.

.. plot::

   from jouets.verger.graphiques import graphique_strategies
   graphique_strategies()

Le graphique suivant calcule, avec neuf corbeaux (comme dans le jeu de base), pour chaque nombre d'arbres et de fruits par arbres, la probabilité de victoire.

.. plot::

   from jouets.verger.graphiques import heatmap_probabilites
   heatmap_probabilites()

Le graphique suivant calcule, pour chaque nombre d'arbres, et de fruits par arbres, le plus petit nombre de corbeaux nécessaire pour que la joueuse ait plus d'une chance sur deux de gagner.

.. plot::

   from jouets.verger.graphiques import heatmap_equiprobabilites
   heatmap_equiprobabilites()

Programme
=========

.. argparse::
    :module: jouets.verger.__main__
    :func: analyse
    :prog: verger
