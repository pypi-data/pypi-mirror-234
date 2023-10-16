..
   Copyright 2014-2017 Louis Paternault
   
   Cette œuvre de Louis Paternault est mise à disposition selon les termes de
   la licence Creative Commons Attribution - Partage dans les Mêmes Conditions
   4.0 International (CC-BY-SA). Le texte complet de la licence est disponible
   à l'adresse : http://creativecommons.org/licenses/by-sa/4.0/deed.fr

.. _dobble_variantes:

Variantes
=========

Je proposerai ici deux variantes du jeu de Dobble, pas forcément jouables, mais
qui peuvent être intéressantes du point de vue mathématique.

.. contents::
   :local:
   :depth: 1

Diffle
------

Lors d'une discussion sur les math derrière le Dobble, quelqu'un m'a posé la
question suivante : Est-il possible de faire un jeu similaire au Dobble, sauf
qu'au lieu que chaque couple de cartes ait exactement un symbole commun, chaque
couple de cartes aurait tous ses symboles communs, sauf un sur chaque carte ?

La réponse est : c'est possible, mais ça n'est pas intéressant.

Quelques exemples
^^^^^^^^^^^^^^^^^

À première vue, nous cherchons un ensemble de cartes tels que deux cartes
quelconques aient tous leurs symboles différents, sauf un sur chaque. Voici un
exemple de jeu de Diffle valide.

.. tikz:: Jeu de Diffle
   :include: diffle_canonique4.tikz

Une première famille de jeux valides est assez simple à constituer : il suffit
de prendre un nombre quelconque de cartes, avec un unique symbole par cartes,
tous les symboles étant différents. Cela fonctionne, mais le jeu n'est pas
vraiment intéressant. De même, on peut imaginer des jeux avec des cartes de
taille variable, ou des symboles apparaissant de manière irrégulière. Mais nous
perdons alors la régularité des configurations de Dobble.

Essayons de construire des configurations plus intéressantes.

Configuration valide
^^^^^^^^^^^^^^^^^^^^
Les :ref:`définitions de base <dobble_math_definitions>` sont les mêmes que
celles du Dobble.

.. proof:definition:: Configuration valide

    * *Convention :* Les symboles sont les nombres entiers positifs (1, 2, 3…).

    * Une configuration de Diffle est dite *valide* si tout couple de cartes
      a tous ses symboles en commun, sauf un sur chaque carte.

.. proof:property::

  Nous remarquons immédiatement que toutes les cartes d'une configuration
  valide de Diffle ont le même nombre de symboles.

Le problème avec ces définitions est que la proposition triviale proposée plus
haut (un unique symbole sur chaque carte) est une configuration valide. Mais
elle n'est pas intéressante à jouer.

Pour ajouter de la difficulté, nous pouvons ajouter autant de symboles
identiques à toutes les cartes, comme sur l'exemple suivant.

.. proof:example::

  .. tikz::
     :include: diffle_redondant.tikz

Cette configuration est valide, mais pas vraiment intéressante non plus : un
joueur expérimenté remarquera assez vite que les symboles 5, 6, 7 sont toujours
en commun (donc peuvent être ignorés), mais que les symboles 1, 2, 3, 4 sont
toujours des symboles différents, à repérer.

Ajoutons des contraintes pour éviter ces configurations peu intéressantes.

Configuration régulière
^^^^^^^^^^^^^^^^^^^^^^^

Nous prenons alors la définition suivante pour une configuration de Diffle
dite régulière. Elle paraît peu contraignante, mais nous verrons qu'elle suffit pour
montrer que des configurations de Diffle jouables n'existent pas.

.. proof:definition:: Configuration régulière

  Une configuration valide de Diffle est dite *régulière* si pour tout
  symbole :math:`s` :

  * il existe un couple de cartes contenant toutes les deux ce symbole ;
  * il existe un couple de cartes dont l'une contient :math:`s`, et l'autre ne
    contient pas :math:`s`.

.. proof:property:: Définition équivalente

  Une configuration valide de :math:`n` cartes est *régulière* si et seulement
  si, pour tout symbole :math:`s` :

  * :math:`s` apparait au moins deux fois ;
  * :math:`s` apparait au plus :math:`n-1` fois.

De telles configurations existent : le premier exemple donné dans cette partie
est une configuration régulière.

Nous allons maintenant caractériser ces configurations régulières.

Configurations canoniques
^^^^^^^^^^^^^^^^^^^^^^^^^

Il est très facile de construire une configuration régulière.

.. proof:definition:: Configuration canonique

  Étant donné un entier :math:`n\geq2`, on appelle *configuration régulière
  canonique de taille* :math:`n` (ou plus simplement *configuration canonique
  de taille* :math:`n`) la configuration constituée :

  * des symboles :math:`1, 2, \cdots, n` ;
  * des cartes :math:`\left[1, n\right]\backslash\left\{i\right\}`, pour chacun
    des nombres :math:`i` allant de :math:`1` à :math:`n` (en d'autres termes,
    chaque carte contient tous les symboles sauf un).

.. proof:property::

  Toute configuration canonique est valide et régulière.

.. proof:proof::

  Laissée au lecteur patient.

.. proof:example::

  Voici la configuration canonique de taille 5 : chaque carte contient tous les
  nombres de 1 à 5, sauf un.

  .. tikz::
     :include: diffle_canonique5.tikz

C'est une configuration régulière mais ce n'est pas une bonne configuration à
jouer pour autant : par exemple, un jeu de 55 cartes (comme le Dobble)
possèderait 54 symboles par cartes, ce qui serait bien trop confus et
compliqué. Existe-t-il d'autres configurations que celles-ci ? La réponse est
malheureusement non.


Caractérisation des solutions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Commençons par un lemme, utile pour prouver la propriété suivante.

.. proof:lemma::

  Soit une configuration telle que l'union de tout couple de cartes
  :math:`c_1`, :math:`c_2` contient l'ensemble des symboles de la
  configuration. Alors cette configuration est le sous-ensemble d'une
  configuration canonique (à un renommage des symboles près).

.. proof:proof::

  Soit :math:`C` une telle configuration, et :math:`c_1` et :math:`c_2` deux de
  ses cartes. Alors :math:`c_1\cup c_2` contient tous les symboles. Mais
  puisque la configuration est valide, :math:`c_2` possède un seul symbole
  absent de :math:`c_1` : :math:`c_1` contient donc tous les symboles sauf un.

  En faisant le même raisonnement pour chacune des cartes de :math:`C`, nous
  pouvons montrer que chaque carte contient tous les symboles sauf un : c'est
  une configuration canonique (ou un sous-ensemble d'une telle configuration).

.. proof:property:: Caractérisation des configurations intéressantes

  Toute configuration régulière est une configuration canonique, ou un
  sous-ensemble d'une configuration canonique (une configuration canonique à
  laquelle il manque des cartes).

.. proof:proof::

  Prouvons cette propriété par l'absurde, en prenant :math:`C` une
  configuration régulière qui ne soit pas un sous-ensemble d'une configuration
  canonique. Nous allons montrer que :math:`C` n'existe pas.
  Faisons une disjonction des cas sur le nombre de cartes
  :math:`\operatorname{card} C` de :math:`C`.

  * *Premier cas :* :math:`C` a deux cartes. Alors il existe un unique couple
    de cartes de :math:`C` et, de manière triviale, tout couple de cartes
    contient l'ensemble des symboles. Par le lemme précédent, :math:`C` est
    canonique, ce qui est en contradiction avec notre hypothèse.

  * *Second cas :* :math:`C` a au moins trois cartes. Prenons deux cartes
    :math:`c_1` et :math:`c_2` telles que :math:`c_1\cup c_2` ne contienne pas
    tous les symboles du jeu (un tel couple existe, sans quoi, par le lemme
    précédent, la configuration serait (un sous-ensemble d'une configuration)
    canonique, ce qui est contraire à l'hypothèse). Considérons (à une
    permutation près des symboles) que :

    * le symbole 1 est présent dans :math:`c_1` mais pas dans :math:`c_2` ;
    * le symbole 2 est présent dans :math:`c_2` mais pas dans :math:`c_1` ;
    * le symbole 3 est présent dans les deux cartes ;
    * éventuellement, d'autres symboles sont présents dans les deux cartes.

    Notons que les cartes ont au moins deux symboles (puisqu'elles ont toutes
    le même nombre de symboles, si l'une d'entre elles a un seul symbole,
    toutes ont un seul symbole, et la configuration n'est pas régulière).

    .. tikz::
       :include: diffle_interessant1.tikz

    Prenons maintenant une troisième carte :math:`c_3`, et :math:`4` un symbole de :math:`c_3`
    n'appartenant ni à :math:`c_1` ni à :math:`c_2` (un tel symbole existe par
    hypothèse sur :math:`c_1` et :math:`c_2`).

    * Si :math:`C` contient trois cartes, alors le symbole :math:`4` n'apparait
      que sur une carte, et la configuration n'est pas régulière, ce qui est en
      contradiction avec notre hypothèse.
    * Donc :math:`C` contient plus de trois cartes. Puisque la configuration est
      régulière, il existe une carte :math:`c_4` contenant le symbole
      :math:`4`.

      .. tikz::
         :include: diffle_interessant2.tikz


      Les cartes :math:`c_3` et :math:`c_4` contiennent tous les symboles de
      :math:`c_1` sauf un, et tous les symboles de :math:`c_2` sauf un.

      * Supposons que :math:`c_3` contienne le symbole 1. Alors elle ne contient
        pas un des autres symboles de :math:`c_1`, par exemple 3 (à une
        permutation près). Donc, de même, elle contient tous les symboles de
        :math:`c_2` sauf 3, donc elle contient 2. Elle contient donc deux
        symboles qui n'apparaissent pas dans :math:`c_1` : 2 et :math:`4`. La
        configuration n'est donc pas valide.
      * Donc :math:`c_3` ne contient pas le symbole 1. Puisque 1 apparait dans
        :math:`c_1` mais pas dans :math:`c_3`, et que 4 apparait dans
        :math:`c_3` mais pas dans :math:`c_1`, puisque la configuration est
        valide, la carte :math:`c_3` est identique à :math:`c_1` en remplaçant
        le symbole 1 par 4.

      Et le même raisonnement s'applique également à :math:`c_4`, donc cette carte
      est également dans le deuxième cas : elle est identique à :math:`c_1` en
      remplaçant le symbole 1 par 4.

      Les deux cartes :math:`c_3` et :math:`c_4` sont donc identiques, donc le
      jeu n'est pas valide, ce qui est contraire à notre hypothèse de départ.

   Nous avons montré que dans tous les cas, l'hypothèse départ ne peut pas être
   valide. En d'autres termes, il n'existe pas de configuration régulière qui
   ne soit pas un sous-ensemble d'une configuration canonique.

Bilan
^^^^^

Nous avons montré que, même avec des contraintes de régularité assez faibles,
il n'existe pas de configuration de Diffle intéressante à jouer. Dommage…

Mémobble
--------

Le Mémobble est un mélange de Dobble et de `Mémory <https://fr.wikipedia.org/wiki/Memory_(jeu)>`__.

Règles
^^^^^^

Le jeu est composé l'un ensemble de cartes, sur lesquelles sont dessinées plusieurs symboles (comme pour un jeu de Dobble). Elles sont disposées face cachée sur la table, et à son tour, un joueur :

* retourne deux cartes ;
* si ces deux cartes ont un symbole en commun, la première personne à l'annoncer remporte les deux cartes ;
* sinon, elles sont remises face cachée sur la table.

Le jeu s'arrête lorsqu'il n'y a plus de cartes sur la table ; la personne ayant ramassé le plus de cartes a gagné la partie.

Intérêt
^^^^^^^

Tuons tout espoir dans l'œuf : ce jeu n'a aucun intérêt.

Je l'ai testé avec de petites configurations, et il est beaucoup trop difficile : se souvenir de la position des symboles n'est déjà pas facile au Mémory, mais dans cette version, il y a plusieurs symboles par carte à mémoriser.

Un `ami <http://www.game-flow.fr>`__ a résumé le problème de la manière suivante : « Ça ressemble au dobble, mais en moins bien ; ça ressemble au mémory, mais en moins bien ».

Heureusement, s'il n'a pas d'intérêt ludique, il a un intérêt mathématique.

Modélisation
^^^^^^^^^^^^

Un tel jeu doit être construit de manière à rendre les blocages impossibles. Imaginons par exemple les deux parties suivantes, jouées avec le même jeu. Sont représentés les cartes restant sur la table ; les deux cartes grisées à chaque étape sont celle allant être retirées du jeu.

.. tikz:: Pas de blocage
   :include: memobble-blocage1.tikz

Dans cette première partie présentée ci-dessus, tout se déroule convenablement, et la partie se termine.

.. tikz:: Blocage
   :include: memobble-blocage2.tikz

En revanche, dans cette seconde partie, réalisée avec les mêmes cartes de départ, la situation se bloque, car les cartes restantes n'ont aucun symbole en commun. Si, dans cet exemple, les joueurs se rendent compte facilement que la partie est terminée, il est possible d'imaginer assez facilement des situations où de nombreuses cartes restent, sans aucun symbole en commun. Dans ce cas, les joueurs ont peu de chance de remarquer que la partie est terminée.

Cette situation de blocage ne doit donc pas arriver.

Graphe
""""""

Comme dans la partie précédente, un jeu peu être représenté par un graphe, où :

* les sommets correspondent aux cartes ;
* les arêtes aux symboles en commun (il existe une arête entre deux sommets si les deux cartes correspondantes ont un symbole en commun).

Par exemple, le jeu étudié à la partie précédente est modélisé par le graphe suivant (où, pour plus de clarté, les arêtes prennent la couleur des symboles qu'elles représentent).

.. tikz:: Graphe modélisant le jeu précédent.
   :include: memobble-graphe.tikz

Quelques propriétés
"""""""""""""""""""

Le problème du blocage peut alors être reformulé de la manière suivante.

.. proof:definition:: Configuration valide

   Une configuration est valide si la procédure suivante (appliquée à son graphe) aboutit toujours à un graphe vide :

   - choisir une arête au hasard ;
   - supprimer les deux sommets aux extrémités de cette arête (et toutes les autres arêtes ayant un de ces deux sommets pour extrémité) ;
   - recommencer.

Une configuration n'est alors pas valide s'il est possible de se retrouver dans une situation où il reste des sommets, mais pas d'arête.

Comme pour l'étude du jeu de Dobble, une certaine régularité dans les jeux étudiés est appréciée.

.. proof:definition:: Configuration régulière

   Une configuration valide est dite régulière si :

   - chaque carte contient le même nombre de symboles ;
   - chaque symbole apparaît autant de fois.

Connexité et Union disjointe
""""""""""""""""""""""""""""

Commençons par définir une configuration connexe.

.. proof:definition:: Configuration connexe

  Une configuration est dite connexe si son graphe est connexe (d'autres termes si, partant d'une carte, en se déplaçant de cartes en cartes uniquement si elles ont un symbole en commun, on peut arriver à n'importe quelle autre carte).

Si les configurations connexes sont intéressantes, c'est parce que l'union disjointe de deux configurations valides est elle aussi valide (:numref:`union-disjointe-valide`).

.. proof:definition:: Union disjointe

  On appelle *union disjointe* de deux configurations la configuration composée des cartes des deux configurations de bases, dans laquelle les symboles ont été renommés (si nécessaire) pour que les deux configurations d'origine n'aient aucun symbole en commun.

.. _union-disjointe-valide:

.. proof:property:: Union disjointe de configurations valides

  L'union disjointe de configurations valides est une configuration valide.

.. proof:proof::

  La démonstration est laissée au lecteur patient.

L'union disjointe est intéressante parce qu'étaint connues plusieurs configurations valides, il est possible de construire une nouvelle configuration composée des configurations connexes valides.

Algorithmes
^^^^^^^^^^^

Présentons quelques algorithmes de génération de configurations régulières connexes. D'autres configurations non connexes valides (mais pas nécessairement régulières) peuvent être crées en unissant des configurations connexes.

Dobble
""""""

Un jeu de Dobble n'est pas une configuration valide, pour la simple raison qu'il est composé d'un nombre impair de cartes (alors qu'une configuration de Mémobble valide doit avoir un nombre pair de cartes).

En enlevant une carte à un jeu de Dobble, cela crée une configuration de Mémobble valide, mais qui n'est pas régulière.

Graphe complet
""""""""""""""

Une configuration représentée par un `graphe complet <https://fr.wikipedia.org/wiki/Graphe_complet>`__ (dans lequel il existe une arête entre n'importe quel couple de sommets) d'ordre pair (ayant un nombre pair de sommets) est une configuration valide. Reste à trouver les cartes et les symboles qui permettent d'obtenir un tel graphe.

Une première méthode est de prendre un jeu de Dobble (dont le graphe est complet), mais nous avons vu précédemment qu'un tel jeu ne constitue pas une configuration valide, sauf à lui enlever une carte, auquel cas elle n'est pas régulière.

Une autre méthode, moins fine, consiste à créer un symbole pour chacune des arêtes. C'est un des algorithmes implémenté dans le :ref:`logiciel <memobble_logiciel>`. Un exemple à quatre cartes est donné ci-dessous.

.. tikz:: Configuration à partir d'un graphe complet.
   :include: memobble-complet.tikz


Graphe bipartite complet
""""""""""""""""""""""""

Un autre algorithme est l'utilisation d'un `graphe bipartite complet <https://fr.wikipedia.org/wiki/Graphe_biparti_complet>`__ dans laquelle chacun des deux sous-ensembles a le même nombre de cartes. Celui-ci est constitué de deux ensembles de cartes. Chaque carte est adjacente (partage une arête avec) chacune des cartes de l'autre ensemble, et uniquement celles-là. Un exemple à six cartes est donné ci-dessous.

.. tikz:: Graphe bipartite complet
   :include: memobble-bipartite.tikz

.. proof:property:: Graphe bipartite complet

  Une configuration représentée par un graphe bipartite complet est valide.

.. proof:proof::

  La preuve est très simple, une fois qu'il a été remarqué que la suppression d'un couple de cartes est toujours possible tant qu'il reste au moins une carte dans chaque sous-ensemble, et enlève toujours une carte dans chacun des deux sous-ensembles.

Une fois encore, je n'ai pas réussi à trouver d'autre configuration que celle consistant à utiliser un symbole différent pour chaque arête (contrairement aux configurations de Dobble, où les symboles correspondent à plusieurs arêtes). Autrement dit, je n'ai pas réussi à faire en sorte que chaque symbole apparaisse plus de deux fois.

Conclusion
^^^^^^^^^^

Je n'ai pas trouvé d'autres configurations régulières, ni même valide. Ce qui me frustre est que je n'ai réussi à trouver aucune configuration dans laquelle chaque symbole apparait plus de deux fois.

Un autre regret est que je n'arrive pas à caractériser la validité d'une configuration autrement qu'en décrivant la suppression successive de couples de cartes, jusqu'à épuisement.

.. _memobble_logiciel:

Logiciel
^^^^^^^^

.. argparse::
    :module: jouets.dobble.memobble.__main__
    :func: analyse
    :prog: python -m jouets.dobble.memobble

