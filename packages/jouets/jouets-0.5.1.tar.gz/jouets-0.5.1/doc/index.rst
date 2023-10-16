..
   Copyright 2014-2017 Louis Paternault
   
   Cette œuvre de Louis Paternault est mise à disposition selon les termes de
   la licence Creative Commons Attribution - Partage dans les Mêmes Conditions
   4.0 International (CC-BY-SA). Le texte complet de la licence est disponible
   à l'adresse : http://creativecommons.org/licenses/by-sa/4.0/deed.fr

Documentation de Jouets
=======================

Ce dépôt contient en ensemble de programmes à connotation mathématique ou
algorithmique. Ce sont des idées qui m'ont trottées dans la tête, et dont je
n'ai pu me débarrasser qu'en les mettant en œuvre dans les programmes suivants.

Chacun de ces programmes a un intérêt mathématique, informatique, ou les deux.

Ils sont abondamment documentés, et sont fournis avec des tests. J'espère que
la lecture et la compréhension de leur code source est possible.

Si j'ai trouvé seul chacun des algorithmes présentés ici [#f1]_, je serais très
surpris si j'étais le premier à les avoir découvert, et, si, par le plus grand
des hasard, c'était le cas, je doute qu'ils soient une grande nouveauté pour la
communauté mathématique.

En revanche, rien sur ce site web n'a été `évalué par des pairs
<https://fr.wikipedia.org/wiki/%C3%89valuation_par_les_pairs>`__. Il est donc
probable qu'il contienne plus ou moins d'erreurs allant de l'étourderie à la
preuve d'une incompétence. À lire avec `esprit critique
<http://cortecs.org/>`__ !

Table des matières
------------------

.. toctree::
   :maxdepth: 1

   addition
   anagrammes
   aperitif
   attente
   azul
   bataille
   cellulaire
   chemin
   dobble
   egyptienne
   erathostene
   euler
   fractale
   horloge
   labyrinthe
   latex
   mafia
   microbit
   peste
   pygame
   sudoku
   traitementimage
   truchet
   verger

Modules et Classes
------------------

.. toctree::
   :maxdepth: 1

   api/anagrammes
   api/verger

Téléchargement et installation
------------------------------

Rendez vous sur `la page principale du projet
<http://framagit.org/spalax/jouets>`_ pour les instructions, et le
`changelog <https://framagit.org/spalax/jouets/blob/main/CHANGELOG.md>`_.

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. rubric:: Notes

.. [#f1] …ou du moins, si un des algorithmes n'est pas de moi, ça n'est pas conscient. En particulier :

    * ayant lu l'article `Modélisation mathématique d'un labyrinthe <http://fr.wikipedia.org/wiki/Mod%C3%A9lisation_math%C3%A9matique_d%27un_labyrinthe>`_ quelques semaines avant d'écrire :ref:`mon algorithme <labyrinthe>`, il est probable que j'ai oublié la source, mais que cet article a semé une idée qui a ensuite germé dans mon esprit ;
    * l'algorithme de recherche de solutions au :ref:`problème des apéritifs <aperitif>` est tellement naïf que je pense que n'importe qui ayant étudié un peu l'algorithmique arriverait au même algorithme que moi.
