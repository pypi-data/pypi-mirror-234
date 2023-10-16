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

"""Tools related to icons."""

import pathlib


def find(appname, *, extensions=None):
    """Find the icon of the given application.

    May return ``None`` if none was found.
    """
    for size in ("scalable", "32x32"):
        for path in pathlib.Path(f"/usr/share/icons/hicolor/{size}/apps/").glob(
            f"{appname}.*"
        ):
            if extensions is None or path.suffix in extensions:
                if path.exists():
                    return path

    return None
