Jouets 🎲 Programmes « amusants » à connotation mathématique ou informatique
============================================================================

Ces programmes n'ont pas ou peu d'utilité pratique, si ce n'est mettre en œuvre
des concepts des deux disciplines.

Les programmes sont :

- `addition <http://jouets.ababsurdo.fr/fr/latest/addition>`_ : Recherche de solutions d'une énigme
- `anagrammes <http://jouets.ababsurdo.fr/fr/latest/anagrammes>`_ : Recherche d'anagrammes
- `aperitif <http://jouets.ababsurdo.fr/fr/latest/aperitif>`_ : Recherche de solutions au problème des apéritifs
- `attente <http://jouets.ababsurdo.fr/fr/latest/attente>`_ : Simulation de files d'attente
- `azul <http://jouets.ababsurdo.fr/fr/latest/azul>`_ : Calcul du score maximal à `Azul <https://www.trictrac.net/jeu-de-societe/azul>`__
- `attente <http://jouets.ababsurdo.fr/fr/latest/attente>`_ : Simulateur de files d'attente.
- `bataille <http://jouets.ababsurdo.fr/fr/latest/bataille>`_ : Analyse de la durée d'une partie de bataille
- `cellulaire <http://jouets.ababsurdo.fr/fr/latest/cellulaire>`_ : Automates cellulaires
- `chemin <http://jouets.ababsurdo.fr/fr/latest/chemin>`_ : Recherche du score maximal d’un jeu
- `dobble <http://jouets.ababsurdo.fr/fr/latest/dobble>`_ : Création de jeu de cartes de Dobble
- `egyptienne <http://jouets.ababsurdo.fr/fr/latest/egyptienne>`_ : Décomposition en fractions égyptiennes
- `erathostene <http://jouets.ababsurdo.fr/fr/latest/erathostene>`_ : Crible d’Érathostène optimisé en espace
- `fractale <http://jouets.ababsurdo.fr/fr/latest/fractale>`_ : Tracé de fractale itératif et infini
- `horloge <http://jouets.ababsurdo.fr/fr/latest/horloge>`_ : Quelques horloges
- `labyrinthe <http://jouets.ababsurdo.fr/fr/latest/labyrinthe>`_ : Construction de labyrinthes
- `latex <http://jouets.ababsurdo.fr/fr/latest/latex>`_ : Bouts de codes amusants en LaTeX
- `mafia <http://jouets.ababsurdo.fr/fr/latest/mafia>`_ : Calcul de probabilités de victoire au jeu de `mafia <https://fr.wikipedia.org/wiki/Mafia_%28jeu%29>`__
- `microbit <http://jouets.ababsurdo.fr/fr/latest/microbit>`_ : Quelques programmes pour cartes `micro:bit <http://microbit.org>`__.
- `peste et choléra <http://jouets.ababsurdo.fr/fr/latest/peste>`_ : Simulation de propagation d'épidémies
- `pygame <http://jouets.ababsurdo.fr/fr/latest/pygame>`_ : Quelques jeux réalisés avec `pygame <http://pygame.org/>`__, pour tester des choses pour l'enseignement de l'ICN et ISN.
- `sudoku <http://jouets.ababsurdo.fr/fr/latest/sudoku>`_ : Solveur de sudoku
- `traitementimage <http://jouets.ababsurdo.fr/fr/latest/traitementimage>`_ : Logiciel de traitement d'image
- `truchet <http://jouets.ababsurdo.fr/fr/latest/truchet>`_ : Génération de tuiles de Truchet généralisées
- `verger <http://jouets.ababsurdo.fr/fr/latest/verger>`_ : Calcul de la probabilité de victoire au jeu du `verger <https://www.haba.de/fr_FR/le-verger--003170>`__.
- d'autres `en cours <https://framagit.org/spalax/jouets/merge_requests?label_name=id%C3%A9e>`_ ou `en projet <https://framagit.org/spalax/jouets/issues?label_name=id%C3%A9e>`_ …

Quoi de neuf ?
--------------

Voir le `journal des modifications <https://framagit.org/spalax/jouets/blob/main/CHANGELOG.md>`_.

Documentation
-------------

* `Voir la version compilée <https://jouets.ababsurdo.fr>`_.

* Pour la compiler depuis les sources, télécharger le paquet, et lancer::

      cd doc && make html

Téléchargement, installation et exécution
-----------------------------------------

Voir à la fin de la liste pour une installation par un paquet Debian.

* Depuis les sources :

  * Téléchargement : https://pypi.python.org/pypi/jouets
  * Installation (dans un `virtualenv`, pour éviter les conflits avec le
    gestionnaire de paquets de votre distribution)::

        python3 -m pip install .

* Avec `pip`::

    pip install jouets

* Pour utiliser les programmes sans les installer, il suffit de les exécuter
  depuis la racine du projet. Par exemple ::

      ./bin/erathostene

* Paquet Debian (et Ubuntu ?) rapide :

  Cela nécessite l'installation de `stdeb <https://github.com/astraw/stdeb>`_ ::

      python3 setup.py --command-packages=stdeb.command bdist_deb
      sudo dpkg -i deb_dist/jouets-<VERSION>_all.deb
