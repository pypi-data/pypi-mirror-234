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

"""Common tkinter frame."""

import tkinter as tk
from tkinter import ttk

from .icon import find as find_icon


class Frame(ttk.Frame):
    """Tkinter frame with default options."""

    # pylint: disable=too-many-ancestors

    def __init__(self, appname, geometry, parent=None):
        super().__init__(parent)
        self.parent = parent
        if icon := find_icon(appname, extensions=(".png",)):
            self.parent.iconphoto(False, tk.PhotoImage(file=icon))
        self.parent.geometry(geometry)
        self.parent.minsize(width=320, height=240)
        self.parent.title(appname)
