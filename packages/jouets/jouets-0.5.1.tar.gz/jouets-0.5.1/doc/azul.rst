..
   Copyright 2019 Louis Paternault
   
   Cette œuvre de Louis Paternault est mise à disposition selon les termes de
   la licence Creative Commons Attribution - Partage dans les Mêmes Conditions
   4.0 International (CC-BY-SA). Le texte complet de la licence est disponible
   à l'adresse : http://creativecommons.org/licenses/by-sa/4.0/deed.fr

.. _azul:

***************************************
`azul` — Calcul du score maximal à Azul
***************************************

`Azul <https://www.trictrac.net/jeu-de-societe/azul>`__ est un jeu aussi intéressant à deux qu'à quatre joueurs. Puisque c'est un jeu d'optimisation, je me suis demandé quel était le score maximal qu'il est possible de réaliser.

.. contents::
  :depth: 1
  :local:

Un peu de dénombrement
======================

En tant qu'informaticien, ma première idée a été de tester toutes les combinaisons possibles. Il y a 25 cases à compléter, cela fait donc :math:`25!` ordres possibles, soit environ :math:`1,6\times10^{25}`. Tester toutes ces possibilités, sur un processeur à 1GHz qui testerait une combinaison par cycle (ce qui est *beaucoup* plus rapide que la réalité), cela prendrait (en années) : :math:`\frac{25!}{10^9\times60\times60\times24\times365}\approx 5\times10^8`, soit environ 500 millions d'années. Il va falloir être plus malin…

Beaucoup de ces combinaisons ne sont pas des combinaisons valides (car on continuerait à jouer *après* la fin de la partie, qui arrive dés qu'une ligne est complète) ; beaucoup de ces combinaisons, pour des raisons de symétrie, sont équivalentes. Il est donc possible de d'ignorer beaucoup de solutions, et de réduire le temps de calcul.

Mais il y a plus simple, grâce… aux mathématiques…

Mathématiques
=============

Une méthode *très* importante de résolution de problème est : simplifier ce problème complexe, pour en extraire un problème plus simple. Une fois ce problème plus simple résolu, cela permet de mieux comprendre le problème complexe pour le résoudre.

Dans ce cas, le problème plus simple que nous allons d'abord étudier est :

    Comment placer les tuiles sur *une seule ligne* pour obtenir un score maximal ?

La solution est : il ne faut laisser aucun trou, comme dans l'exemple suivant. Le score (de cette ligne, sans les bonus) est alors 15.

.. image:: azul/ligne.gif

Démontrons cette affirmation.

Commençons par donner un nom au fait qu'il n'y ait pas de trou : c'est la notion de `connexité <https://fr.wikipedia.org/wiki/Connexit%C3%A9_(math%C3%A9matiques)>`__, souvent utilisée en mathématiques.

.. proof:definition:: Connexe

   Une ligne (des tuiles sur une ligne) est dite *connexe* s'il n'y a pas de case vide entre deux tuiles.

.. proof:example::

   .. tikz:: Une ligne non connexe
      :libs: azul

       \fill (0, 0) rectangle (5, 1);
       \tuileA{0, 0}
       \tuileJ{1, 0}
       %\tuileR{2, 0}
       %\tuileN{3, 0}
       \tuileB{4, 0}

   .. tikz:: Une ligne connexe
      :libs: azul

       \fill (0, 0) rectangle (5, 1);
       %\tuileA{0, 0}
       %\tuileJ{1, 0}
       \tuileR{2, 0}
       \tuileN{3, 0}
       %\tuileB{4, 0}

.. proof:property::

   Placer les cinq tuiles d'une ligne en s'assurant que la ligne reste toujours connexe permet d'obtenir le score maximal de 15.

.. proof:proof::

   Démontrons ce théorème par récurrence.

   Définissons la suite :math:`u`, définie pour :math:`n\in\left[1;5\right]`, par : :math:`u_n` est le nombre maximal de points obtenus en plaçant :math:`n` tuiles sur une ligne.

   L'hypothèse de récurrence est double :

   - :math:`u_n=\sum\limits_{i=1}^ni` ;
   - le score maximal :math:`u_n` est atteint si à chaque étape, la ligne est connexe.

   Initialisation : Pour :math:`n=1`, la tuile ne rapporte qu'un point, donc :math:`u_1=1=\sum\limits_{i=1}^1i`, et la ligne est connexe.

   Supposons l'hypothèse de récurrence vraie pour l'entier :math:`n`. Nous avons donc une ligne à :math:`n` tuiles, réalisant le score maximal. Ajoutons une tuile de plus. Trois cas sont alors possibles.

   - La nouvelle tuile est isolée. Le score est alors :math:`u_{n+1}=u_{n}+1`. La ligne n'est alors pas connexe, mais nous verrons que ce cas est exclus.
   - La nouvelle tuile est adjacente à *une seule* autre tuile. D'après la relation de récurrence, les :math:`n` premières tuiles sont connexes, donc la nouvelle tuile rapporte :math:`n+1` points, et :math:`u_{n+1}=u_n+n+1`. Nous remarquons que la ligne est connexe.
   - La nouvelle tuile est adjacente à deux autres tuiles (une de chaque côté). Ce cas est exclus, car cela signifie qu'à l'étape précédente, la ligne n'était pas connexe.

   Ne restent que les deux premiers cas. Mais puisque :math:`n\geq1`, alors :math:`u_n+n+1>u_n+1`, et le score maximal est obtenu avec le second cas (en plaçant la tuile adjacente à une tuile déjà placée). Les deux hypothèses de récurrences sont alors vérifiées :

   - d'une part :math:`u_{n+1}=u_n+n+1=\sum\limits_{i=1}^ni+n+1=\sum\limits_{i=1}^{n+1}i` ;
   - d'autre part, à chaque étape, la ligne est connexe.

   L'hypothèse de récurrence est donc vérifiée, et elle est vraie pour :math:`n=5`, ce qui signifie que :

   - le score maximal est :math:`u_5=\sum\limits_{i=1}^5i=15` ;
   - à chaque étape, la ligne était connexe.


Nous avons réussi à déterminer le score maximal pour une ligne. Remarquons que la même chose s'applique à une colonne : le score maximal est 15, et il est possible de l'obtenir si à chaque étape, la colonne reste connexe.

Repassons maintenant au problème original : Quel est le score maximal pour l'ensemble de la grille ? Commençons par remarquer qu'il est possible de remplir toute la grille en s'assurant que chaque ligne et chaque colonne est toujours connexe.

.. proof:example::

   Deux exemples de remplissage de la grille de telle manière qu'à chaque étape, chaque ligne et chaque colonne est connexe.

   .. figure:: azul/maximal1.gif

   .. figure:: azul/maximal2.gif

.. proof:theorem::

   Le score maximal au jeu d'Azul est 245.

.. proof:proof::

   Nous avons montré que le score maximal rapporté par une ligne est 15, de même pour une colonne. Nous avons aussi montré que remplir la grille en s'assurant que chaque ligne et chaque colonne soit toujours connexe est possible. Donc, en admettant que le score maximal est atteint si la grille est complète (la démonstration est laissée au lecteur patient), c'est en remplissant intégralement la grille, avec chaque ligne et chaque colonne connexe à chaque étape, que le score maximal sera atteint. Le score est alors :

   ========================= ==== =======
   Construction des lignes   5×15 75
   Construction des colonnes 5×15 75
   Bonus des lignes          5×2  10
   Bonus des colonnes        5×7  35
   Bonus des couleurs        5×10 50
   **Total**                      **245**
   ========================= ==== =======

Programmation
=============

L'algorithme de calcul du score maximal est le plus simple de tous les algorithmes de ce site web.

.. literalinclude:: ../jouets/azul/__main__.py
   :pyobject: score_maximal

Blague à part, cet algorithme illustre qu'un des outil de l'informaticien, qu'il a en permanence devant lui, est un papier de brouillon et un crayon (je le répète sans cesse à mes élèves, sans trop de succès). Une architecte peut improviser une cabane dans les bois, mais pour construire une maison, elle aura besoin de papier et d'un crayon pour dessiner des plans, calculer des surfaces, des forces, des résistances ; de même, une informaticienne peut improviser des petits programmes, mais elle aura besoin de papier et d'un crayon pour planifier, gribouiller, calculer, pendant la réalisation d'un algorithme ou logiciel plus important.

Stratégie
=========

Ce score est atteignable *en théorie*, dans des conditions idéales, sans tuile cassée, à condition d'avoir un tirage parfait, et des adversaires pas très agressifs (voire aidant). Reflète-t-il une bonne stratégie dans un jeu en condition réelle ?

Je pense que oui : en suivant cette stratégie (éviter au maximum les trous), nous réussissons régulièrement à obtenir un score supérieur (voire bien supérieur) à 100.
