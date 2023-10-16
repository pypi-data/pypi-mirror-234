# Copyright 2020-2021 Louis Paternault
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

"""Main script for paste2file."""

import logging
import subprocess

import pyperclip

import toto2titi
from toto2titi import T2TException, commandline, dialog, message

APPNAME = "paste2file"


def main():
    """Main function."""
    logging.basicConfig(level=logging.INFO)

    try:
        # Read configuration file
        config = toto2titi.read_config(APPNAME)

        # Parse command line arguments
        commandline.parser(
            APPNAME,
            description="Save clipboard as a file.",
        ).parse_args()

        clipboard = pyperclip.paste()
        if not clipboard:
            raise T2TException("Clipboard is empty. Cancelled.", level=logging.ERROR)

        filename = dialog.asksaveasfilename(title=APPNAME)
        if filename in ("", ()):
            raise T2TException("Cancelled.", level=logging.WARNING)

        with open(filename, mode="w", encoding="utf8") as file:
            file.write(clipboard)

        # Notify user
        message.notify(f"Clipboard content saved as {filename}.", appname=APPNAME)

        command = toto2titi.get_editor(config)
        if command is not None:
            subprocess.check_call(command.format(filename), shell=True)

    except T2TException as error:
        logging.log(level=error.level, msg=str(error))
        message.message(error, level=error.level, appname=APPNAME)


if __name__ == "__main__":
    main()
