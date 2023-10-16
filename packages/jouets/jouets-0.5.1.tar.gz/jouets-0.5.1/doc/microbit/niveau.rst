`niveau` — Trace un trait horizontal
====================================

Ceci est un bon exemple de programme qui nécessite beaucoup de travail de
réflexion avec un papier et un crayon pour aboutir à un programme simple qui
tient en quelques lignes.

Le tracé de la droite horizontale se fait avec les étapes suivantes.

0. *Remarque préliminaire :* Les mathématiques faites ici manquent beaucoup de rigueur. Il y a des erreurs de signe plus ou moins volontaires ; les angles sont parfois pris par rapport à l'horizontale, parfois par rapport à la verticale ; etc. Si je construisais un avion (avec des vies en jeux), je referais proprement ces calculs ; c'est seulement une carte micro:bit, et ça à l'air de fonctionner, donc c'est bien comme ça.

1. La carte fournit l'accélération selon les axes `x`, `y` et `z`, qu'il faut
   convertir en angles. Si la carte n'est pivotée uniquement selon l'axe `x`, la gravité est proportionnelle au cosinus de l'angle (où 0 est l'horizontale). Malheureusement, la carte est aussi pivotée selon les deux autres axes, donc c'est un peu plus compliqué…

   J'ai trouvé dans ces deux articles (`ici <https://www.digikey.com/en/articles/techzone/2011/may/using-an-accelerometer-for-inclination-sensing>`__ et `là <https://www.nxp.com/files-static/sensors/doc/app_note/AN3461.pdf>`__) ces formules, qui convertissent l'accélération en inclinaison (en radians, où `atan2 <https://fr.wikipedia.org/wiki/Atan2>`__ est une variante de la fonction `arc tangente` qui donne un angle entre :math:`-\pi` et :math:`\pi` (au lieu de :math:`-\frac{\pi}{2}` et :math:`\frac{\pi}{2}`).

   .. math::

      \begin{array}{rcl}
         angleX &=& \operatorname{atan2}\left(-x, z\right)\\
         angleY &=& \operatorname{atan2}\left(-y, z\right)\\
      \end{array}

3. Au lieu d'incliner la carte, dans mes calculs, j'incline le plan horizontal selon les axes `x` et `y`. La droite marquant l'horizontale est donc l'intersection du plan horizontal avec le plan de la carte.

   - Le plan de la carte est celui d'équation :math:`z=0`.
   - Le plan de l'horizontale, qui a été incliné selon des angles :math:`angleX` et :math:`angleY` est le plan passant par les trois points de coordonnées :
     :math:`\left(0 ;0 ;0 \right)`,
     :math:`\left(\cos angleX ; 0 ; \sin angleX \right)`,
     :math:`\left(0 ; \cos angleY ; \sin angleY \right)`.

   L'équation de la droite est donc :

   .. math::

      \sin(angleX) \times \cos(angleY) + \cos(angleX) \times \sin(angleY) = 0

4. Enfin, le tracé de la droite se fait dans la fonction :func:`tracedroite` (qui prend en argument les coefficients `a` et `b` de l'équation cartésienne `ax+by=0` ; il n'y a pas de constante `c` puisque la droite passe par l'origine).

   Selon le coefficient directeur de la droite (dont la valeur absolue est plus grande ou plus petite que 1), on calcule, pour chaque valeur de `x` (ou de `y`), la valeur de l'autre coordonnées correspondante en utilisant l'équation. Ceci est fait avec un décalage de 2 sur chacun des deux axes, puisque dans nos calculs, la droite passe par l'origine, alors que sur la carte, elle passe par le pixel de coordonnées :math:`(2;2)`.

5. C'est un peu cracra. Il y a la moitié de ce raisonnement que je comprends à moitié. Il y a des incohérences (notamment les angles dont le 0 est l'horizontale ou la verticale, selon les cas). Mais ça marche.

.. literalinclude:: /../microbit/niveau.py
   :language: python
   :linenos:
