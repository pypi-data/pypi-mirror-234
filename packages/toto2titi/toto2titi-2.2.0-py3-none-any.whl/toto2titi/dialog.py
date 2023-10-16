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

"""Simple dialog boxes"""

import logging
import tkinter as tk
from tkinter import filedialog, messagebox


def dialog(text, level, *, appname):
    """Display the message in a window."""
    root = tk.Tk()
    root.withdraw()

    dialogbox = messagebox.showinfo
    if level >= logging.ERROR:
        dialogbox = messagebox.showerror

    dialogbox(parent=root, title=appname, message=text)
    root.destroy()


def asksaveasfilename(**options):
    """Prompt a file name."""
    root = tk.Tk()
    root.withdraw()

    filename = filedialog.asksaveasfilename(**options)

    root.destroy()

    return filename
