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

"""A quick and dirty text editor."""

import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from . import tkcommon


class Editor(tkcommon.Frame):
    # pylint: disable=too-many-ancestors
    """A quick and dirty text editor."""

    def __init__(self, parent=None, initial="", *, appname):
        super().__init__(appname, parent=parent, geometry="640x480")
        self.content = ""
        self._create_widgets(initial)

    def _save(self, *args, **kwargs):
        # pylint: disable=unused-argument
        self.content = self.text.get(1.0, tk.END)[:-1]
        self.parent.destroy()

    def _cancel(self, *args, **kwargs):
        # pylint: disable=unused-argument
        self.content = ""
        self.parent.destroy()

    def _create_widgets(self, initial):
        self.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Text area
        self.text = ScrolledText(
            self, font="Helvetica 14", foreground="black", background="lightgray"
        )
        self.text.insert(tk.INSERT, initial)
        self.text.focus()

        # Buttons
        self.save = ttk.Button(self, text="Save & Exit", command=self._save)
        self.cancel = ttk.Button(self, text="Cancel", command=self._cancel)

        # Place everything on grid
        self.text.grid(
            column=0, row=0, columnspan=3, rowspan=1, sticky=(tk.N, tk.E, tk.W, tk.S)
        )
        self.save.grid(column=2, row=1, sticky=(tk.S, tk.W), padx=5, pady=5)
        self.cancel.grid(column=1, row=1, sticky=(tk.S, tk.W), padx=5, pady=5)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

        # Bindings
        self.parent.bind("<Escape>", self._cancel)
        self.parent.bind("<Control-s>", self._save)
        self.parent.bind("<Control-S>", self._save)


def editor(initial="", *, appname):
    """A quick and dirty text editor."""
    root = tk.Tk()
    app = Editor(parent=root, initial=initial, appname=appname)
    app.mainloop()
    return app.content
