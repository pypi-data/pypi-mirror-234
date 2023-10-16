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

"""Main script for paste2sms."""

import logging
import tempfile

import pyperclip

import toto2titi
from toto2titi import T2TException, commandline, message, sendsms

APPNAME = "paste2sms"

logging.basicConfig(level=logging.INFO)


def main():
    """Main function."""

    content = None
    try:
        # Parse command line arguments
        commandline.parser(
            APPNAME,
            description="Send clipboard content as a SMS.",
        ).parse_args()

        # Read configuration file
        config = toto2titi.read_config(APPNAME)

        # Edit message
        content = toto2titi.edit_content(
            pyperclip.paste(), config=config, appname=APPNAME
        )
        if not content:
            raise T2TException("Message is empty. No SMS sent.", level=logging.WARNING)

        # Send message
        try:
            sendsms.sendsms(content, config=config)
        except Exception as error:
            raise T2TException(f"Error: {error}.") from error

        # Notify user
        message.notify("SMS sent successfully.", appname=APPNAME)

    except T2TException as error:
        if content is None or content == "":
            text = str(error)
        else:
            with tempfile.NamedTemporaryFile(
                prefix="paste2sms-", mode="w", delete=False
            ) as backup:
                backup.write(content)
                backup.write("\n")
            text = str(error) + f"\nMessage has been saved in '{backup.name}'."
        logging.log(level=error.level, msg=text)
        message.message(text, level=error.level, appname=APPNAME)


if __name__ == "__main__":
    main()
