#!/usr/bin/env python3

# Copyright 2014-2017 Louis Paternault
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

"""Analyseur de ligne de commandes pour fractales."""

from jouets.utils.aargparse import analyseur

from . import VERSION

PREDEFINED = {"koch": [0, 60, -120, 60]}


def analyse():
    """Renvoie un analyseur de ligne de commande"""
    parser = analyseur(VERSION, prog="fractale")

    parser.add_argument("-f", "--fast", action="store_true", help="Fast drawing.")

    parser.add_argument(
        "-t",
        "--type",
        metavar="NAME",
        action="store",
        choices=PREDEFINED.keys(),
        help="Predefined fractals: 'koch': Koch snowflake,",
    )

    parser.add_argument(
        "angles",
        metavar="angle",
        type=int,
        nargs="*",
        help="Angles of the base drawing of the frarctal.",
    )

    return parser
