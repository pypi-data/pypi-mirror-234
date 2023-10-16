`chronometre` — Un chronomètre
==============================

Un chronomètre commandé par deux boutons :

- bouton `B` pour démarrer ; mettre en pause ; relancer ;
- bouton `A` pour afficher le temps de tour (afficher le temps, mais continuer mesurer le temps en arrière plan).

L'intérêt de ce programme est double :

- tester l'API concernant `boutons <https://microbit-micropython.readthedocs.io/en/v1.0.1/button.html>`__ ;
- mettre en œuvre une machine à états.

Le programme peut se trouver dans un des cinq états suivants :

- ``INITIAL`` : affiche 00, et attend l'action de l'utilisateur ;
- ``COURSE`` : mesure le temps, et affiche le nombre de secondes écoulées ;
- ``PAUSE`` : le temps écoulé est affiché, mais il ne change pas ;
- ``TOUR`` : le temps écoulé est affiché (sans changer), mais le temps continue de s'écouler en arrière-plan (utilisé pendant une course, pour afficher le temps d'un tour sans pour autant mettre le chronomètre en pause) ;
- ``DOUBLEPAUSE`` : comme l'état ``TOUR``, mais en arrière-plan, le chronomètre est en pause.

Les transitions entre les états se font suivant le graphe suivant (où les étiquettes des transitions désignent la pression des boutons).

.. tikz::
   :include: chronometre/etats.tikz

.. literalinclude:: /../microbit/chronometre.py
   :language: python
   :linenos:
