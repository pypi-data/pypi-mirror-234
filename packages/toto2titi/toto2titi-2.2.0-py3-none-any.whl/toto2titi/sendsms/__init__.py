# Copyright 2021 Louis Paternault
#
# This file is part of Toto2Titi.
#
# Toto2Titi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Toto2Titi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Toto2Titi.  If not, see <https://www.gnu.org/licenses/>.

"""Define functions to sens SMS."""

import importlib
import logging

from .. import T2TException, read_config

APPNAME = "sendsms"


def sendsms(content, *, config=None):
    """Send SMS using the provider given in configuration.

    If no configuration file is given, read it using :func:`read_config`.

    :param str content: Message to be sent.
    :param configparser.ConfigParser config: Configuration, as described in :ref:`configfile`.
    :raises T2TException:
       If an error occured: incomplete configuration file, error while sending the message…
    """
    if config is None:
        config = read_config(APPNAME)
    try:
        provider = config["general"]["smsprovider"]
    except KeyError as error:
        raise T2TException(
            "No cellphone provider given in configuration file.", level=logging.ERROR
        ) from error
    module = importlib.import_module(f".provider.{provider}", __package__)
    return module.sendsms(content, config=config[f"smsprovider:{provider}"])
