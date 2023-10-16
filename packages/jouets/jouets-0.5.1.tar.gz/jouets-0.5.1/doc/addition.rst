************************************************
`addition` — Recherche de solutions d'une énigme
************************************************

Ce programme met en œuvre plusieurs algorithmes de recherche de solutions de l'énigme suivante.

    Par quels chiffres faut-il remplacer les lettres pour que l'addition suivante soit correcte ?

    .. math::

      \begin{array}{lcccc}
          &  & &U&N \\
        + &  & &U&N \\
        + & D&E&U&X \\
        + & C&I&N&Q \\
      \hline
        = & N&E&U&F \\
      \end{array}

La première solution présentée mets sept minutes à trouver les solutions, tandis que la dernière fait le même travail en moins de deux secondes.

.. contents::
   :local:
   :depth: 1

Algorithmes
===========

Version 1
---------

.. literalinclude:: ../jouets/addition/__init__.py
    :linenos:
    :pyobject: addition1

La première version est *très* naïve, et n'utilise aucune fonctionnalité avancée du langage Python (si ce n'est le ``yield`` pour itérer les solutions).

Chaque lettre a sa propre boucle (qui balaye tous les chiffres de 0 à 9), et avant de tester si les variables correspondent à une solution, on vérifie que chaque variable est différente avec un ``if`` qui teste chacune des 28 combinaisons possibles.

Cette version est très lente : l'exécution prend presque sept minutes.

Version 2
---------

.. literalinclude:: ../jouets/addition/__init__.py
    :linenos:
    :pyobject: addition2

Le ``if`` de la première version (qui teste si les variables sont distinctes) n'est pas très élégant. Cette seconde version remplace cette trentaine de lignes par une unique : ``len(set((C, D, E, F, I, N, Q, U, X))) == 9``. Ce test vérifie que l'ensemble des neuf variables contient neuf éléments (si deux variables sont égales, la taille de l'ensemble sera moindre).

J'ai été surpris de constater que cette version est plus lente que la précédente : plus de dix minutes.

Version 3
---------

.. literalinclude:: ../jouets/addition/__init__.py
    :linenos:
    :pyobject: addition3

Dans les versions précédentes, chacune des variables prend chacune des dix valeurs possibles, et c'est seulement juste avant de tester si l'addition est vérifiée ou non que l'on teste si les variables sont distinctes. C'est une perte de temps : dés qu'une variable prend la même valeur qu'une variable déjà définie, on peut passer à la valeur supérieure. C'est ce qui est mis en œuvre dans la fonction suivante.

Dans les deux versions précédentes, les boucles itèrent sur :math:`10^9` éléments (soit un milliard). Avec cette version (ainsi que toutes les suivantes), les boucles n'itèrent plus que sur :math:`A^9_{10}` arrangements (soit environ 3,6 millions). Cela fait 300 fois moins de tests, et explique que le temps d'exécution passe de sept minutes à seulemnt 8,5 secondes.

Version 4
---------

.. literalinclude:: ../jouets/addition/__init__.py
    :linenos:
    :pyobject: addition4

Cette version est la même que la précédente, sauf que l'énumération des arrangements n'est pas fait « à la main », mais en utilisant la fonction :func:`itertools.permutations` correspondante de la bibliothèque standard de Python. Ces fonctions de la bibliothèque standard ont été écrites par des gens plus intelligents que moi, testées depuis des années, écrites en C pour certaines : sauf cas très particulier, elles sont plus rapides que ce que je pourrais écrire.

Et en effet, le simple fait de remplacer mon implémentation des arrangements par l'appel de la bonne fonction de la bibliothèque standard fait passer le temps d'exécution de 8,5 secondes à 3,3 secondes (trois fois plus rapide).

Version 5
---------

.. literalinclude:: ../jouets/addition/__init__.py
    :linenos:
    :pyobject: addition5

Lors de la vérification de l'égalité :math:`(10 \times U + N) + (10 \times U + N) + (1000 \times C + 100 \times I + 10 \times N + Q) + (1000 \times D + 100 \times E + 10 \times U + X) = 1000 \times N + 100 \times E + 10 \times U + F`, onze multiplications sont effectuées. En réarrangeant cette équation (en factorisant par 10, 100, et 1000), on obtient le test :math:`1000 \times (C + D - N) + 100 \times I + 10 \times (2 \times U + N) + (2 \times N + Q + X - F) = 0` qui ne contient plus que trois multiplications (en ignorant les multiplications par 2). Cette simple optimisation fait-elle gagner de temps ?

Oui : elle permet de passer de 3,3 secondes à 2,1 secondes (soit un gain d'un tiers).

Version 6
---------

.. literalinclude:: ../jouets/addition/__init__.py
    :linenos:
    :pyobject: _sousfonction6

.. literalinclude:: ../jouets/addition/__init__.py
    :linenos:
    :pyobject: addition6

La dernière optimisation permet de profiter des plusieurs processeurs utilisés par la plupart des ordinateurs modernes. La fonction de recherche est exécutée 10 fois, pour chacune des valeurs possibles de la première lettre `C`. Ces fonctions sont appelées avec autant d'exécution parallèles que de processeurs, en utilisant la classe :class:`multiprocessing.pool.Pool` de la bibliothèque standand, qui gère tout cela de manière automatique.

Sur ma machine (qui possède quatre cœurs), cela permet de passer de 2 secondes d'exécution à seulement 1 seconde. Cela divise le temps d'exécution par deux, ce qui est moins que ce que l'on aurait pu attendre (une division par quatre avec quatre cœurs), mais c'est déjà bien.

Conclusion
----------

Trois principales optimisations sont à remarquer.

- La réduction de l'espace des solutions recherchées (des versions 2 à 3) a produit un algorithme 300 fois plus rapide. C'est la seule des optisations présentées ici qui réduit la complexité de l'algorithme.
- L'utilisation de la bibliothèque standard de Python (modules :mod:`itertools` et :mod:`multiprocessing`).
- La réduction du nombre de multiplications (versions 4 à 5).

Usage
=====

Le binaire ``python -m jouets.addition`` n'accepte aucune option (plus précisément, il les ignore toutes). Il recherche les solutions de l'énigme en utilisant toutes les variantes possibles, affiche ces solutions, et le temps d'exécution de chaque fonction.
