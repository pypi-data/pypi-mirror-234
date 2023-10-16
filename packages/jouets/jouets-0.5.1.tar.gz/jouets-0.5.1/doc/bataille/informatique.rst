.. _bataille-informatique:

====================
Analyse informatique
====================

Indicateurs
-----------

Voici les indicateurs pour les jeux les plus courants. Toutes les configurations ont été testées, pour un nombre de couleurs inférieur à 10, et un nombre de cartes par couleur inférieur à 10 : voir
:doc:`les données et graphiques <donnees>`,
:doc:`les statistiques <statistiques>`.

Jeu de 32 cartes
""""""""""""""""

Sur un million de parties (avec un jeu de 8 cartes de 4 couleur) :

.. plot::

   from jouets.bataille.graphiques import histogramme
   histogramme(4, 8, nombre=1000000)

- Plus courte partie : 3 plis ; plus longue partie : 1625 plis.
- Moyenne : 126.5, Médiane : 96.0, Mode : 44.
- Intervalle de confiance : [20 ; 404].
- :download:`Données brutes <bataille-4-8-1000000.csv>`.

Interprétation : Une partie dure en moyenne 126,5 plis ; la moitié des parties dure 96 plis ou moins, la moitié dure 96 plis ou plus ; la durée la plus fréquente est 44 plis. Dans 95% des cas, la durée de la partie est comprise entre 20 et 404 plis.

Jeu de 52 cartes
""""""""""""""""

Sur un million de parties (avec un jeu de 13 cartes de 4 couleur) :

.. plot::

   from jouets.bataille.graphiques import histogramme
   histogramme(4, 13, nombre=1000000)

- Plus courte partie : 15 plis ; plus longue partie : 6680 plis.
- Moyenne : 441.4, Médiane : 334.0, Mode : 140.
- Intervalle de confiance : [70 ; 1414].
- :download:`Données brutes <bataille-4-13-1000000.csv>`.

Jeu de Bata-waf
"""""""""""""""

Sur un million de parties (avec un jeu de 6 cartes de 6 couleurs) :

.. plot::

   from jouets.bataille.graphiques import histogramme
   histogramme(6, 6, nombre=1000000, titre="Durées de 1.000.000 parties de Bata-waf", etendue=2)

- Plus courte partie : 2 ; plus longue partie : 1260.
- Moyenne : 118.9, Médiane : 90.0, Mode : 40.
- Intervalle de confiance : [20 ; 374].
- :download:`Données brutes <bataille-6-6-1000000.csv>`.

Parité
------

Une chose qui m'a surpris est que selon mes simulations, la probabilité d'obtenir une durée de partie (en nombre de plis) paire ou impaire n'est absolument pas la même. Dans le graphique suivant, la courbe bleue correspond aux durées de parties paires, alors que la orange aux parties impaires (avec un jeu de 52 cartes).

.. plot::

   from jouets.bataille.graphiques import pairimpair
   pairimpair(4, 13, nombre=1000000)

Je ne comprends ni pourquoi, pour un jeu de 52 cartes, les deux parités ne sont pas équiprobables, ni pourquoi cela dépend du nombre de couleurs et de cartes.

:ref:`J'ai calculé <bataille-parite>` la parité la plus courante en fonction du nombre de cartes et de couleurs. En ignorant les parties avec peu de cartes ou de couleurs, la règle semble être :

- Si le nombre de couleurs et le nombre de valeurs sont tous les deux pairs, les parties de durée paire sont les plus probables.
- Si le nombre de couleurs ou le nombre de valeurs est un multiple de 4, les parties de durée paire sont les plus probables.
- Si le nombre de couleurs et le nombre de valeurs sont tous les deux impairs, les parties de durée paire et impaire sont à peu près équiprobables.
- Sinon, si le nombre de couleurs est pair, et le nombre de valeurs est impair, ou l'inverse, les parties de durée paire sont les plus probables.

Je ne sais absolument pas quoi faire de ces affirmations…

.. _comparaison-delahay:

Comparaison
-----------

Comme dit plus haut, dans leur article, Delahay te Mathieu n'utilisent pas exactement les mêmes règles que moi.
Pour voir la différence, j'ai simulé 1000000 de parties avec mes règles, et avec celles de Delahay et Mathieu.
Voici les statistiques obtenues.

+-------------------------+-----------------------------------------------------+-------------------------------------------------------------+
|                         | Moi                                                 | Delahay & Mathieu                                           |
+-------------------------+-----------------------------------------------------+-------------------------------------------------------------+
| Plus courte partie      | 15                                                  | 23                                                          |
+-------------------------+-----------------------------------------------------+-------------------------------------------------------------+
| Plus longue partie      | 6680                                                | 6955                                                        |
+-------------------------+-----------------------------------------------------+-------------------------------------------------------------+
| Moyenne                 | 441,4                                               | 582,3                                                       |
+-------------------------+-----------------------------------------------------+-------------------------------------------------------------+
| Médiane                 | 334                                                 | 438                                                         |
+-------------------------+-----------------------------------------------------+-------------------------------------------------------------+
| Mode                    | 140                                                 | 197                                                         |
+-------------------------+-----------------------------------------------------+-------------------------------------------------------------+
| Intervalle de confiance | [70 ; 1414]                                         | [92 ; 1872]                                                 |
+-------------------------+-----------------------------------------------------+-------------------------------------------------------------+
| Données brutes          | :download:`Télécharger <bataille-4-13-1000000.csv>` | :download:`Télécharger <bataille-4-13-1000000-delahay.csv>` |
+-------------------------+-----------------------------------------------------+-------------------------------------------------------------+

Remarquons également que ces statistiques diffèrent grandement de celles annoncées dans leur article : ils obtiennent une durée moyenne de 287 plis (la plus grande partie trouvée ayant 4571 plis), quand je trouve en moyenne 582 plis (la plus grande partie trouvée ayant 6955).

Plusieurs hypothèses peuvent expliquer cela :

- la description de des règles utilisées comporte une ambigüité : l'ordre dans lequel sont ramassées les cartes en cas de bataille : peut-être que mon interprétation n'est pas la bonne ;
- ils ont fait une erreur dans leurs simulations ;
- j'ai fait une erreur dans ma simulation.

À ma connaissance, ils n'ont pas publié le programme utilisé pour les simulations. Malhreusement, je serais tenté de dire que l'erreur vient de mon côté.

Usage
-----

.. argparse::
    :module: jouets.bataille.__main__
    :func: analyse
    :prog: bataille
