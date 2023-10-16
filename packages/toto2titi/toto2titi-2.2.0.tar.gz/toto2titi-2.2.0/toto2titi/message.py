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

"""Display messages to user."""

import logging

try:
    import notifypy

    _NOTIFY_LIB = "notifypy"
except ImportError:
    try:
        import notify2

        _NOTIFY_LIB = "notify2"
    except ImportError:
        _NOTIFY_LIB = "default"

from .dialog import dialog
from .icon import find as find_icon


def message(text, level, *, appname):
    """Display the message in a window, or notify it, depending of level."""
    if level > logging.WARNING:
        dialog(str(text), level, appname=appname)
    else:
        notify(str(text), appname=appname)


def _notify_notifypy(text, *, appname):
    """Display a notification."""
    notification = notifypy.Notify()
    notification.title = appname
    notification.message = text
    notification.icon = find_icon(appname)
    notification.send(block=False)


def _notify_notify2(text, *, appname):
    # We can only run this function if `notify2` has been correctly imported
    # pylint: disable=used-before-assignment
    notify2.init(appname)

    notify2.Notification(
        summary=appname,
        message=text,
        icon=str(find_icon(appname)),
    ).show()


def _notify_default(text, *, appname):
    logging.info("%s: %s", appname, text)


def notify(text, *, appname):
    """Display a desktop notification, using an available library.

    If no library is availble, log to terminal.
    """
    if _NOTIFY_LIB == "notifypy":
        return _notify_notifypy(text, appname=appname)
    if _NOTIFY_LIB == "notify2":
        return _notify_notify2(text, appname=appname)
    return _notify_default(text, appname=appname)
