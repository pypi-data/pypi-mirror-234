# Copyright (C) 2010 - 2011 Red Hat, Inc.
# Copyright (C) 2021 Louis Paternault
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

# This code was first released by Red Hat, Inc., in 2010-2011, under the GPL 2.0 or later.

"""Some functions related to wifi."""

import logging

import dbus


def active_connection():
    """Return the UUID of the active connection.

    Original source:
    https://cgit.freedesktop.org/NetworkManager/NetworkManager/tree/examples/python/dbus/get-active-connection-uuids.py
    """

    # pylint: disable=invalid-name, broad-except

    bus = dbus.SystemBus()

    # Get a proxy for the base NetworkManager object
    m_proxy = bus.get_object(
        "org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager"
    )
    mgr_props = dbus.Interface(m_proxy, "org.freedesktop.DBus.Properties")

    # Find all active connections
    active = mgr_props.Get("org.freedesktop.NetworkManager", "ActiveConnections")

    for a in active:
        a_proxy = bus.get_object("org.freedesktop.NetworkManager", a)

        a_props = dbus.Interface(a_proxy, "org.freedesktop.DBus.Properties")

        # Grab the connection object path so we can get all the connection's settings
        connection_path = a_props.Get(
            "org.freedesktop.NetworkManager.Connection.Active", "Connection"
        )
        c_proxy = bus.get_object("org.freedesktop.NetworkManager", connection_path)
        connection = dbus.Interface(
            c_proxy, "org.freedesktop.NetworkManager.Settings.Connection"
        )
        settings = connection.GetSettings()

        if settings["connection"]["type"] == "802-11-wireless":
            return str(settings["connection"]["uuid"])
    return None


def _merge_secrets(proxy, config, setting_name):
    # Original source:
    # https://cgit.freedesktop.org/NetworkManager/NetworkManager/tree/examples/python/dbus/list-connections.py

    # pylint: disable=broad-except
    try:
        # returns a dict of dicts mapping name::setting, where setting is a dict
        # mapping key::value.  Each member of the 'setting' dict is a secret
        secrets = proxy.GetSecrets(setting_name)
        # Copy the secrets into our connection config
        for setting in secrets:
            for key in secrets[setting]:
                config[setting_name][key] = secrets[setting][key]
    except Exception:
        pass


def connections():
    """Ask the settings service for the list of connections it provides

    Original source:
    https://cgit.freedesktop.org/NetworkManager/NetworkManager/tree/examples/python/dbus/list-connections.py
    """
    bus = dbus.SystemBus()
    service_name = "org.freedesktop.NetworkManager"
    proxy = bus.get_object(service_name, "/org/freedesktop/NetworkManager/Settings")
    settings = dbus.Interface(proxy, "org.freedesktop.NetworkManager.Settings")
    connection_paths = settings.ListConnections()

    # List each connection's name, UUID, and type
    for path in connection_paths:
        con_proxy = bus.get_object(service_name, path)
        settings_connection = dbus.Interface(
            con_proxy, "org.freedesktop.NetworkManager.Settings.Connection"
        )
        config = settings_connection.GetSettings()

        # Now get secrets too; we grab the secrets for each type of connection
        # (since there isn't a "get all secrets" call because most of the time
        # you only need 'wifi' secrets or '802.1x' secrets, not everything) and
        # merge that into the configuration data
        _merge_secrets(settings_connection, config, "802-11-wireless")
        _merge_secrets(settings_connection, config, "802-11-wireless-security")
        _merge_secrets(settings_connection, config, "802-1x")
        _merge_secrets(settings_connection, config, "gsm")
        _merge_secrets(settings_connection, config, "cdma")
        _merge_secrets(settings_connection, config, "ppp")

        if config["connection"]["type"] == "802-11-wireless":
            ssid = "".join(chr(byte) for byte in config["802-11-wireless"]["ssid"])
            security = None
            password = None

            if "802-11-wireless-security" in config:
                if config["802-11-wireless-security"]["key-mgmt"] == "wpa-psk":
                    if "psk" in config["802-11-wireless-security"]:
                        security = "WPA"
                        password = str(config["802-11-wireless-security"]["psk"])
                    else:
                        logging.error("No password found for %s.", ssid)
                elif (
                    config["802-11-wireless-security"]["key-mgmt"] == "none"
                    and "wep-key0" in config["802-11-wireless-security"]
                ):
                    security = "WEP"
                    password = str(config["802-11-wireless-security"]["wep-key0"])
                else:
                    logging.error("Unknown security type for %s.", ssid)

            yield {
                "uuid": str(config["connection"]["uuid"]),
                "name": str(config["connection"]["id"]),
                "ssid": ssid,
                "security": security,
                "password": password,
            }


def qrcode(ssid, password):
    """Return the code meant to be turned as a QR code containing the credentials."""

    def escape(text):
        return text.replace(":", r"\:").replace(";", r"\;")

    return f"WIFI:T:WPA;S:{escape(ssid)};P:{escape(password)};;"
