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

"""A graphical application to display images."""

import functools
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

from . import tkcommon


def between(a, n, b):
    """Return n (in a<=n<=b), or a if n<a, or b if n>b."""
    # pylint: disable=invalid-name
    return max(a, min(n, b))


class ImageViewer(tkcommon.Frame):
    """A graphical application to display images."""

    # pylint: disable=too-many-ancestors, too-many-instance-attributes

    def __init__(self, images, *, appname, parent=None, single=False):
        super().__init__(appname, parent=parent, geometry="640x480")

        self.images = images
        self.current_image = 0
        self._create_widgets(single)

    def _next_image(self, step, *args, **kwargs):
        # pylint: disable=unused-argument
        self.current_image = between(0, self.current_image + step, len(self.images) - 1)

        self.resize()
        self.progress["text"] = f"{self.current_image+1}/{len(self.images)}"
        if self.current_image == 0:
            self.previous["state"] = tk.DISABLED
        else:
            self.previous["state"] = tk.NORMAL
        if self.current_image == len(self.images) - 1:
            self.next["state"] = tk.DISABLED
        else:
            self.next["state"] = tk.NORMAL

    def resize(self, event=None):
        """Fit image to window."""
        if event is None:
            size = (self.image.winfo_width(), self.image.winfo_height())
        else:
            size = (event.width, event.height)
        size = [min(size)] * 2
        self._resized = (  # pylint: disable=attribute-defined-outside-init
            # pylint: disable=no-member
            ImageTk.PhotoImage(self.images[self.current_image].resize(size, Image.BOX))
        )
        self.image.configure(image=self._resized)

    def _create_widgets(self, single):
        self.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Image
        self.image = tk.Label(self)
        self.resize()

        # Place on grid
        self.image.grid(
            column=0,
            row=0,
            columnspan=5,
            rowspan=1,
            sticky=(tk.N, tk.E, tk.W, tk.S),
        )

        self.columnconfigure(0, weight=1)
        self.columnconfigure(4, weight=1)
        self.rowconfigure(0, weight=1)
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

        # Bindings
        self.parent.bind("<Escape>", self.quit)
        self.parent.bind("<Configure>", self.resize)

        # Buttons
        if not single:
            self.previous = ttk.Button(
                self,
                text="\N{Leftwards Black Arrow}",
                command=functools.partial(self._next_image, -1),
            )
            self.next = ttk.Button(
                self,
                text="\N{Rightwards Black Arrow}",
                command=functools.partial(self._next_image, 1),
            )
            self.progress = ttk.Label(self, text="")
            self.next.focus()
            # Place on grid
            self.previous.grid(column=1, row=1, sticky=(tk.S, tk.W), padx=5, pady=5)
            self.progress.grid(column=2, row=1, sticky=(), padx=5, pady=5)
            self.next.grid(column=3, row=1, sticky=(tk.S, tk.E, tk.W), padx=5, pady=5)
            # Bindings
            self.parent.bind("<Left>", functools.partial(self._next_image, -1))
            self.parent.bind("<Right>", functools.partial(self._next_image, 1))
            # Initialisez buttons and label
            self._next_image(0)

    def quit(self, *args, **kwargs):
        # pylint: disable=unused-argument
        self.parent.destroy()


def imageviewer(images, single=False, *, appname):
    """A graphical application to display images."""
    root = tk.Tk()
    app = ImageViewer(parent=root, images=images, single=single, appname=appname)
    app.mainloop()
