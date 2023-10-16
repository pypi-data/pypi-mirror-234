`LaTeX` — Quelques explications pour les nœuds (première version)
=================================================================

Voici comment est construit le nœud suivant.

.. image:: noeuds1-03.svg

Le prodécé est illustré sur l'illustration suivantes.

.. image:: noeuds1-explications-01.png

1. Comme pour :ref:`l'étoile <latex_etoiles>`, un polyèdre régulier est construit sur le cercle trigonométrique en utilisant les coordonnées polaires (petit pentagone en noir sur la figure).

2. Puis un second polygone est construit, plus grand que le premier, en respectant l'épaisseur donnée en argument. Ce second polygone est tronqué pour que le raccord des cercles (étape suivante) se fasse correctement.

3. Des arcs de cercle sont tracés pour relier ces différents segments.

4. Enfin, pour que le nœud apparaisse certaines parties de la figure viennent en recouvrir d'autres. Pour cela, le remplissage est fait en deux étapes :

   - d'abord les parties rouges ;
   - puis les parties bleues, qui viennent recouvrir les parties rouge.

Bon courage pour décortiquer les mathématiques derrière tout ça (les *math* ne sont pas si complexes, mais comprendre mon code non documenté l'est beaucoup plus) !

