# Copyright 2018-2023 Louis Paternault
#
# This file is part of Jouets.
#
# Jouets is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Jouets is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Jouets.  If not, see <http://www.gnu.org/licenses/>.

"""Gestion des simulations sauvegardées."""

import csv
import functools
import glob
import os

from .aargparse import yesno

CACHEDIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "doc", "{module}")
)

FORCEREADCACHE = yesno(os.environ.get("FORCEREADCACHE", "non"))
WRITECACHE = yesno(os.environ.get("WRITECACHE", "non"))


def format_stars(string, **kwargs):
    """Renvoit une chaîne de caractère dans laquelle tous les `{}` sont remplacés par des étoiles.

    Ceci fonctionne si les toutes les valeurs à remplacée sont de la forme ``{toto}``
    (sans autre indication de mise en forme).
    """
    try:
        return string.format(**kwargs)
    except KeyError as error:
        kwargs[error.args[0]] = "*"
        return format_stars(string, **kwargs)


class Cache:
    """Mise en cache des données de simulation.

    Un argument ``**kwargs`` est donné dans plusieurs méthodes.
    Il correspond aux arguments donnés à la simulation,
    et permet d'identifier les données mises en cache :
    si une simulation est appelée avec comme argument un ``**kwargs`` déjà présent dans le cache,
    les données mises en cache sont renvoyées à la place.
    """

    # pylint: disable=too-few-public-methods

    module = None
    cachename = None

    @classmethod
    def est_sauvegardee(cls, **kwargs):
        """Renvoit un booléen signifiant si cette simulation a été sauvegardée ou non.

        L'argument `kwargs` est le même que celui décrit dans la classe :class:`Cache`.
        """
        raise NotImplementedError()

    @classmethod
    def read_cache(cls, **kwargs):
        """Lit et renvoit les données depuis le cache.

        L'argument `kwargs` est le même que celui décrit dans la classe :class:`Cache`.
        """
        raise NotImplementedError()

    @classmethod
    def write_cache(cls, data, **kwargs):
        """Écrit les données dans le cache (qui est sensé exister).

        L'argument `kwargs` est le même que celui décrit dans la classe :class:`Cache`.
        """
        raise NotImplementedError()

    @classmethod
    def intercepte(cls):
        """Décorateur pour ne pas re-calculer une simulation sauvegardée."""

        def decorateur(fonction):
            @functools.wraps(fonction)
            def wrapper(**kwargs):
                if cls.est_sauvegardee(**kwargs) or FORCEREADCACHE:
                    return cls.read_cache(**kwargs)
                data = fonction(**kwargs)
                if WRITECACHE:
                    cls.write_cache(data, **kwargs)
                return data

            return wrapper

        return decorateur


class AllInOneCache(Cache):
    """Cache dans lequel toutes les données sont sauvegardées dans un seul fichier."""

    @classmethod
    def fichier(cls):
        """Renvoit le nom du fichier contenant le cache.

        Ce fichier peut ne pas exister.
        """
        return os.path.join(CACHEDIR.format(module=cls.module), cls.cachename)

    @classmethod
    def opencache(cls):
        """Ouvre le fichier de cache, et renvoit la liste des lignes.

        Si le fichier n'existe pas, renvoit une liste vide.
        """
        try:
            with open(cls.fichier(), encoding="utf8") as csvfile:
                reader = csv.reader(csvfile, delimiter=",")
                return list(reader)
        except FileNotFoundError:
            return []

    @classmethod
    def est_sauvegardee(cls, **kwargs):
        """Renvoit un booléen signifiant si cette simulation a été sauvegardée ou non.

        L'argument `kwargs` est le même que celui décrit dans la classe :class:`Cache`.
        """
        for row in cls.opencache():
            if row[: len(kwargs)] == [
                str(value) for key, value in sorted(kwargs.items())
            ]:
                return True
        return False

    @classmethod
    def write_cache(cls, data, **kwargs):
        """Écrit les données dans le cache (qui est sensé exister).

        L'argument `kwargs` est le même que celui décrit dans la classe :class:`Cache`.
        """
        cache = list(cls.opencache())
        cache.append(
            [str(value) for key, value in sorted(kwargs.items())] + cls.data2row(data)
        )
        with open(cls.fichier(), mode="w", encoding="utf8") as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            for row in sorted(cache):
                writer.writerow(row)

    @classmethod
    def data2row(cls, data):
        """Convertit des données en un format inscriptible dans une ligne d'un fichier CSV."""
        raise NotImplementedError()

    @classmethod
    def row2data(cls, row):
        """Convertit une ligne lue depuis le fichier CSV en donnée mise en cache.

        Ceci permet d'obtenir les données au bon format.
        """
        raise NotImplementedError()

    @classmethod
    def read_cache(cls, **kwargs):
        """Lit et renvoit les données depuis le cache.

        L'argument `kwargs` est le même que celui décrit dans la classe :class:`Cache`.
        """
        for row in cls.opencache():
            if row[: len(kwargs)] == [
                str(value) for key, value in sorted(kwargs.items())
            ]:
                return cls.row2data(row[len(kwargs) :])
        raise KeyError("Les données n'ont pas été trouvées dans le cache.")


class SeveralFilesCache(Cache):
    """Cache dans lequel un fichier est utilisé par donnée mise en cache."""

    @classmethod
    def lscache(cls, _):
        """Affiche la liste des simulations disponibles dans le cache."""
        for nom in glob.glob(cls.fichier(format_stars(cls.cachename))):
            print(os.path.basename(nom[: -len(".csv")]))

    @classmethod
    def fichier(cls, cachename):
        """Retourne le nom du fichier contenant la simulation.

        Cette fonction fonctionne, que le fichier existe ou non.
        """
        return os.path.join(CACHEDIR.format(module=cls.module), cachename)

    @classmethod
    def est_sauvegardee(cls, **kwargs):
        """Renvoit un booléen signifiant si cette simulation a été sauvegardée ou non.

        L'argument `kwargs` est le même que celui décrit dans la classe :class:`Cache`.
        """
        return os.path.exists(cls.fichier(cls.cachename.format(**kwargs)))

    @classmethod
    def read_cache(cls, **kwargs):
        """Lit et renvoit les données depuis le cache.

        L'argument `kwargs` est le même que celui décrit dans la classe :class:`Cache`.
        """
        raise NotImplementedError()

    @classmethod
    def write_cache(cls, data, **kwargs):
        """Écrit les données dans le cache (qui est sensé exister).

        L'argument `kwargs` est le même que celui décrit dans la classe :class:`Cache`.
        """
        raise NotImplementedError()
