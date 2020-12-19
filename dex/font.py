#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Carry png font information and related methods.

Todo:
    Document special character usage

"""

import re
from PIL import Image  # type: ignore
from typing import Union
import png  # type: ignore
import dex.util as util  # type: ignore


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
        self.image: Image.Image = Image.open(self.filename)
        self.update_metadata()

    def update_metadata(self) -> None:
        """Load metadata from font png chunks."""
        sheet = png.Reader(filename=self.filename)
        chunk_list = list(sheet.chunks())
        metadata = {}

        for chunk in chunk_list:
            if re.compile(b"..Xt").match(chunk[0]):
                decoded = bytes.decode(chunk[1]).split("\x00")
                keyword = decoded[0]
                value = decoded[-1]
                if keyword != "SHEETSTRING":
                    metadata[keyword] = int(value)
                else:
                    self.sheetstring = value

        self.charwidth = metadata["CHARWIDTH"]
        self.charheight = metadata["CHARHEIGHT"]
        self.sheetwidth = metadata["SHEETWIDTH"]
        self.pixel_gap = int(0.125 * self.charwidth)

    def get_character(self, character: str) -> Image.Image:
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

    def get_string(self, line: str) -> Image.Image:
        """Return a line using characters from the font sheet.

        Args:
            line: The line to build and fetch

        """
        out = Image.new("P", (self.charwidth * len(line), self.charheight))
        for index, character in enumerate(line, 0):
            out.paste(self.get_character(character), (index * self.charwidth, 0))
        return out

    def get_numeral(self, num: Union[int, float], prefix: str = None, suffix: str = None) -> Image.Image:
        """Return a numeral formatted cleanly with pre/postfixes in font.

        Args:
            num:     Numeral to format
            prefix:  Optional prefix character(s) to include
            postfix: Optional postfix character(s) to include

        """

        # calc numeral length
        is_float = isinstance(num, float)
        snum = str(num)
        num_len = len(snum) - is_float

        # calc prefix and suffix lengths
        pre_len = 0
        suff_len = 0
        cw = self.charwidth
        pg = self.pixel_gap
        if prefix is not None:
            pre_len = sum([cw - pg if letter.islower() else cw for letter in prefix])
        if suffix is not None:
            suff_len = sum([cw - pg if letter.islower() else cw for letter in suffix])

        # calc final width and generate base image
        final_width = pre_len + suff_len + num_len * cw + 4 * is_float
        out = Image.new("P", (final_width, self.charheight))

        # add suffix
        offset = final_width
        if suffix is not None:
            for character in suffix[::-1]:
                offset -= cw - pg * character.islower()
                temp = self.get_character(character)
                out.paste(temp, (offset, 0), util.create_mask(temp))

        # add float
        if is_float:
            pre_float, post_float = snum.split(".")
            offset -= len(post_float) * cw
            temp = self.get_string(post_float)
            out.paste(temp, (offset, 0), util.create_mask(temp))
            offset -= int(cw / 2) + pg
            temp = self.get_character(".")
            out.paste(temp, (offset, 0), util.create_mask(temp))
            offset -= len(pre_float) * cw - 2 * pg
            temp = self.get_string(pre_float)
            out.paste(temp, (offset, 0), util.create_mask(temp))

        # add integer
        if not is_float:
            offset -= len(snum) * cw - pg
            temp = self.get_string(snum)
            out.paste(temp, (offset, 0), util.create_mask(temp))

        # add prefix
        if prefix is not None:
            for character in prefix[::-1]:
                offset -= cw - pg * character.islower()
                temp = self.get_character(character)
                out.paste(temp, (offset, 0), util.create_mask(temp))

        return out
