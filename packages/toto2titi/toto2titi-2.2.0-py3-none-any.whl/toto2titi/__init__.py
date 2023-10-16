# Copyright 2021-2023 Louis Paternault
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

"""Common tools for Toto2Titi."""

import configparser
import logging
import os
import subprocess
import tempfile
from dataclasses import dataclass

from xdg import BaseDirectory

from .editor import editor

APPNAME = "toto2titi"
VERSION = "2.2.0"


@dataclass
class T2TException(Exception):
    """Generic exception to be nicely catched and displayed to the user."""

    message: str
    level: int = logging.INFO


def get_config_files(appname):
    """Search for a configuration file, and return its name."""
    for directory in BaseDirectory.xdg_config_dirs:
        for keyword in (appname, APPNAME):
            filename = os.path.join(directory, f"{keyword}.conf")
            if os.path.exists(filename):
                yield filename


def read_config(appname):
    """Return the configuration file (as a configparser.ConfigParser() object."""
    config = configparser.ConfigParser()
    config.read(get_config_files(appname))
    return config


def get_editor(config):
    """Return the command line to be used to run the editor."""
    try:
        return config["general"]["editor"]
    except KeyError:
        return None


def edit_content(content, *, config, appname):
    """Edit content.

    Open a file containing the content, and edit it. When
    user closes the editor, return the file content.
    """
    command = get_editor(config)

    if command is None:
        return editor(content, appname=appname)

    with tempfile.TemporaryDirectory() as tempdir:
        filename = os.path.join(tempdir, "message.txt")
        with open(filename, "w", encoding="utf8") as temp:
            temp.write(content)

        try:
            subprocess.check_call(command.format(filename), shell=True)
        except subprocess.CalledProcessError as error:
            raise T2TException(str(error), level=logging.ERROR) from error

        with open(filename, "r", encoding="utf8") as temp:
            return temp.read().strip()
