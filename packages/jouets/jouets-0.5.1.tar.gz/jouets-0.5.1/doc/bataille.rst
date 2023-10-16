..
   Copyright 2018 Louis Paternault
   
   Cette œuvre de Louis Paternault est mise à disposition selon les termes de
   la licence Creative Commons Attribution - Partage dans les Mêmes Conditions
   4.0 International (CC-BY-SA). Le texte complet de la licence est disponible
   à l'adresse : http://creativecommons.org/licenses/by-sa/4.0/deed.fr

*******************************************
`bataille` — Durée d'une partie de bataille
*******************************************

En ce moment, ma fille aime jouer à `Bata-waf <https://www.trictrac.net/jeu-de-societe/bata-waf>`__. C'est long et répétitif. Pour combler les temps morts pendant lesquels elle joue, compare, ramasse, ou mélange les cartes, je me suis demandé quel était la durée moyenne d'une partie. Le résultat est là.

Ce programme simule des parties de bataille (le jeu de carte) en mesurant la durée (en nombre de tours) de chaque partie. Il affiche le résultat sous la forme d'un tableau au format CSV (par exemple :download:`bataille/bataille-4-13-1000000.csv`, où chaque ligne est de la forme ``durée, effectif``), ou sous la forme d'un graphique, ou il calcule des statistiques sur les durées des parties.

.. contents::
   :local:
   :depth: 2

Règles
======

Voici les règles utilisées dans cette simulation.

* Les cartes (4 couleurs de 13 cartes) sont mélangées, et réparties équitablement entre les deux joueuses.

* Chaque tour se déroule de la manière suivante.

  1. À chaque tour, chacune des joueuses pioche la carte située sur le dessus de son paquet.
  2. Elles comparent leur carte.
      * Si les cartes sont de valeur différente, la joueuse ayant la carte la plus grande remporte le tour.
      * Si les cartes sont de même valeur, il y a une bataille : les joueuses posent chacun sur la table, face cachée, une nouvelle carte, et piochent encore une carte dont ils comparent la valeur en revenant à l'étape 2 (il peut y avoir à nouveau une bataille).
  3. Quand les batailles sont résoluées, la joueuse remportant le tour ramasse les cartes des deux joueuses, et les place dans un ordre aléatoire en bas de son tas de carte.
  4. Retour à l'étape 1.

* La partie se termine lorsqu'à n'importe quelle phase du jeu, une joueuse doit piocher, mais n'a plus de cartes.

Remarquons un cas particulier : si les deux joueuses ont le même nombre de carte, et enchaînent bataille après bataille, il peut arriver un cas où les deux joueuses, en même temps, sont à cours de cartes à piocher. Dans ce cas là, la partie s'arrête et il y a match nul (même si cela est sans importance pour cette simulation, où seul le nombre de tours compte).

État de l'art
=============

En 1995, Jean-Paul Delahay et Philippe Mathieu ont publié une analyse de la partie de bataille [Delahay1995]_. Leurs règles diffèrent des miennes de deux manières :

- en cas de bataille, ils ne placent pas de cartes face cachées sur la carte précédente ;
- en fin de plis, les cartes sont remises sous le tas de la joueuse gagnante dans un ordre bien précis (alors que dans ma version, l'ordre est aléatoire).

Ils s'intéressent surtout aux parties nulles et infinies, cas que j'ignore ici :

- Je ne m'intéresse pas aux parties nulles : si une partie est nulle, elle est terminée, et c'est tout ce qui m'importe.
- Ma règle mettant en jeu le hasard, les parties infinies sont impossibles.

Selon leurs calculs (ou simulations), les parties nulles ou infinies sont très rares : environ 2% de chaque pour 3 cartes de 4 couleurs différentes, ou 0,18% de parties nulles et 0,027% de parties infinies pour un jeu de 4 cartes de 4 couleurs. Nous devrions donc trouver des résultats similaires, même si j'ignore ces cas-là.

Voir dans l'analyse :ref:`une comparaison de nos résultats <comparaison-delahay>`.

Analyses
========

J'ai analysé de deux manières différentes ce jeu : avec l'informatique, et avec les mathématiques.

.. toctree::
   :maxdepth: 2
   :numbered:

   bataille/informatique
   bataille/mathematique

Statistiques et Données brutes
==============================

.. toctree::
   :maxdepth: 1
   :numbered:

   bataille/statistiques
   bataille/donnees

Notes et Références
===================

.. [Delahay1995] Jean-Paul Delahay et Philippe Mathieu, La bataille, enfin analysée. http://www.lifl.fr/%7Ejdelahay/pls/1995/030.pdf
