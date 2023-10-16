..
   Copyright 2018 Louis Paternault
   
   Cette œuvre de Louis Paternault est mise à disposition selon les termes de
   la licence Creative Commons Attribution - Partage dans les Mêmes Conditions
   4.0 International (CC-BY-SA). Le texte complet de la licence est disponible
   à l'adresse : http://creativecommons.org/licenses/by-sa/4.0/deed.fr

.. _traitementimage:

***************************************************
`traitementimage` — Logiciel de traitement d'images
***************************************************

.. currentmodule:: jouets.traitementimage

Ce module permet de réaliser quelques transformation d'images (conversion en niveaux de gris, augmentation du contraste, etc.). J'ai écrit ces fonctions pour les tester avant de les faire mettre en œuvre par mes élèves de seconde dans le cadre de l'ICN [#f1]_.

.. toctree::
   :hidden:

   traitementimage/transformations

Fonctionnalités
===============

La liste des transformations proposées est listée :ref:`par ici <traitementimage_transformations>`.

Utilisation
===========

Le module prend deux arguments : le fichier source, et le fichier de sortie. Il propose ensuite à l'utilisateur l'ensemble des transformations disponibles, avant d'appliquer la transformation choisie.

.. argparse::
    :module: jouets.traitementimage.__main__
    :func: analyse
    :prog: traitementimage

.. rubric:: Notes

.. [#f1] Informatique et Création Numérique. La séquence en question est décrite `sur mon site web <https://ababsurdo.fr/pedago/traitement-d-image>`__.
