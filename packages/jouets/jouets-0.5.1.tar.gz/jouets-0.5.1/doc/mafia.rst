*************************************************
`mafia` — Probabilités de victoire au jeu *mafia*
*************************************************

.. currentmodule:: jouets.mafia

Les `Loups-Garous de Thiercelieux <http://www.loups-garous.com/>`__ est un succès commercial récent dans le monde du jeu de société. C'est une adaptation d'un jeu plus vieux, `Mafia <https://fr.wikipedia.org/wiki/Mafia_(jeu)>`__. J'ai pas mal joué à Mafia étant jeune, et avec du recul, je n'aime pas ce jeu : il favorise les beaux parleurs, et les perdants sont peu à peu exclus du jeu, et ne sont plus que spectateurs [#colo]_. Les loups-garous ajoutent à ce jeu beaucoups de personnage, ce qui rend, à mon avis, le jeu encore moins amusant : les défauts déjà évoqués restent, et en plus, le jeu est allongé (beaucoup plus d'actions prennent place la nuit) sans pour autant être plus intéressant.

Néanmoins, je me suis intéressé aux probabilités de victoire.

Règles
======

Un maître du jeu anime la partie. Les autres joueurs se voient attribuer un rôle secret, de manière aléatoire : ils peuvent être mafieux, innocents ou détectives. Ils jouent la population d'une ville que la mafia veut conquérir. Le but des mafieux est de prendre le pouvoir en éliminant les autres personnages ; le but des innocents et détectives, qui sont alliés, est de se débarrasser des mafieux.

Le jeu alterne jour (où les joueurs discutent librement) et nuit (où les joueurs ferment les yeux et ne les ouvrent que sur ordre du maître du jeu), et commence la nuit.

* La nuit, le maître du jeu demande aux mafieux de se réveiller. En silence, ils s'accordent sur un joueur à éliminer. Puis ils se rendorment. Les détectives, s'il en reste, se réveillent, et se mettent d'accord sur un joueur à interroger. Puis ils se rendorment.
* Au matin, le maître du jeu fait le bilan de la nuit : il désigne le joueur éliminé par les mafieux. Ce joueur est éliminé, et  son identité est révélée. Puis le maître annonce le résultat de l'action des détectives : s'ils ont désigné un mafieux, celui-ci est éliminé et son identité révélée ; s'ils ont désigné un innocent, le maître du jeu annonce simplement que les détectives n'ont pas réussi à attraper de mafieux cette nuit-là, sans révélé qui a été interrogé.
* Le jour, les joueurs discutent pour éliminer un joueur. Cela se fait au hasard, selon les indices entendus la nuit (« J'ai entendu du bruit de ce côté-là, donc je pense qu'Untel est un mafieux »), ou selon le comportement des joueurs (« Untel a défendu Untel hier, alors que ce dernier était mafieux. Il est donc sans doute aussi mafieux »). Le vote se fait généralement à la majorité, et le joueur désigné est éliminé, et son identité révélée.

Le jeu se termine quand il n'y a plus de mafieux (les innocents et détectives ont gagné) ou lorsque les mafieux constituent la moitié des joueurs restants.

Le but des mafieux est évidemment d'essayer, la nuit, de tuer les détectives en premier, qui constituent un avantage pour les innocents ; et le jour, de se protéger les uns les autres tout en étant discrets pour ne pas être démasqués. Le but des innocents et détectives est de repérer des comportements suspects pour éliminer les mafieux.

Une dernière remarque concernant la nuit : les actions des mafieux et détectives sont considérées simultanées.

* Si les mafieux tuent un détective, celui-ci ce réveille tout de même dans la même nuit pour désigner un mafieux à interroger. Ce n'est qu'au matin qu'il apprend qu'il a été tué.
* Même s'il ne reste qu'un détective et qu'il est tué par les mafieux, il est tout de même réveillé pour interroger un suspect. Il peut très bien tuer un mafieux. C'est alors au maître du jeu de romancer l'apparente incohérence (« Tombé dans une lâche embuscade, le détective eut juste le temps d'abattre un de ses assaillants avant de mourir à son tour. »).

La question importante est alors : Quel doit être le nombre de mafieux et de détectives pour que le jeu soit équilibré ?

Calcul des probabilités
=======================

Pour calculer les probabilités de victoire, on suppose que tous les choix sont faits au hasard. Par exemple, si un jour, il reste en jeu 3 mafieux, 1 détective et 16 innocents, on considère qu'il y a 3 chances sur 20 de tuer un mafieux, 1 chance sur 20 de tuer un détective, et 16 chances sur 20 de tuer un innocent.

Algorithme
----------

Le calcul est fait ici en utilisant une algorithme récursif. Une analyse mathématique a été réalisée (entre autres) par Erlin Yao [Yao]_. Un résumé des études, et des liens vers d'autres études peut être trouvé sur la `page Wikipédia du jeu <https://en.wikipedia.org/wiki/Mafia_(party_game)#Game_theory>`__.

Cet algorithme n'a rien de très original.

* Les cas de victoire ou défaite certaines sont traités au début de l'algorithme (lignes 8 et 9 pour ``proba_soir``, lignes 8 à 11 pour ``proba_matin``).
* Les appels récursifs sont ensuite traités. Tous les cas sont étudiés. Par exemple, pour ``proba_matin``, il est possible de tuer un mafieux, un innocent ou un détective, donc, en notant :math:`P_m(m, i, d)` (respectivement :math:`P_s(m, i, d)`) la probabilité de victoire des innocents si le matin (respectivement le soir) il reste :math:`m` mafieux, :math:`i` innocents et :math:`d` détectives, alors la `formule des probabilités totales <https://fr.wikipedia.org/wiki/Formule_des_probabilit%C3%A9s_totales>`__ nous permet d'affirmer :

  .. math::

    P_m(m, i, d) =
      \frac{m}{m+i+d} P_s(m-1, i, d) +
      \frac{i}{m+i+d} P_s(m, i-1, d) +
      \frac{d}{m+i+d} P_s(m, i, d-1)

  Pour :math:`P_s(m, i, d)`, la même formule est utilisée, mais elle est un peu plus compliquée, puisque les mafieux et les détectives (s'il en reste) peuvent tuer, donc il y a plus de cas à traiter.

Notons que la formule ci-dessus (l'application de la formule des probabilités totales) n'est valide que si il reste en jeu à la fois des mafieux, des innocents et des détectives. Plusieurs formules devraient être utilisées pour prendre en compte toutes ces possibilités. Nous verrons :ref:`à la partie suivante <argumentspositifs>` la méthode utilisées pour ne pas avoir à s'occuper de cela.

.. autofunction:: proba_soir

.. literalinclude:: ../jouets/mafia/__init__.py
    :linenos:
    :pyobject: proba_soir

.. autofunction:: proba_matin

.. literalinclude:: ../jouets/mafia/__init__.py
    :linenos:
    :pyobject: proba_matin

Optimisations
-------------

Deux optimisations permettent de rendre le code plus clair et plus efficace.

.. _argumentspositifs:

Clarté du code
^^^^^^^^^^^^^^

Comme dit précédemment, plusieurs cas devraient être pris en compte pour calculer la probabilité de victoire le matin, selon la présence ou non d'innoncents et de détectives (les mafieux sont forcément présents, sans quoi les innocents gagnent avec une probabilité 1, et cette partie du programme n'est pas exécutée). Le code devrait ressembler à quelque chose comme ::

  def proba_matin(mafieux, innocents, detectives):
      if mafieux == 0:
          return 1.0
      if mafieux >= innocents + detectives:
          return 0.0
      total = mafieux + innocents + detectives
      proba = mafieux/total * proba_soir(mafieux-1, innocents, detectives)
      if innocents > 0:
          proba += innocents/total * proba_soir(mafieux, innocents-1, detectives)
      if detectives > 0:
          proba += detectives/total * proba_soir(mafieux, innocents, detectives-1)
      return proba

Ça n'est pas grand chose, mais une astuce permet d'éviter cela.

Si nous appelons la fonction :func:`proba_soir` avec les arguments ``proba_soir(mafieux=2, innocents=4, detectives=0)``, lors du calcul de la probabilité, nous allons calculer à un moment donné :math:`\frac{detectives}{total}P_m(mafieux, innocents, detectives-1)`, soit :math:`\frac{0}{6}P_m(2, 4, -1)`. Le membre de droite de la multiplication (:math:`P_m(\ldots)`) n'a aucun sens puisque le nombre de détectives est négatif. Mais puisque le membre de gauche est nul, on pourrait considérer que ça n'est pas grave, puisque le produit est de toutes manières nul. Nous pourrions donc ajouter une règle *« Une multiplication de 0 par une probabilité qui n'a pas de sens a un sens et est égale à zéro. »* En étudiant soigneusement notre code, nous voyons qu'une telle règle produit un résultat correct. Reste à la mettre en œuvre.

Les deux fonctions :func:`proba_matin` et :func:`proba_soir` sont `décorées <http://gillesfabio.com/blog/2010/12/16/python-et-les-decorateurs/>`__ par le décorateur :func:`argumentspositifs`. Son effet est : si l'une de ces fonctions est appelée avec un de ses arguments négatifs, alors elle renvoit 0. Ainsi, un appel qui n'a pas de sens (par exemple :math:`P_m(2, 4, -1)`) renvoit une valeur, qui est de toutes manières ignorée puisqu'elle est multipliée par zéro, et le résultat est cohérent.

Complexité algorithmique
^^^^^^^^^^^^^^^^^^^^^^^^

La seconde optimisation est beaucoup plus intéressante.

Supposons qu'un matin, il reste en jeu 2 mafieux, 1 détective et 6 innocents. Il est possible que les prochains morts, dans cet ordre, soient un mafieux, un détective, un innocent, ou alors un détective, un innocent, un mafieux, ou encore un innocent, un détective, un mafieux, etc. Dans tous ces cas, à un moment donné, nous allons calculer :math:`P_s(1, 0, 5)`. Avec une implémentation naïve (qui est celle décrite jusqu'ici), cette probabilité est calculée plusieurs fois, et cela est de pire en pire au fur des récursions.

Pour éviter cela, les fonctions :func:`proba_soir` et :func:`proba_matin` sont décorées avec le décorateur `lru_cache <https://docs.python.org/3/library/functools.html#functools.lru_cache>`__. L'effet est que, chaque fois que l'une de ces fonctions est appelée, si elle a déjà été appelée avec les mêmes arguments, le résultat précédent est renvoyé sans exécuter la fonction ; sinon, la fonction est exécutée normalement, et le résultat est stocké pour une utilisation future.

Gain théorique
""""""""""""""

Sur le plan théorique, d'après un calcul `à l'arrache <http://www.la-rache.com/>`__, l'utilisation de ce décorateur transforme notre algorithme de `complexité exponentielle <https://fr.wikipedia.org/wiki/NP_(complexit%C3%A9)>`__ en un algorithme de `complexité polynomiale <https://fr.wikipedia.org/wiki/P_(complexit%C3%A9)>`__ (de degré 3). C'est une *énorme* amélioration.

Gain pratique
"""""""""""""

Sur le plan pratique, j'ai calculé avec :mod:`timeit` la durée de calcul de la probabilité de victoire d'un jeu à 4 mafieux, 4 innoncents et 4 détectives (soit 12 joueurs en tout).

.. code-block:: sh

  # Sans `lru_cache`
  $ python -m timeit "from jouets.mafia.__init__ import proba_soir; proba_soir(4 4 4)"
  10 loops best of 3: 21 msec per loop

  # Avec `lru_cache`
  $ python -m timeit "from jouets.mafia.__init__ import proba_soir; proba_soir(4 4 4)"
  1000000 loops best of 3: 1.17 usec per loop

Le résultat est sans appel. Avec cette optimisation, le calcul est effectué *20000* fois plus rapidement que sans.

Cette optimisation permet aussi de calculer en quelques microsecondes des probabilités de parties à 1000 joueurs. Sans cette optimisation, j'ai interrompu le programme sans avoir ma réponse au bout de dix minutes…

Usage des programmes
====================

Le programme livré avec ce module permet de calculer la probabilité de victoire des innocents lors d'une partie.

.. argparse::
    :module: jouets.mafia.__main__
    :func: analyse
    :prog: mafia

D'autres programmes, ne pouvant être appelés que par le nom de leur module python (``python3 -m jouets.mafia.equilibre ARGUMENTS``) plutôt qu'un binaire sont disponibles, et ont été utilisés pour générer les tableaux ci-dessous.

Probabilité de victoire des innocents
=====================================

En fonction du nombre de joueurs et de mafieux, pour un nombre de détectives fixé.

Aucun détectives
----------------

Obtenu avec la commande :

.. code-block:: sh

  python -m jouets.mafia.probadetective --detectives 0 --players 20

+-------------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| Mafieux \ Joueurs | 2      | 3      | 4      | 5      | 6      | 7      | 8      | 9      | 10     | 11     | 12     | 13     | 14     | 15     | 16     | 17     | 18     | 19     | 20     |
+-------------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| 0                 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
+-------------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| 1                 | 0.0%   | 0.0%   | 33.3%  | 25.0%  | 46.7%  | 37.5%  | 54.3%  | 45.3%  | 59.4%  | 50.8%  | 63.1%  | 54.9%  | 65.9%  | 58.1%  | 68.2%  | 60.7%  | 70.0%  | 62.9%  | 71.6%  |
+-------------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| 2                 |        | 0.0%   | 0.0%   | 0.0%   | 13.3%  | 8.3%   | 22.9%  | 15.6%  | 29.8%  | 21.6%  | 35.2%  | 26.4%  | 39.5%  | 30.5%  | 43.0%  | 33.9%  | 46.0%  | 36.9%  | 48.5%  |
+-------------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| 3                 |        |        | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 5.7%   | 3.1%   | 11.4%  | 6.9%   | 16.5%  | 10.5%  | 20.8%  | 14.0%  | 24.5%  | 17.1%  | 27.8%  | 19.9%  | 30.7%  |
+-------------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| 4                 |        |        |        | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 2.5%   | 1.2%   | 5.8%   | 3.1%   | 9.1%   | 5.2%   | 12.2%  | 7.4%   | 15.1%  | 9.6%   | 17.8%  |
+-------------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| 5                 |        |        |        |        | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 1.2%   | 0.5%   | 2.9%   | 1.5%   | 5.0%   | 2.6%   | 7.1%   | 4.0%   | 9.2%   |
+-------------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| 6                 |        |        |        |        |        | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.5%   | 0.2%   | 1.5%   | 0.7%   | 2.7%   | 1.3%   | 4.1%   |
+-------------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| 7                 |        |        |        |        |        |        | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.2%   | 0.1%   | 0.8%   | 0.3%   | 1.5%   |
+-------------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| 8                 |        |        |        |        |        |        |        | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.1%   | 0.0%   | 0.4%   |
+-------------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| 9                 |        |        |        |        |        |        |        |        | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.1%   |
+-------------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| 10                |        |        |        |        |        |        |        |        |        | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   |
+-------------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+

Le tableau se lit comme suit. Par exemple, le nombre 15,6 % dans la ligne 2 et la colonne 9 signifie : « À 9 joueurs, avec 0 détectives et 2 mafieux, la probabilité que les innocents gagne est 15,6 %. »

Un seul détective
-----------------

Obtenu avec la commande :

.. code-block:: sh

  python -m jouets.mafia.probadetective --detectives 1 --players 20

+-------------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| Mafieux \ Joueurs | 2      | 3      | 4      | 5      | 6      | 7      | 8      | 9      | 10     | 11     | 12     | 13     | 14     | 15     | 16     | 17     | 18     | 19     | 20     |
+-------------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| 0                 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
+-------------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| 1                 | 100.0% | 50.0%  | 70.4%  | 57.8%  | 71.6%  | 63.1%  | 73.9%  | 66.9%  | 75.9%  | 69.7%  | 77.6%  | 71.9%  | 79.0%  | 73.6%  | 80.2%  | 75.1%  | 81.2%  | 76.4%  | 82.1%  |
+-------------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| 2                 |        | 0.0%   | 0.0%   | 27.8%  | 32.2%  | 40.3%  | 42.9%  | 46.1%  | 49.1%  | 50.0%  | 53.4%  | 53.2%  | 56.7%  | 55.7%  | 59.3%  | 57.9%  | 61.5%  | 59.7%  | 63.3%  |
+-------------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| 3                 |        |        | 0.0%   | 0.0%   | 0.0%   | 12.2%  | 19.0%  | 25.5%  | 28.4%  | 32.2%  | 34.4%  | 36.8%  | 38.9%  | 40.2%  | 42.4%  | 43.0%  | 45.3%  | 45.4%  | 47.7%  |
+-------------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| 4                 |        |        |        | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 6.1%   | 12.2%  | 16.3%  | 19.7%  | 22.5%  | 25.0%  | 27.0%  | 29.0%  | 30.4%  | 32.3%  | 33.3%  | 35.1%  |
+-------------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| 5                 |        |        |        |        | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 3.7%   | 7.9%   | 11.0%  | 13.8%  | 16.2%  | 18.3%  | 20.1%  | 21.9%  | 23.3%  | 24.9%  |
+-------------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| 6                 |        |        |        |        |        | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 2.5%   | 5.3%   | 7.7%   | 9.9%   | 11.9%  | 13.6%  | 15.2%  | 16.7%  |
+-------------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| 7                 |        |        |        |        |        |        | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 1.6%   | 3.7%   | 5.5%   | 7.2%   | 8.8%   | 10.2%  |
+-------------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| 8                 |        |        |        |        |        |        |        | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 1.1%   | 2.6%   | 4.0%   | 5.3%   |
+-------------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| 9                 |        |        |        |        |        |        |        |        | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.8%   | 1.9%   |
+-------------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| 10                |        |        |        |        |        |        |        |        |        | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   | 0.0%   |
+-------------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+

Équilibre
=========

Pour un nombre de joueurs donnés, calcule le nombre de détectives et mafieux pour que le jeu soit le plus équilibré possible (que la probabilité de victoire soit aussi proche de *50 %* que possible). Puisque l'égalité est rarement atteinte, deux configurations sont affichées : celle la plus équilibrée possible, avec avantage aux innocents (excés) ; et celle la plus équilibrée possible, avec avantage aux mafieux (défaut).

Aucun détectives
----------------

Obtenu avec la commande :

.. code-block:: sh

  python -m jouets.mafia.equilibre --detectives 0 --players :30

+---------+-----------------+-----------------+-----------------+-----------------+-----------------+-----------------+----------------+-----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+
| Joueurs | 2               | 3               | 4               | 5               | 6               | 7               | 8              | 9               | 10             | 11             | 12             | 13             | 14             | 15             | 16             | 17             | 18             | 19             | 20             | 21             | 22             | 23             | 24             | 25             | 26             | 27             | 28             | 29             | 30             |
+---------+-----------------+-----------------+-----------------+-----------------+-----------------+-----------------+----------------+-----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+
| Défaut  | 0.0% (2m, 0d)   | 0.0% (3m, 0d)   | 33.3% (1m, 0d)  | 25.0% (1m, 0d)  | 46.7% (1m, 0d)  | 37.5% (1m, 0d)  | 22.9% (2m, 0d) | 45.3% (1m, 0d)  | 29.8% (2m, 0d) | 21.6% (2m, 0d) | 35.2% (2m, 0d) | 26.4% (2m, 0d) | 39.5% (2m, 0d) | 30.5% (2m, 0d) | 43.0% (2m, 0d) | 33.9% (2m, 0d) | 46.0% (2m, 0d) | 36.9% (2m, 0d) | 48.5% (2m, 0d) | 39.5% (2m, 0d) | 33.2% (3m, 0d) | 41.8% (2m, 0d) | 35.5% (3m, 0d) | 43.9% (2m, 0d) | 37.5% (3m, 0d) | 45.7% (2m, 0d) | 39.4% (3m, 0d) | 47.4% (2m, 0d) | 41.1% (3m, 0d) |
+---------+-----------------+-----------------+-----------------+-----------------+-----------------+-----------------+----------------+-----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+
| Excès   | 100.0% (0m, 0d) | 100.0% (0m, 0d) | 100.0% (0m, 0d) | 100.0% (0m, 0d) | 100.0% (0m, 0d) | 100.0% (0m, 0d) | 54.3% (1m, 0d) | 100.0% (0m, 0d) | 59.4% (1m, 0d) | 50.8% (1m, 0d) | 63.1% (1m, 0d) | 54.9% (1m, 0d) | 65.9% (1m, 0d) | 58.1% (1m, 0d) | 68.2% (1m, 0d) | 60.7% (1m, 0d) | 70.0% (1m, 0d) | 62.9% (1m, 0d) | 71.6% (1m, 0d) | 64.8% (1m, 0d) | 50.7% (2m, 0d) | 66.4% (1m, 0d) | 52.6% (2m, 0d) | 67.8% (1m, 0d) | 54.4% (2m, 0d) | 69.0% (1m, 0d) | 55.9% (2m, 0d) | 70.1% (1m, 0d) | 57.3% (2m, 0d) |
+---------+-----------------+-----------------+-----------------+-----------------+-----------------+-----------------+----------------+-----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+

Le tableau se lit comme suit. Par exemple, la colonne 10 signifie :

- à 10 joueurs, pour un jeu le plus équilibré possible avec avantage aux mafieux, il faut 2 mafieux et 0 détectives (la proba de victoire est alors 29,8 %) ;
- à 10 joueurs, pour un jeu le plus équilibré possible avec avantage aux innocents, il faut 1 mafieux et 0 détectives (la proba de victoire est alors 59,4 %).

Un ou deux détectives
---------------------

Obtenu avec la commande :

.. code-block:: sh

  python -m jouets.mafia.equilibre --detectives 1:2 --players :30

+---------+-----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+
| Joueurs | 2               | 3              | 4              | 5              | 6              | 7              | 8              | 9              | 10             | 11             | 12             | 13             | 14             | 15             | 16             | 17             | 18             | 19             | 20             | 21             | 22             | 23             | 24             | 25             | 26             | 27             | 28             | 29             | 30             |
+---------+-----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+
| Défaut  | 0.0% (2m, 0d)   | 50.0% (1m, 1d) | 0.0% (3m, 1d)  | 27.8% (2m, 1d) | 47.2% (2m, 2d) | 40.3% (2m, 1d) | 42.9% (2m, 1d) | 46.1% (2m, 1d) | 49.1% (2m, 1d) | 44.5% (3m, 2d) | 46.3% (3m, 2d) | 48.9% (3m, 2d) | 38.9% (3m, 1d) | 40.2% (3m, 1d) | 42.4% (3m, 1d) | 43.0% (3m, 1d) | 45.3% (3m, 1d) | 45.4% (3m, 1d) | 47.7% (3m, 1d) | 47.5% (3m, 1d) | 49.8% (3m, 1d) | 49.4% (3m, 1d) | 49.6% (4m, 2d) | 40.8% (5m, 2d) | 41.8% (5m, 2d) | 42.7% (5m, 2d) | 43.6% (5m, 2d) | 44.3% (5m, 2d) | 45.1% (5m, 2d) |
+---------+-----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+
| Excès   | 100.0% (0m, 1d) | 50.0% (1m, 1d) | 70.4% (1m, 1d) | 51.9% (2m, 2d) | 71.6% (1m, 1d) | 57.6% (2m, 2d) | 55.6% (2m, 2d) | 60.7% (2m, 2d) | 60.1% (2m, 2d) | 50.0% (2m, 1d) | 53.4% (2m, 1d) | 53.2% (2m, 1d) | 50.0% (3m, 2d) | 52.0% (3m, 2d) | 53.0% (3m, 2d) | 54.4% (3m, 2d) | 55.3% (3m, 2d) | 56.4% (3m, 2d) | 57.3% (3m, 2d) | 58.1% (3m, 2d) | 59.0% (3m, 2d) | 59.6% (3m, 2d) | 51.7% (3m, 1d) | 50.4% (4m, 2d) | 51.3% (4m, 2d) | 51.9% (4m, 2d) | 52.8% (4m, 2d) | 53.3% (4m, 2d) | 54.1% (4m, 2d) |
+---------+-----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+

Nombre illimité de détectives
-----------------------------

Obtenu avec la commande :

.. code-block:: sh

  python -m jouets.mafia.equilibre --detectives : --players :30

+---------+-----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+-----------------+------------------+----------------+------------------+------------------+----------------+
| Joueurs | 2               | 3              | 4              | 5              | 6              | 7              | 8              | 9              | 10             | 11             | 12             | 13             | 14             | 15             | 16             | 17             | 18             | 19             | 20             | 21             | 22             | 23             | 24             | 25              | 26               | 27             | 28               | 29               | 30             |
+---------+-----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+-----------------+------------------+----------------+------------------+------------------+----------------+
| Défaut  | 0.0% (2m, 0d)   | 50.0% (1m, 1d) | 33.3% (1m, 0d) | 27.8% (2m, 1d) | 47.2% (2m, 2d) | 40.3% (2m, 1d) | 45.4% (3m, 3d) | 48.0% (3m, 3d) | 49.5% (4m, 5d) | 44.5% (3m, 2d) | 48.2% (4m, 4d) | 48.9% (3m, 2d) | 46.7% (6m, 7d) | 47.6% (5m, 5d) | 49.5% (5m, 5d) | 49.6% (4m, 3d) | 48.1% (7m, 8d) | 49.0% (6m, 6d) | 49.2% (5m, 4d) | 48.5% (8m, 9d) | 49.8% (3m, 1d) | 50.0% (7m, 7d) | 49.8% (6m, 5d) | 50.0% (9m, 10d) | 49.5% (8m, 8d)   | 49.9% (5m, 3d) | 49.8% (10m, 11d) | 49.2% (9m, 9d)   | 49.8% (6m, 4d) |
+---------+-----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+-----------------+------------------+----------------+------------------+------------------+----------------+
| Excès   | 100.0% (0m, 0d) | 50.0% (1m, 1d) | 70.4% (1m, 1d) | 51.9% (2m, 2d) | 66.4% (2m, 3d) | 57.6% (2m, 2d) | 54.3% (1m, 0d) | 60.2% (3m, 4d) | 52.4% (3m, 3d) | 50.0% (2m, 1d) | 53.4% (2m, 1d) | 50.2% (4m, 4d) | 50.0% (3m, 2d) | 52.0% (3m, 2d) | 51.5% (6m, 7d) | 51.5% (5m, 5d) | 51.1% (4m, 3d) | 50.7% (7m, 8d) | 50.6% (6m, 6d) | 50.4% (5m, 4d) | 50.3% (8m, 9d) | 51.7% (8m, 9d) | 51.2% (7m, 7d) | 50.4% (4m, 2d)  | 51.0% (11m, 13d) | 50.6% (8m, 8d) | 50.2% (7m, 6d)   | 50.5% (12m, 14d) | 50.2% (9m, 9d) |
+---------+-----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+----------------+-----------------+------------------+----------------+------------------+------------------+----------------+

Notes et Références
===================

.. [#colo] Pour une version encore plus mauvaise, jouez à ce jeu durant une veillée (en colonie de vacances par exemple), en ajoutant comme règle que les perdants doivent aller se coucher. À l'exclusion symbolique (le perdant ne joue plus et regarde les autres s'amuser), on ajoute l'exclusion physique : le perdant quitte la partie, et laisse les autres s'amuser sans lui.
.. [Yao] Erlin Yao, A Theoretical Study of Mafia Games. https://arxiv.org/abs/0804.0071
