#!/usr/bin/env python3

# Copyright 2021 Louis Paternault
#
# png2svg is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# png2svg is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with png2svg.  If not, see <http://www.gnu.org/licenses/>.

import logging
import sys
import textwrap

from jinja2 import Template
from PIL import Image

SVG_TEMPLATE = textwrap.dedent(
    """\
    <?xml version="1.0" encoding="UTF-8"?>
    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
        viewBox="0 0 {{ image.width }} {{ image.height }}">
    <defs>
    </defs>
    {%- for x in range(image.width) -%}
        {%- for y in range(image.height) -%}
            {% set red, green, blue, alpha = image.getpixel((x, y)) %}
            {%- if alpha != 0 %}
                <rect x="{{ x }}" y="{{ y }}" width="1" height="1" fill="{{ "#{0:02X}{1:02X}{2:02X}".format(red, green, blue) }}" opacity="{{ alpha / 255 }}" />
            {%- endif -%}
        {%- endfor -%}
    {%- endfor %}
    </svg>
"""
)


def png2svg(pngname, svgname):
    png = Image.open(pngname).convert("RGBA")
    with open(svgname, mode="w") as svg:
        svg.write(Template(SVG_TEMPLATE).render(image=png))


def usage():
    print("png2svg.py PNG SVG")
    print(
        "Convert the PNG image file to a SVG file. Each pixel of the source file is converted to a SVG rectangle."
    )


if __name__ == "__main__":
    if "--help" in sys.argv[1:] or "-h" in sys.argv[1:]:
        usage()
        sys.exit(0)

    if len(sys.argv) != 3:
        logging.error("Wrong number of arguments.")
        usage()
        sys.exit(1)

    png, svg = sys.argv[1:]
    try:
        png2svg(png, svg)
    except OSError as error:
        logging.error(error)
        sys.exit(1)
