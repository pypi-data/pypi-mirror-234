`memoire` — Un jeu de mémoire
=============================

Dans ce jeu, l'utilisateur se voit présenter une suite de directions aléatoires (haut, bas, gauche, droite), et doit ensuite la reproduire en inclinant la carte dans les directions proposées, dans le bon ordre. À chaque fais qu'il réussit, un nouvel élément est ajouté à la liste.

L'algorithme est composé de trois boucles imbriquées.

- Chaque passage dans la boucle extérieure correspond à une nouvelle partie.
- Chaque passage dans la boucle intermédiaire correspond à une nouvelle manche (l'affichage d'une suite à mémoriser, et la lecture de la suite proposée par l'utilisateur) ;
- Chaque passage dans la boucle intérieure correspond à la lecture de la suite proposée par l'utilisateur.

La sortie d'une boucle se fait uniquement avec l'instruction ``break``.

L'algorithme en pseudo-code ressemble à ceci.

.. code-block:: none

   while True:

      Attendre que l'utilisateur secoue la carte.

      Initialisation de la partie

      while True:

         Ajout d'une direction à la liste
         Affichage de la liste des directions

         while True:

            Lecture de la liste des directions, en vérifiant la validité au fur et à mesure.
            Si toute la liste est lue, ou qu'une erreur est détectée:
               break

         Si toute la liste a été lue:
            Afficher ☺️
         Sinon
            break

      # Perdu…
      Afficher 💀

Et le vrai code est le suivant.

.. literalinclude:: /../microbit/memoire.py
   :language: python
   :linenos:
