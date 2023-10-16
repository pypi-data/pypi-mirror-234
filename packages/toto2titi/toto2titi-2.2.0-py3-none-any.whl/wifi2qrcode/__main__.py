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

"""Main script for wifi2qrcode."""

import locale
import logging
import operator

import qrcode

from toto2titi import T2TException, commandline, imageviewer, message, selector, wifi

APPNAME = "wifi2qrcode"


def selectconnection():
    """Display list of available connections, and return the one the user selected."""
    connections = list(wifi.connections())
    active = wifi.active_connection()

    for conn in connections:
        if conn["name"] == conn["ssid"]:
            conn["text"] = conn["name"]
        else:
            conn["text"] = f"{conn['name']} ({conn['ssid']})"
        conn["_sortkey"] = locale.strxfrm(conn["text"]).lower()
        conn["enabled"] = (
            conn["security"] in ("WPA", "WEP") and conn["password"] is not None
        )

    connections = list(sorted(connections, key=operator.itemgetter("_sortkey")))
    default = None
    for i, conn in enumerate(connections):
        if conn["uuid"] == active and conn["enabled"]:
            default = i
            break

    if (
        answer := selector.selector(
            choices=connections, default=default, appname=APPNAME
        )
    ) is None:
        return None
    return connections[answer]


def main():
    """Main function."""
    logging.basicConfig(level=logging.INFO)

    try:
        commandline.parser(
            APPNAME, description="Display a QR code containing Wifi credentials."
        ).parse_args()

        credentials = selectconnection()

        if credentials is None:
            raise T2TException("No wifi connection selected.", level=logging.WARNING)

        code = wifi.qrcode(credentials["ssid"], credentials["password"])

        imageviewer.imageviewer([qrcode.make(code)], single=True, appname=APPNAME)

    except T2TException as error:
        logging.log(level=error.level, msg=error)
        message.message(error, level=error.level, appname=APPNAME)


if __name__ == "__main__":
    main()
