..
   Copyright 2014-2020 Louis Paternault
   
   Cette œuvre de Louis Paternault est mise à disposition selon les termes de
   la licence Creative Commons Attribution - Partage dans les Mêmes Conditions
   4.0 International (CC-BY-SA). Le texte complet de la licence est disponible
   à l'adresse : http://creativecommons.org/licenses/by-sa/4.0/deed.fr

*******************************************************
`erathostene` — Crible d'Érathostène optimisé en espace
*******************************************************

Le `crible d'Érathostène <http://fr.wikipedia.org/wiki/Crible_d'Érathostène>`_
est un algorithme permettant d'énumérer tous les nombres premiers inférieurs à
un certain nombre :math:`N`. Cette version l'améliore suivant deux aspects :

#. Le nombre maximal n'a pas a être précisé au départ : les nombres premiers
   sont énumérés tant que l'utilisateur n'arrête pas le programme.
#. La mémoire nécessaire est linéaire en le nombre de nombres premiers trouvés,
   et non pas en le plus grand nombre premier. La mémoire nécéssaire `est donc
   <http://fr.wikipedia.org/wiki/Fonction_de_compte_des_nombres_premiers>`_ en
   :math:`O\left(\frac{n}{\ln n}\right)` au lieu de :math:`O(n)` (où :math:`n`
   est le plus grand nombre premier trouvé).

L'algorithme est décrit par la suite (:ref:`erathostene_algo`), et implémenté
dans la fonction :py:func:`premiers`.

.. contents::
   :local:
   :depth: 1

Usage
=====

.. argparse::
    :module: jouets.erathostene.__main__
    :func: analyse
    :prog: erathostene

.. _erathostene_algo:

Algorithme
==========

Code source
-----------

.. literalinclude:: ../jouets/erathostene/__init__.py
    :linenos:
    :pyobject: premiers

Algorithme d'Érathostène original
---------------------------------

Le principe du crible d'Érathostène est :

#. On considère une table de tous les nombres entiers naturels supérieurs
   (strictement) à 1, jusqu'à un certain :math:`N`.
#. On prend le premier nombre de cette table : il est premier. On le
   supprime, et on supprime également de la table tous ses multiples.
#. On recommence l'étape précédente jusqu'à épuisement de la liste.

Optimisation en espace
----------------------

L'optimisation consiste en la chose suivante.
On construit un dictionnaire ``prochains`` dont
les clefs sont des nombres pas encore rencontrés,
et les valeurs des nombres premiers.
Par exemple, ``prochains[p] == m`` signifie que ``p`` est un nombre premier,
et ``m`` le prochain (nous verrons dans quel sens) de ses multiples.
Ensuite, quand un nombre premier est trouvé,
plutôt que de supprimer tous ses multiples de la table des entiers
(ce qui n'a pas de sens ici, puisqu'une telle table n'existe pas),
on ajoute au dictionnaire ``prochains`` ce nombre,
ainsi que son prochain multiple.

L'algorithme (de base : quelques optimisations seront apportées dans la
section suivante) est donc le suivant :

1. Initialisation : ``prochains`` est un dictionnaire vide.

2. On considère ``n`` :

  * Si ``n`` n'est pas une clef du dictionnaire ``prochains``, il est premier.
    On le renvoit (``yield n``), et on affecte ``premiers[n**2] = n``,
    ce qui signifie que la clef ``n**2`` est le prochain multiple du nombre premier ``n`` à étudier.
  * Sinon, ``n`` est une clef du dictionnaire.
    Donc il est multiple du nombre premier ``prochains[n]``.
    On supprime alors ``prochains[n]``,
    et on crée dans le dictionnaire une nouvelle entrée ``prochains[m] = p``, où
    ``p`` était la valeur de ``prochains[n]``
    (c'est-à-dire un des diviseurs premiers de ``n``),
    et ``m`` est le prochain multiple de ``p``.

    En d'autres termes, dans notre crible d'Érathostène,
    on raye le prochain nombre multiple du nombre premier ``p``.

3. On ajoute 1 à ``n``, et on recommence à l'étape 2.

Optimisations supplémentaires
-----------------------------

Quelques optimisations sont mises en place.

* Plutôt que de compter de 1 en 1, on remarque que 2 est premier, et on
  compte de 2 en 2, uniquement les nombres impairs (puisqu'aucuns des
  nombres pairs autre que 2 n'est premier).
* Le ``multiple`` du couple :math:`(premier, multiple)` n'est pas
  nécéssairement le *prochain* multiple de :math:`premier` si cela n'est
  pas nécessaire. Par exemple, si ``prochains`` contient le couple
  :math:`(3, 15)`, il n'est pas nécessaire d'ajouter :math:`(5, 15)` à la
  liste, puisque 15 est déjà marqué comme non premier ; on ajoutera donc
  plutôt :math:`(5, 25)`.
* Lors du premier ajout d'un nombre premier :math:`p` à la liste
  ``prochains``, le multiple associé est :math:`p^2`. En effet, tous les
  multiples plus petits sont ou seront traités par des nombres premiers
  déjà découverts.

Exemple
-------

Par exemple, au bout de quelques tours de boucles, alors que :math:`n=13`, la varibles ``prochains`` vaut:

.. code-block:: python

   {
     15: 3,
     25: 5,
     49: 7,
     121: 11,
    }

Cela signifie que dans notre crible d'Érathostène, à partir du nombre 13 :

- le prochain multiple de 3 est 15 ;
- le prochain multiple de 5 est 25 ;
- le prochain multiple de 7 est 49 ;
- le prochain multiple de 11 est 121.

Au tour suivant, :math:`n=15`. Puisque 15 est une clef du dictionnaire, il n'est pas premier. On le retire, et on ajoute ``prochains[21] = 3`` (ce qui signifie que le prochain multiple de 3 est 21) :

.. code-block:: python

   {
     21: 3,
     25: 5,
     49: 7,
     121: 11,
     169: 13,
   }

Au tour suivant, :math:`n=17`, qui *n'est pas* une clef du dictionnaire : c'est donc un nombre premier, et on ajoute ``prochains[17] = 17**2`` comme le prochain nombre multiple de 17 à rayer (il y a d'autres nombres multiples de 17 avant :math:`17^2`, mais il est inutile de les rayer ici car ils seront rayés comme multiples de nombres plus petits).

Performances
============

Sur mon ordinateur portable, j'ai été capable de générer les nombres premiers suivants :

- un million de nombres premiers en 7 secondes ;
- dix millions de nombres premiers en 1 minute et demi.

J'ai été jusqu'à calculer le 70140686ᵉ nombre premier (1403273909), en utilisant 10Go de mémoire. Après cela, le programme s'est arrêté, sans que je comprenne pourquoi…

Par peur du ridicule, je n'ose pas comparer cela aux performances des algorithmes qui battent des records, mais je suis quand même content de moi… 🤓🙂
