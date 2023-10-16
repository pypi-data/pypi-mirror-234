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

"""A graphical application to select one item."""

import functools
import tkinter as tk
from tkinter import ttk

from . import tkcommon


class Selector(tkcommon.Frame):
    """A graphical application to select one item."""

    # pylint: disable=too-many-ancestors, too-many-instance-attributes

    def __init__(self, choices, parent=None, focus=None, *, appname):
        super().__init__(appname, parent=parent, geometry="320x480")

        self.answer = None
        self.current_button = None
        self._create_widgets(choices, focus)

    def _on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.itemconfig(self.frame_id, width=event.width)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mouse_wheel_up(self, event):
        # pylint: disable=unused-argument
        self.canvas.yview_scroll(1, "units")

    def _on_mouse_wheel_down(self, event):
        # pylint: disable=unused-argument
        self.canvas.yview_scroll(-1, "units")

    def _on_key_return(self, event):
        # pylint: disable=unused-argument
        self._on_button_pressed(self.current_button)

    def _update_focus_top(self, direction, *args, **kwargs):
        """Selected button has moved to top or bottom. Update everything that needs it."""
        # pylint: disable=unused-argument
        if self.current_button is None:
            # No button is enabled
            return

        if direction == 1:
            self.current_button = 0
            step = 1
        else:
            self.current_button = len(self.buttons) - 1
            step = -1

        while str(self.buttons[self.current_button]["state"]) != str(tk.NORMAL):
            self.current_button += step

        self.buttons[self.current_button].focus()

    def _update_focus(self, step, *args, **kwargs):
        """Selected button has changed. Update everything that needs it."""
        # pylint: disable=unused-argument

        if self.current_button is None:
            # No button is enabled
            return

        start = self.current_button

        while True:
            self.current_button = self.current_button + step
            if self.current_button == 0 or self.current_button == len(self.buttons):
                self.current_button = start
                break
            if str(self.buttons[self.current_button]["state"]) == str(tk.NORMAL):
                break

        self.buttons[self.current_button].focus()

    def _create_widgets(self, choices, focus):
        self.pack(side="top", fill="both", expand=True)
        self.canvas = tk.Canvas(self)
        self.frame = ttk.Frame(self.canvas)
        self.scrollbar = ttk.Scrollbar(
            self, orient="vertical", command=self.canvas.yview
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.frame_id = self.canvas.create_window(
            (0, 0), window=self.frame, anchor="nw"
        )

        self.frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_frame_configure)

        # Buttons
        self.buttons = []
        at_least_one_enabled_button = False
        for i, item in enumerate(choices):
            button = ttk.Button(
                self.frame,
                text=item["text"],
                command=functools.partial(self._on_button_pressed, i),
            )
            button.grid(column=0, row=i, sticky=(tk.E, tk.W))
            if item["enabled"]:
                button["state"] = tk.NORMAL
                at_least_one_enabled_button = True
            else:
                button["state"] = tk.DISABLED
            self.buttons.append(button)

        # Initial focus
        if focus is None:
            focus = 0
        if at_least_one_enabled_button:
            self.current_button = focus - 1
            self._update_focus(1)
        else:
            self.current_button = None

        # Finalize grid
        self.frame.columnconfigure(0, weight=1)

        # Bindings
        self.parent.bind("<Escape>", self._cancel)
        # self.canvas.bind_all("<MouseWheel>", self._onMouseWheel)
        self.canvas.bind_all("<Button-4>", self._on_mouse_wheel_down)
        self.canvas.bind_all("<Button-5>", self._on_mouse_wheel_up)
        self.canvas.bind_all("<Up>", functools.partial(self._update_focus, -1))
        self.canvas.bind_all("<Down>", functools.partial(self._update_focus, 1))
        self.canvas.bind_all(
            "<Home>",
            functools.partial(
                self._update_focus_top,
                1,
            ),
        )
        self.canvas.bind_all("<End>", functools.partial(self._update_focus_top, -1))
        self.canvas.bind_all("<Return>", self._on_key_return)

    def _cancel(self, event):
        # pylint: disable=unused-argument
        self.answer = None
        self.parent.destroy()

    def _on_button_pressed(self, button):
        self.answer = button
        self.parent.destroy()


def selector(choices, default, *, appname):
    """A graphical application to select one item."""
    root = tk.Tk()
    app = Selector(parent=root, choices=choices, focus=default, appname=appname)
    root.mainloop()
    return app.answer
