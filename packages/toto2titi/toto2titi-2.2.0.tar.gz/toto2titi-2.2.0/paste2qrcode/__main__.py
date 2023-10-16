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

"""Main script for paste2qrcode."""

import logging

import pyperclip
import qrcode

import toto2titi
from toto2titi import T2TException, commandline, imageviewer, message

APPNAME = "paste2qrcode"

logging.basicConfig(level=logging.INFO)


def qrcodes(text):
    """Split text into a list of QR codes."""
    try:
        return [qrcode.make(text)]
    except qrcode.exceptions.DataOverflowError:
        i = len(text) // 2
        return qrcodes(text[:i]) + qrcodes(text[i:])


def main():
    """Main function."""

    content = None
    try:
        commandline.parser(
            APPNAME,
            description="Display clipboard content as a QR code.",
        ).parse_args()

        content = pyperclip.paste()

        # Read configuration file
        config = toto2titi.read_config(APPNAME)

        # Edit message
        content = toto2titi.edit_content(
            pyperclip.paste(), config=config, appname=APPNAME
        )
        if not content:
            raise T2TException("Clipboard is empty. Cancelled.", level=logging.ERROR)

        imageviewer.imageviewer(qrcodes(content), appname=APPNAME)

    except T2TException as error:
        logging.log(msg=str(error), level=error.level)
        message.message(error, level=error.level, appname=APPNAME)


if __name__ == "__main__":
    main()
