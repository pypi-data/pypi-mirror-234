.. _anagrammes:

*************************************
`anagrammes` — Recherche d'anagrammes
*************************************

.. currentmodule:: jouets.anagrammes

.. note::

    Pour chercher le groupes de lettres fournissant le plus grand nombre d'anagrammes, voir :ref:`anagramme_clique`.

Cet utilitaire permet de rechercher des anagrammes.

J'ai pu ainsi découvrir que *« postulat lunaire »* est une anagramme de mes prénom et nom.

.. toctree::
   :hidden:

   anagrammes/clique

.. contents::
   :local:
   :depth: 1

Structure de données
====================

.. epigraph::

   Data dominates.  If you've chosen the right data structures and organized things well, the algorithms will almost always be self­evident.  Data structures, not algorithms, are central to programming.

   -- Rob Pike [Pike1989]_

.. note::

   Le détail de ces classes est décrit dans la partie dédiée : :ref:`api-anagrammes`.

Le dictionnaire des mots valides est stocké sous la forme d'un arbre, qui est :ref:`décrit plus loin <dictionnairearborescent>`. Commençons par définir deux classes qui seront utilisées par la suite.

Classes diverses
----------------

.. testsetup:: *

   from jouets.anagrammes import Alphabet
   from jouets.anagrammes import Intervalle
   import math

La classe :class:`Alphabet` définit un ensemble de lettres, avec répétition. Il est possible de soustraire un caractère à un tel objet :

.. doctest::

   >>> alpha = Alphabet("aabc")
   >>> alpha - "b"
   Alphabet("aac")

La classe :class:`Intervalle` définit un intervalle. Ajouter (ou soustraire) un nombre à un intervalle applique l'opération deux deux bornes.

.. doctest::

   >>> Intervalle(1, 2) + 5
   Intervalle(6, 7)
   >>> Intervalle(-math.inf, 2) + 5
   Intervalle(-math.inf, 7)


.. _dictionnairearborescent:

Dictionnaire arborescent
------------------------

Un :class:`DictionnaireArborescent` est stocké sous la forme suivante.

.. graphviz:: anagrammes/dictionnaire.dot

Chaque nœud contient un dictionnaire (un :class:`dict` au sens de la bibliothèque standard) dont les clefs sont les lettres, et les valeurs sont elles-mêmes des dictionnaires arborescent qui représentent les suffixes. Dans l'exemple illustré ci-dessus, en appellant ``NE`` le dictionnaire correspondant au préfixe `ne` :

- ``NE["z"]`` est le dictionnaire arborescent qui contient le mot `z` ;
- ``NE["t"]`` est le dictionnaire arborescent qui contient le mot `tte`.

De plus, chaque :class:`DictionnaireArborescent` a un attribut :attr:`DictionnaireArborescent.mot`, qui est un booléen qui vaut `True` si et seulement si le nœud correspondant est un mot valide. Dans l'exemple ci-dessus, de tels nœuds sont représentés par des doubles cercles.

Algorithme
==========

Sans contraintes
----------------

L'algorithme de recherche d'une unique anagramme (chercher les mots constitués d'exactement les lettres données en argument) ressemblerait à ceci.

.. code-block:: python

   def anagramme(self, alphabet):
      # Le nœud courant est un mot, et toutes les lettres ont été consommées
      if self.mot and not alphabet:
         yield ""

      # Pour chacun des suffixes (qui commencent par une lettre disponible), faire :
      for lettre in self.suffixes:
         if lettre not in alphabet:
            continue

         # Rechercher les anagrammes de l'alphabet (auquel on a retiré la lettre courante) dans les suffixes.
         for suffixe in self.suffixes[lettre].anagramme(alphabet - lettre):
            yield lettre + suffixe

Avec contraintes
----------------

L'algorithme est en fait un peu plus compliqué que cela, à cause des deux contraintes suivantes :

- la taille des mots peut être limitée ;
- le nombre de mots retourné peut être limité (il est possible de renvoyer, par exemple, un triplet de mots qui utilisent toutes les lettres demandées au lieu d'un simple mot).

La première méthode, :meth:`DictionnaireArborescent._anagrammes`, recherche *une seule* anagramme des lettres de l'alphabet demandé. Par contre, elle n'itère pas simplement sur cette anagramme, mais sur le couple ``(mot, reste)``, où ``mot`` est le mot trouvé, et ``reste`` est :class:`l'alphabet <Alphabet>` des lettres inutilisées, qui pourront être utilisées, plus tard, pour former d'autres mots.

Puisque plusieurs mots peuvent être trouvés, il y a un risque de chercher plusieurs fois les mêmes mots. Par exemple, en cherchant les anagrammes de `chienne`, on pourra trouver d'abord `chien` et `ne`, puis `ne` et `chien`. C'est une perte de temps. Pour remédier à cela, un autre argument est passé à cette méthode : ``apres``. Cet argument signifie que l'on ne recherche que des mots situés *après* cet argument dans l'ordre lexicographique du dictionnaire (ou il est simplement ignoré s'il vaut ``None``). Cela assure deux choses :

- les ensembles de mots trouvés le seront dans l'ordre alphabétique (par exemple `chien` et `ne`, plutôt que `ne` et `chien`) ;
- plus important : chaque ensemble de mots ne sera cherché et trouvé qu'une seule fois.

.. literalinclude:: ../jouets/anagrammes/__init__.py
    :linenos:
    :pyobject: DictionnaireArborescent._anagrammes

Une fois que cette fonction de recherche *d'un seul* mot a été défini, nous pouvons rechercher plusieurs mots. Le principe est qu'après avoir cherché un mot, nous recherchons des anagrammes parmi les lettres restantes (en respectant les contraintes).

.. literalinclude:: ../jouets/anagrammes/__init__.py
    :linenos:
    :pyobject: DictionnaireArborescent._multi_anagrammes

Interface en ligne de commandes
===============================

Recherche simple
----------------

Ce module permet d'effectuer une recherche à la fois. La commande suivante va lister les anagrammes :

- ``--dict aspell://fr`` : constitués de mots français (en utilisant le dictionnaire aspell, s'il est installé) ;
- ``--mots 2`` : en deux mots ;
- ``--lettres 3:`` : chacun des mots ayant au moins trois lettres ;
- ``Boris Vian`` : en utilisant ces lettres pour construire l'anagramme.

.. code-block:: shell

   $ anagrammes search --dict aspell://fr --mots 2 --lettres 3: Boris Vian
   …
   bison ravi
   …

.. argparse::
    :module: jouets.anagrammes.__main__
    :func: analyse_search
    :prog: anagrammes

Shell interactif
----------------

Le chargement d'un dictionnaire peut être assez long. Un shell permet de charger le dictionnaire une fois pour toute, et d'effectuer par la suite plusieurs recherche. Voici un exemple d'exécution arrivant au même résultat que la commande utilisée plus haut.

.. code-block:: shell

   $ anagrammes shell
   Recherche d'anagrammes : shell.
   Tapez `help` pour afficher l'aide.
   > load aspell://fr
   > option mots 2
   > option lettres 3:
   > search Boris Vian
   …
   bison ravi
   …
   > exit
   INFO:root:Terminé…

Notes et Références
===================

.. [Pike1989] Rob Pike, *Notes on Programming in C*, 1989. http://www.lysator.liu.se/c/pikestyle.html
