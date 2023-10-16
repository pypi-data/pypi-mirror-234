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

"""Common command line parser."""

import argparse

from toto2titi import VERSION


def parser(appname, *args, **kwargs):
    """Build and return the command line parser."""
    cmd_parser = argparse.ArgumentParser(
        prog=appname,
        epilog=(
            "This command line arguments has no options (besides the obligatory "
            "--help and --version): it is meant to be used as a graphical tool, "
            "and that's all. But this might change in the future…"
        ),
        *args,
        **kwargs,
    )
    cmd_parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
    )
    return cmd_parser
