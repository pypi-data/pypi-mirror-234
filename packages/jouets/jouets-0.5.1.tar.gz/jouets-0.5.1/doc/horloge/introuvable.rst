*******************************************
`horloge.introuvable` — Horloge introuvable
*******************************************

.. currentmodule:: jouets.horloge.introuvable

Dans son *Catalogue d'objets introuvables* [Carelman]_, Carelman propose des objets loufoques, dont la *montre à chiffres mélangés*.

Ce programme produit de telles montres.

.. figure:: ../_images/horloge/introuvable/horloge1.png
  :width: 250px
  :align: left

.. figure:: ../_images/horloge/introuvable/horloge2.png
  :width: 250px
  :align: right

.. contents::
   :local:
   :depth: 1

Fonctionnement
==============

Le fonctionnement est assez simple : j'ai un dictionnaire ``heures2angles`` dont :

- les clefs sont les heures ;
- les valeurs sont les angles où sont positionnées cette heure.

Par exemple, ``heures2angles[4] == 120`` signifie que le nombre 4 sur l'horloge est situé à un angle de 120°.

Supposons ensuite qu'il soit 12h34'56'' (12 heures, 34 minutes et 56 secondes). Pour chaque aiguille, on calcule la valeur correspondante en secondes, ainsi que le total (le nombre de secondes écoulées lorsque l'aiguille a parcouru un tour complet).

- secondes : :math:`56` ;
- minutes : :math:`34×60+56` ;
- heures : :math:`0×60×60 + 34×60 + 56` (12h correspond à 0h sur notre horloge).

Il faut ensuite savoir entre quels nombres (de 1 à 12, ou plutôt de 0 à 11) se trouvent chacune de ces proportions. C'est un simple calcul de proportionnalité. Par exemple pour les minutes :

======== =====
Portion  Total
======== =====
34×60+56 60×60
?        12
======== =====

Nous obtenons ici :math:`\frac{(34×60+56)×12}{60×60}\approx6,987`.
L'aiguille des minutes sera donc située quelque part entre les nombres 6 et 7.

Pour connaître la position exacte, c'est une question de fonction affine. Supposons que sur notre horloge, le 6 soit situé à 120°, et le 7 à 30°. Nous cherchons alors une fonction affine :math:`f` telle que :
:math:`f(6)=120` et :math:`f(7)=30`. L'angle de l'aiguille des minutes sera alors :math:`f(6,987)`. Et voilà !

Une subtilité éludée ici est ce qu'il se passe lorsque ce calcul fait passer par le chemin le plus long. Typiquement, si le chiffre 6 est à 330°, et le 7 à 30°. Avec notre calcul, entre 6h et 7h, l'angle de l'aiguille des heures parcourra presque tout le cadrant, son angle décroissant de 330° jusqu'à 30°, alors que cet angle devrait *augmenter* de 330° à 360° (c'est-à-dire 0°), puis ensuite augmenter de 0° à 30°. La solution trouvée est alors de détecter lorsque la différence d'angles est supérieure à 180°, et modifier alors un des deux angles (plus ou moins 360°) pour réduire cette différence à une valeur acceptable.

Toute ceci est fait dans la méthode ``Horloge.angle()`` :

.. literalinclude:: ../../jouets/horloge/introuvable/__init__.py
    :linenos:
    :pyobject: Horloge.angle

Ligne de commande
=================

.. argparse::
    :module: jouets.horloge.introuvable.__main__
    :func: analyse
    :prog: horloge.introuvable

Notes et Références
===================

.. [Carelman] Jacques Carelman, *Catalogue d'objets introuvables*, Le Livre de Poche, 1996.
