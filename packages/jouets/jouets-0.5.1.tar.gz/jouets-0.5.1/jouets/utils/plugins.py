# Copyright 2014-2023 Louis Paternault
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

"""Facilite la définition et l'utilisation de plugins."""

import importlib
import inspect
import pkgutil
import re


def iter_modules(package, *, ignore=None, recursive=False):
    """Itérateur sur tous les sous-modules de celui donné en argument.

    :param list ignore: Liste de chaînes de caractères.
        Les modules qui correspondent à ces expressions régulières sont ignorées.
    :param boolean recursive: La recherche est-elle récursive ?
        Si non, elle s'arrête au premier niveau.
    """
    if ignore is None:
        ignore = []
    else:
        ignore = [re.compile(item) for item in ignore]

    for __finder, name, ispkg in pkgutil.iter_modules(
        package.__path__, package.__name__ + "."
    ):
        if any(regexp.match(name) for regexp in ignore):
            continue
        newpackage = importlib.import_module(name)
        yield newpackage
        if ispkg:
            yield from iter_modules(newpackage, ignore=ignore, recursive=recursive)


def iter_classes(package, classe, *, recursive=False):
    """Itérateur sur toutes les classes d'un sous-module de `package` héritant de `classe`.

    Ignore les classes dont le nom commence par `_`, ainsi que `classe` elle-même.

    :param boolean recursive: La recherche est-elle récursive ?
        Si non, elle s'arrête au premier niveau.
    """
    for module in iter_modules(package, recursive=recursive):
        for name in dir(module):
            if name.startswith("_"):
                continue
            obj = getattr(module, name)
            if obj is classe:
                continue
            if inspect.isclass(obj) and issubclass(obj, classe):
                yield obj


def get_description(obj):
    """Renvoit la description d'un objet.

    La description est la première ligne de la docstring.
    Si l'objet n'a pas de docstring, renvoit la chaîne vide.
    """
    try:
        return obj.__doc__.strip().split("\n")[0]
    except AttributeError:  # Pas d'attribut `__doc__`
        return ""
