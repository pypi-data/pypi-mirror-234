====================
Analyse mathématique
====================

Je n'ai aucune idée de la manière dont je pourrais étudier ce problème d'un point de vue général. Donc nous allons commencer par un cas particulier, pour réduire la complexité : un jeu de bataille avec un jeu de deux couleurs de deux cartes chacune.

Cas particulier : Deux cartes dans deux couleurs
================================================

Pour étudier ce problème, dressons le graphe probabiliste qui correspond à la situation.

Graphe
------

.. tikz:: Graphe probabiliste d'un jeu de bataille à deux couleurs de deux cartes chacune.
   :include: graphe-proba-2-2.tikz

Quelques précisions sur ce graphe.

Description des sommets
"""""""""""""""""""""""

- Le sommet :math:`A` représente l'état initial, avant la distribution des cartes. Les quatre cartes peuvent être distribuées de quatre manières différentes, correspondant aux sommets :math:`B`, :math:`C`, :math:`F`, :math:`G`.
- Le sommet :math:`J` représente l'état final, lorsque la partie est terminée.
- Sur les autres sommets (sauf :math:`A` et :math:`J`), le paquet de carte est représenté. Chaque colonne correspond au paquet d'une joueuse, et les nombres aux numéros des cartes (les couleurs ne sont pas représentées). Par exemple, le sommet :math:`E` correspond à la situation où une des joueuse n'a plus qu'une carte (2) et l'autre a trois cartes (de haut en bas : 1 2 1).

Remarquons deux choses :

- l'ordre des joueuses n'a aucune importance : elles peuvent être permutées sans changer les probabilités ;
- les couleurs des cartes n'ont aucune importance.

Transitions
"""""""""""

- Les probabilités n'interviennent que pour le rangement des cartes (une fois le pli résolu).
- Puisque :math:`J` est l'état final, cet état ne change pas, ce qui est symbolisé par une probabilité 1 de rester en :math:`J`.
- Étudions les probabilités de distribution des cartes. Comment peut-on distribuer quatre cartes :math:`a`, :math:`b`, :math:`c`, :math:`d` en deux paquets ? Il y a 24 possibilités.

  .. container:: columns

      .. math::

          \begin{array}{|cc|}
              \hline
              a & b \\
              c & d \\
              \hline
          \end{array}

      .. math::

          \begin{array}{|cc|}
              \hline
              a & b \\
              d & c \\
              \hline
          \end{array}

      .. math::

          \begin{array}{|cc|}
              \hline
              a & c \\
              b & d \\
              \hline
          \end{array}

      .. math::

          \begin{array}{|cc|}
              \hline
              a & c \\
              d & b \\
              \hline
          \end{array}

      .. math::

          \begin{array}{|cc|}
              \hline
              a & d \\
              b & c \\
              \hline
          \end{array}

      .. math::

          \begin{array}{|cc|}
              \hline
              a & d \\
              c & b \\
              \hline
          \end{array}

      .. math::

          \begin{array}{|cc|}
              \hline
              b & a \\
              c & d \\
              \hline
          \end{array}

      .. math::

          \begin{array}{|cc|}
              \hline
              b & a \\
              d & c \\
              \hline
          \end{array}

      .. math::

          \begin{array}{|cc|}
              \hline
              b & c \\
              a & d \\
              \hline
          \end{array}

      .. math::

          \begin{array}{|cc|}
              \hline
              b & c \\
              d & a \\
              \hline
          \end{array}

      .. math::

          \begin{array}{|cc|}
              \hline
              b & d \\
              a & c \\
              \hline
          \end{array}

      .. math::

          \begin{array}{|cc|}
              \hline
              b & d \\
              c & a \\
              \hline
          \end{array}

      .. math::

          \begin{array}{|cc|}
              \hline
              c & a \\
              b & d \\
              \hline
          \end{array}

      .. math::

          \begin{array}{|cc|}
              \hline
              c & a \\
              d & b \\
              \hline
          \end{array}

      .. math::

          \begin{array}{|cc|}
              \hline
              c & b \\
              a & d \\
              \hline
          \end{array}

      .. math::

          \begin{array}{|cc|}
              \hline
              c & b \\
              d & a \\
              \hline
          \end{array}

      .. math::

          \begin{array}{|cc|}
              \hline
              c & d \\
              a & b \\
              \hline
          \end{array}

      .. math::

          \begin{array}{|cc|}
              \hline
              c & d \\
              b & a \\
              \hline
          \end{array}

      .. math::

          \begin{array}{|cc|}
              \hline
              d & a \\
              b & c \\
              \hline
          \end{array}

      .. math::

          \begin{array}{|cc|}
              \hline
              d & a \\
              c & b \\
              \hline
          \end{array}

      .. math::

          \begin{array}{|cc|}
              \hline
              d & b \\
              a & c \\
              \hline
          \end{array}

      .. math::

          \begin{array}{|cc|}
              \hline
              d & b \\
              c & a \\
              \hline
          \end{array}

      .. math::

          \begin{array}{|cc|}
              \hline
              d & c \\
              a & b \\
              \hline
          \end{array}

      .. math::

          \begin{array}{|cc|}
              \hline
              d & c \\
              b & a \\
              \hline
          \end{array}

  Enfin, en attribuant les valeurs 1, 1, 2, 2 aux cartes :math:`a`, :math:`b`, :math:`c`, :math:`d`, on obtient les probabilités décrites par les transitions allant de l'état :math:`A` aux états :math:`B`, :math:`C`, :math:`F`, :math:`G`.

Probabilités
------------

Cela va être compliqué de déterminer toutes les probabilités, mais nous pouvons en calculer quelques unes.

- Tout d'abord, remarquons que si la partie commence en :math:`B`, :math:`F` ou :math:`G`, le nombre de plis joués avant la fin est impair ; si la partie commence en :math:`C`, il est pair. Cela veut dire que la probablité d'avoir un nombre de plis pair est de :math:`1/3`, la probabilité d'avoir un nombre de plis impairs est :math:`2/3`.
- La partie ne dure qu'un pli si et seulement si elle commence en :math:`F` ou :math:`G`. Donc la probabilité d'avoir un seul pli est :math:`1/3`.
- La partie ne dure que deux plis si et seulement si elle commence en :math:`C`, ce qui donne une probabilité de :math:`1/3`.
- Sinon, la partie dure au moins trois plis, avec une probabilité de :math:`1/3` également.

Comparaison
-----------

En étudiant les :download:`résultats d'un million de simulations <bataille-2-2-1000000.ods>` (décrits à la :ref:`partie précédente <bataille-informatique>`), on tombe sur les mêmes résultats.

============== =========== =========
Nombre de plis Probablitié Fréquence
============== =========== =========
Pair           1/3         0,332986
Impair         2/3         0,667014
1              1/3         0,333510
2              1/3         0,332986
3 et plus      1/3         0,333504
============== =========== =========

Les résultats théoriques sont concordants avec les observations des simulations. Cela signifie probablement l'une des deux choses suivantes :

- soit mes calculs et ma simulation sont correctes ;
- soit j'ai fait la même erreur dans les deux cas.

Généralisation
==============

En théorie, il serait possible de généraliser cette méthode à n'importe quel nombre de cartes. En pratique, le nombre d'états de mon graphe serait énorme.

Étudions le cas avec une couleur de treize cartes. Il y aurait alors :math:`13!\times12` états possibles. En effet, le nombre de combinaisons possibles de ces treize cartes en un tas unique est :math:`13!`, que l'on peut ensuite découper en deux tas de 12 manières différentes. Cela donne donc :math:`13!\times12\approx 7,5\times10^{10}`, soit plus de sept milliards d'états. Pour un jeu de 52 cartes (13 numéros pour chacune des 4 couleurs), le nombre d'états serait encore plus vertigineux.

À moins de trouver de très bonnes optimisations, étudier tous ces états avec un ordinateur me paraît inenvisageable.

Conclusion
==========

À défaut de pouvoir généraliser cette analyse mathématique à plus de cartes, elle ne sert malheureusement qu'à valider le modèle informatique décrit dans la partie qui précède.
