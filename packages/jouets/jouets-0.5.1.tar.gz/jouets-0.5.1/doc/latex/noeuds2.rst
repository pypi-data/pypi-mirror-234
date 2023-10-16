`LaTeX` — Quelques explications pour les nœuds (deuxième version)
=================================================================

Voici comment est construit le nœud suivant (sur la base d'un pentagone).

.. image:: noeuds2-explications-05.png

Ces explications ne présentent que les grandes lignes. Le reste est laissé au lecteur patient : il faut un peu de trigonométrie et de coordonnées polaires.

#. D'abord, le pentagone intérieur est tracé, ainsi qu'une partie du pentagone extérieur. Notons que chaque segment du (presque) pentagone extérieur est tracé à une distance :math:`e` (l'épaisseur) du pentagone intérieur, perpendiculairement. Cela est fait en ajoutant des coordonnées polaires en TikZ.

   .. image:: noeuds2-explications-01.png

#. Puis les coordonnées de l'extérieur de la forme sont calculées, en prenant la moyenne des angles des deux sommets correspondant (c'est-à-dire le sommet de départ, auquel on ajoute la moitié du saut). À ce stade, on obtient la forme demandée, mais la courbe a des « angles ».

   .. image:: noeuds2-explications-02.png

#. Pour arrondir ces angles, des courbes de Bézier sont utilisées (notation ``.. controls`` de TikZ), avec les tangentes suivantes (les « points de contrôle » sont les extrémités de chaque tangente). La figure est terminée, sauf que certains brins devraient passer en dessous des autres.

   .. image:: noeuds2-explications-03.png

#. Pour cela, la courbe est dessinée en deux fois : d'abord la partie bleue, qui va être ensuite recouverte par la partie rouge.

   .. image:: noeuds2-explications-04.png

#. Et voilà ! Le travail est fait.

   .. image:: noeuds2-explications-05.png
