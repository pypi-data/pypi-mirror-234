.. _latex_etoiles:

`LaTeX` — Quelques explications pour l'étoile
=============================================

Voici comment sont construites les étoiles suivantes : |etoiles03| |etoiles04|.

.. |etoiles03| image:: etoiles-03.svg

.. |etoiles04| image:: etoiles-04.svg

1. Prenons d'abord le cercle trigonométrie, et plaçons les septs sommets d'un polygone régulier à sept branches (en prenant les points de coordonnées polaires :math:`(1 ; 360k/7)` (pour :math:`k` allant de 0 à 6).

   .. image:: etoiles-explications-01.png

2. À partir de là, pour l'étoile avec un *décalage* de 2 (``\etoile{1}{7}{2}``), chaque sommet est relié au deuxième sommet dans le sens horaire.

   .. figure:: etoiles-explications-02.png

3. Et pour l'étoile avec un *décalage* de 3 (``\etoile{1}{7}{3}``), chaque sommet est relié au troisième dans le sens horaire.

   .. figure:: etoiles-explications-03.png

4. Il ne reste plus qu'à calculer les positions des intersections de ces segments, pour ne pas tracer les segments intérieurs, et le tour est joué.

J'ai écrit ce code il y a plusieurs années, donc je ne me souviens plus des détails de calcul, et j'ai la flemme de refaire les calculs (et les figures qui vont avec). Bon courage !
