..
   Copyright 2018 Louis Paternault
   
   Cette œuvre de Louis Paternault est mise à disposition selon les termes de
   la licence Creative Commons Attribution - Partage dans les Mêmes Conditions
   4.0 International (CC-BY-SA). Le texte complet de la licence est disponible
   à l'adresse : http://creativecommons.org/licenses/by-sa/4.0/deed.fr

.. _pygame:

********************************
`pygame` — Quelques jeux simples
********************************

Ce module contient quelques jeux réalisés pour tester ce que je peux faire faire à mes élèves en ICN et ISN [#f1]_ en utilisant la bibliothèque `pygame <http://pygame.org>`__. Ceci explique que :

- seule la mécanique du jeu est implémentée, mais pas un tas de choses qu'il faudrait réaliser si je voulais distribuer les jeux, par exemple, en vrac :

    - de jolis menus ;
    - la possibilité de mettre en pause ;
    - la possibilité de recommencer une partie sans quitter le programme ;
    - des graphismes plus jolis ;
    - du son ;
    - plusieurs niveau de difficulté ;
    - etc.

- ils n'utilisent que des concepts de programmation aussi simples que possibles (aucune nouvelle classe n'est définie, par exemple).

Je me suis permi quelques entorses à cette règle :

- des bouts de code que j'utilise dans plusieurs jeux ont été rassemblés dans un module commun (ce que je ne ferais sans doute pas avec des élèves, ou en tout cas pas dans un premier temps) ;
- je me suis permi d'utiliser des ensembles ou la compréhension de listes lorsque cela me simplifiait vraiment la tâche.

Chacun des jeux teste une fonctionnalité particulière de pygame.

J'ai été surpris de la facilité avec laquelle il est possible de réaliser de petits jeux. Par contre, il consomment énormément de ressources processeur, et j'ignore pourquoi.

Jouer
=====

Pour exécuter les jeux :

- si le module a été installé avec pip, utiliser, à la ligne de commande, le nom du jeu précédé de `pg` (comme `pygame`) : par exemple `pgserpent` pour le jeu du serpent ;
- si le module a simplement été téléchargé ou cloné avec `git`, il contient des binaires dans le dossier `bin`.

Liste des jeux
==============

Slalom
------

.. figure:: _images/pygame/slalom.png
  :width: 400
  :align: center

  Capture d'écran.

Réalisé pour tester la manipulation de la souris.

Sans doute le jeu le plus amusant : il est très simple au début, la difficulté est progressive, et lorsque l'on perd, il y a cette frustration et ce sentiment de « ma défaite n'était pas injuste, mais je pense que j'aurais pu aller encore un peu plus loin ».

Labyrinthe
----------

.. figure:: _images/pygame/labyrinthe.png
  :width: 400
  :align: center

  Capture d'écran.

Réalisé pour tester la fonction `event.wait() <http://www.pygame.org/docs/ref/event.html#pygame.event.wait>`__ de pygame.

Le personnage ne se déplace pas en continue lorsqu'une des touches de direction reste appuyée : il faut presser plusieurs fois la touche pour le faire avancer. C'est un défaut, mais le corriger impliquerait de ne plus utiliser la fonction `event.wait()` pour laquelle il a été écrit.

Serpent
-------

.. figure:: _images/pygame/serpent.png
  :width: 400
  :align: center

  Capture d'écran.

Réalisé pour tester la réalisation de ce classique que tout le monde connait.

Il ne donne pas une impression de fluidité.

Envahisseurs
------------

.. figure:: _images/pygame/envahisseurs.png
  :width: 400
  :align: center

  Capture d'écran.

Réalisé pour tester la mise en œuvre de la méthode d'Euler.

Il est trop facile : une bonne stratégie consiste à tirer en continu quasiment à la verticale, afin de créer une barrière de boulets difficilement franchissable.

Les collisions sont testées de manière très approximatives. Une manière plus propre serait d'utiliser les `sprites <https://www.pygame.org/docs/tut/SpriteIntro.html>`__. Peut-être que je ré-écrierai ce jeu un jour en les utilisant.

.. rubric:: Notes

.. [#f1] Informatique et Création Numérique, et Informatique et Sciences du Numérique.
