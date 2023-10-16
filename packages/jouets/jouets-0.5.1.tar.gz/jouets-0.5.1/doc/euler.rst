..
   Copyright 2015-2019 Louis Paternault
   
   Cette œuvre de Louis Paternault est mise à disposition selon les termes de
   la licence Creative Commons Attribution - Partage dans les Mêmes Conditions
   4.0 International (CC-BY-SA). Le texte complet de la licence est disponible
   à l'adresse : http://creativecommons.org/licenses/by-sa/4.0/deed.fr

******************************************************
`euler` — Exemples d'application de la méthode d'Euler
******************************************************

La `méthode d'Euler <http://fr.wikipedia.org/wiki/Méthode_d'Euler>`_ est une
méthode permettant de calculer des solutions approchées d'équations
différentielles.

Cet outil fournit différents exemples de mise en œuvre de cette méthode.

Usage
=====

Le but de cet outil est de montrer la simplicité de la mise en œuvre de cette
méthode. Pour cette raison, les programmes sont réduits à leur strict minimum,
et ne contiennent pas d'options. Pour les appeler, lancer l'une des commandes
suivantes ::

    euler chute
    euler proiepredateur
    euler ressort
    euler satellite

Principe et Algorithme
======================

La méthode d'Euler est utilisée pour trouver une solution approchée d'une
équation différentielle. Dans toute cette page, elle permet de tracer point par
point une solution approchée de la solution.

Problème
--------

Considérons l'équation différentielle suivante :

.. math::

   \left\{\begin{array}{rcl}
   f(0)  &=& 1\\
   f'(x) &=& 0,5\times f(x)\\
   \end{array}\right.

Pour quelqu'un ayant étudié un tout petit peu les équations différentielles,
trouver la solution exacte est simple. Mais il est fréquent, en modélisant des
problèmes réels, de devoir résoudre des équations différentielles complexes,
dont on ne connaît pas de solution exacte.

Supposons que nous ne connaissions pas la solution exacte. Comment tracer la
courbe d'une solution approchée ?

Approximation
-------------

Prenons la courbe représentative d'une fonction, et sa tangente en une absicsse
:math:`a` donnée, comme sur l'exemple ci-dessous.

.. tikz:: Une courbe et une tangente
   :include: _images/euler/tangente.tikz

On remarque qu'au voisinnage de l'abscisse :math:`a`, la corube et sa tangente sont presque confondues. C'est l'approximation faite par la méthode d'Euler.

.. figure:: https://upload.wikimedia.org/wikipedia/commons/9/9e/Integration_x_div_2.png
   :align: center

   *Intégration de la fonction x/2 par la méthode d'Euler*, `Pdebart <https://commons.wikimedia.org/wiki/User:Pdebart>`_ (`source <https://commons.wikimedia.org/wiki/File:Integration_x_div_2.png>`__).


Premier exemple
---------------

Reprenons l'équation différentielle précédente.

.. math::

   \left\{\begin{array}{rcl}
   f(0) &=& 1\\
   f'(x) &=& 0,5\times f(x) \\
   \end{array}\right.

La solution est la fonction :math:`x\mapsto e^{0,5\times x}`. Supposons que nous ne connaissons pas cette réponse, et résolvons cette équation sur l'intervalle :math:`[0;1]` avec la méthode d'Euler, en traçant la courbe sur cet intervalle, avec un pas :math:`k=0,1`.

- Tout d'abord, :math:`f(0)=1`, donc la courbe passe  par le point de coordonnées :math:`(0;1)`.

- Ensuite, puisque :math:`f'(x)=0,5\times f(x)`, alors :math:`f'(0)=0,5\times f(0)=0,5`, donc l'équation de la tangente à la courbe au point d'abscisse 1 est :math:`y=0,5 x+1`. Intervient l'approximation de la méthode d'Euler : nous considérons que sur l'intervalle :math:`[0;0,1]`, la courbe de la fonction est *confondue* avec la tangente, et donc que :math:`f(0,1)=0,5\times 0,1+1=1,05`. La courbe passe donc par le point de coordonnées :math:`(0,1;1,05)`.

- Et nous répétons cette étape. Puisque :math:`f'(x)=0,5\times f(x)`, alors :math:`f'(0,1)=0,5\times f(0,1)=0,5\times 1,05=0,525`, donc l'équation de la tangente à la courbe au point d'abscisse :math:`0,1` est :math:`y=0,525x+0,9975`. Nous considérons que sur l'intervalle :math:`[0,1;0,2]`, la courbe de la fonction est *confondue* avec la tangente, donc :math:`f(0,2)=0,525\times 0,2+0,9975=1,1025`. La courbe passe donc par le point de coordonnées :math:`(0,2;1,1025)`.

Et ainsi de suite.

Les résultats obtenus sur l'intervalle :math:`[0;1]` sont visibles dans :download:`ce fichier <_images/euler/exponentielle.ods>` (arrondis à :math:`10^{-4}`), ou graphiquement sur le tracé suivant (avec en bleu, la solution exacte).

.. tikz:: Solutions exacte et approchée de l'équation différentielle.
   :include: _images/euler/exponentielle.tikz

Limites
-------

Comme on peut le voir sur le graphique précédent, l'erreur d'approximation est de plus en plus élevée. Pour améliorer cela, on peut prendre un pas plus petit, mais ce ne sera jamais parfait.

Si je me souviens bien de mes études, un autre problème de la méthode d'Euler est qu'il ne respecte pas la conservation de l'énergie. Si ce n'est pas forcément très grave pour un jeu vidéo, cela peut poser de gros problèmes au moment d'envoyer une fusée dans l'espace. D'autres méthodes sont alors plus adaptées.

Applications
============

Voici quelques applications mises en œuvre dans ce dépôt.

Chute libre avec rebond
-----------------------

La seconde loi de Newton appliquée à un objet en chute libre donne comme équation :math:`m\overrightarrow{g}=m\overrightarrow{a}`, soit plus simplement :math:`\overrightarrow{g}=\overrightarrow{a}`, ainsi, sur chacun des deux axes :math:`x` et :math:`y` (dans un plan vertical contenant la trajectoire), on a :

.. math::

   \left\{\begin{array}{rcl}
      x''(t) &=& 0\\
      y''(t) &=& -9,81\\
   \end{array}\right.

On considère en plus que lorsque l'objet atteint le sol (:math:`y<0`), la vitesse est inversée, et amortie.

La mise en œuvre en Python est donc le code suivant.

.. literalinclude:: ../jouets/euler/chute.py
   :linenos:
   :pyobject: main

Ce qui donne l'exemple de trajectoire suivant.

.. image:: _images/euler/euler-chute.png

Satellite
---------

La seconde loi de Newton appliquée au satellite d'une étoile donne comme équation :math:`\overrightarrow{P}=m\overrightarrow{a}`, soit (en ne considérant que l'intensité des forces) :math:`\frac{MG}{d^2}=a`. Ici, :math:`M` et :math:`G` (masse de l'étoile, et constante universelle de gravitation) sont constante, mais la distance :math:`d` entre les deux objets varie en fonction de la position du satellite. L'équation différentielle est donc (avec :math:`g` l'intensité de la gravité divisée par le poids, et :math:`\alpha` l'angle formé entre l'axe des abscisses, et la droite étoile-satellite) :

.. math::

   \left\{\begin{array}{rcl}
      x''(t) &=& -g\cos{\alpha}\\
      y''(t) &=& -g\sin{\alpha}\\
   \end{array}\right.

La mise en œuvre en Python est donc le code suivant (l'étoile est à l'origine du repère).

.. literalinclude:: ../jouets/euler/satellite.py
   :linenos:
   :pyobject: main

Ce qui donne l'exemple de trajectoire suivant.

.. image:: _images/euler/euler-satellite.png

Remarquons que si mes souvenirs sont bons, la solution exacte de cette équation différentielle forme une ellipse parfaite : le satillite devrait revenir exactement à son point de départ. Ce n'est pas le cas ici, à cause des approximations de cette méthode.

Ressort amorti
--------------

Dans notre système, deux forces sont exercées sur la masse :

- la force de traction (ou d'extension) du ressort, d'intensité proportionnelle à son allongement (la différence par rapport à la longueur au repos) ;
- les frottements, d'intensité proportionnelle à la vitesse.

L'équation différentielle à résoudre est donc (où :math:`k` et :math:`f` sont des constantes, ici arbitraires) :

.. math::

   -kx(t)-fx'(t)=mx''(t)

Dans ce cas, j'ai choisi de placer le temps sur l'axe des abscisses, et l'allongement sur les ordonnées.
La mise en œuvre en Python est donc le code suivant.

.. literalinclude:: ../jouets/euler/ressort.py
   :linenos:
   :pyobject: main

Ce qui donne l'exemple de trajectoire suivant.

.. image:: _images/euler/euler-ressort.png

Système proies-prédateurs
-------------------------

Lotka et Volterra ont proposé, indépendamment, un `modèle de l'évolution des populations de proies et prédateurs <https://fr.wikipedia.org/wiki/%C3%89quations_de_pr%C3%A9dation_de_Lotka-Volterra>`__. Le système d'équations à résoudre est le suivant (voir la signification des constantes dans l'article de Wikipédia cité précédemment).

.. math::

   \left\{\begin{array}{rcl}
      x'(t) &=& x(t) \times \left(\alpha - \beta  y(t) \right) \\
      y'(t) &=& y(t) \times \left(\delta  x(t) - \gamma \right)
   \end{array}\right.

La mise en œuvre en Python est donc le code suivant.

.. literalinclude:: ../jouets/euler/proiepredateur.py
   :linenos:
   :pyobject: main

Ce qui donne l'exemple de trajectoire suivant, où :

- la courbe verte est celle de la population des proies en fonction du temps ;
- la courbe rouge est celle de la population des prédateurs en fonction du temps ;
- la courbe noire est la courbe des points :math:`(x(t);y(t))`.

Nous pouvons observer un cycle.

- Au départ, les proies sont nombreuses. Les prédateurs ont beaucoup à manger, donc leur population augmente.
- Puisque la population des prédateurs augmente, ils mangent de plus en plus de proies, dont la population diminue.
- La population de proies n'est plus assez suffisante pour nourrir les prédateurs, dont la population diminue.
- Il y a moins de prédateurs, dont la population de proies augmente, ce qui ramène à la population initiale.

.. image:: _images/euler/euler-proie-predateur.png
