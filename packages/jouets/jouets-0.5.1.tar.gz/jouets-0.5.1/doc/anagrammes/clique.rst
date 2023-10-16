.. _anagramme_clique:

============================================================================
Recherche du groupe de lettres fournissant le plus grand nombre d'anagrammes
============================================================================

.. currentmodule:: jouets.anagrammes

.. contents::
   :local:
   :depth: 1

Algorithme
==========

Pour répondre à ce problème, nous allons d'abord construire un dictionnaire dont :

- les clefs sont des ensembles de lettres (triées par ordre croissant) ;
- les valeurs sont l'ensemble des mots pouvant être formés avec ce groupe de lettres.

Ceci va donner un dictionnaire du genre ::

    {
      "aimr": {"mari", "rima"},
      "cehin": {"chien", "chine", "niche"},
    }

Ce dictionnaire se construit avec le code suivant (le vrai code est un chouïa plus compliqué, puisque cet exemple ne tient pas compte des arguments ``accents`` et ``majuscules``)::

    groupes = collections.defaultdict(set)
    for mot in dictionnaire:
        clef = "".join(sorted(mot))
        groupes[clef].add(mot)

Remarquons qu'en utilisant un :class:`collections.defaultdict`, nous n'avons même pas à initialiser une valeur avec un ensemble vide si la clef est rencontrée pour la première fois.

Il suffit ensuite de rechercher, dans ce dictionnaire, quel est le groupe de mots le plus grand. Ceci ce fait par un simple parcours des clefs.

Résultats
=========

Les listes de mots utilisées ici sont celles fournies avec le dictionnaire `aspell <http://aspell.net/>`__, sous Debian.

Français
--------

Accepter ou non les noms propres (avec l'option ``majuscules``) ne modifie pas les résultats. Nous obtenons :

- En ignorant les accents, il est possible de former 19 mots avec les mêmes lettres :

    arisent
    entrais
    insérât
    ratines
    ratinés
    rentais
    riantes
    résinât
    satiner
    sentira
    serinât
    sériant
    taniser
    tarsien
    traines
    transie
    traînes
    traînés
    tsarine

- En tentant compte des accents, il est possible de former 13 mots avec les mêmes lettres :

    ratisse
    restais
    retissa
    satires
    staries
    starise
    tarisse
    tersais
    tirasse
    tiseras
    tissera
    tressai
    triasse

Anglais
-------

Sans surprise, tenir compte ou non des accents ne change rien en langue anglaise.

- Sans les noms propres, il est possible de former 8 anagrammes avec le même ensemble de lettres :

    aster
    rates
    resat
    stare
    tares
    taser
    tears
    treas

- Avec les noms propres, il est possible de former 8 anagrammes avec le même ensemble de lettres, de trois manières différentes.

    Gore
    Oreg
    Roeg
    ergo
    goer
    gore
    ogre
    rego

    aster
    rates
    resat
    stare
    tares
    taser
    tears
    treas

    Stael
    Tesla
    least
    slate
    stale
    steal
    tales
    teals


Ligne de commande
=================

.. argparse::
    :module: jouets.anagrammes.clique
    :func: analyseur
    :prog: anagrammes.clique
