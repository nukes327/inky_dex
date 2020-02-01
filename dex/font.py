#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Carry png font information and related methods.

Todo:
    Document special character usage

"""

import re
from PIL import Image  # type: ignore
import png  # type: ignore


class Font:
    """Font object for use in dex routines."""

    def __init__(self, filename: str):
        """Initialize values for font object.

        Args:
            filename: Filename of the font image to load

        """
        self.filename = filename
        self.charwidth: int
        self.charheight: int
        self.sheetwidth: int
        self.sheetstring: str
        self.image = Image.open(self.filename)
        self.update_metadata()

    def update_metadata(self) -> None:
        """Load metadata from font png chunks."""
        sheet = png.Reader(filename=self.filename)
        chunk_list = list(sheet.chunks())
        metadata = {}

        for chunk in chunk_list:
            if re.compile(b'..Xt').match(chunk[0]):
                decoded = bytes.decode(chunk[1]).split('\x00')
                keyword = decoded[0]
                value = decoded[-1]
                if keyword != 'SHEETSTRING':
                    metadata[keyword] = int(value)
                else:
                    self.sheetstring = value

        self.charwidth = metadata['CHARWIDTH']
        self.charheight = metadata['CHARHEIGHT']
        self.sheetwidth = metadata['SHEETWIDTH']

    def get_character(self, character: str) -> Image:
        """Return a single character from the font sheet.

        Args:
            character: The character or special character replacement to fetch

        """
        index = self.sheetstring.index(character)
        sheet_x = (index % self.sheetwidth) * self.charwidth
        sheet_y = (int(index / self.sheetwidth)) * self.charheight
        right_bound = sheet_x + self.charwidth
        lower_bound = sheet_y + self.charheight
        return self.image.crop((sheet_x, sheet_y, right_bound, lower_bound))

