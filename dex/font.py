#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Carry png font information and related methods.

Todo:
    Implement class

"""

from PIL import Image  # type: ignore
import png  # type: ignore
import re
from typing import Dict, Union


class Font:
    """Font object for use in dex routines."""

    def __init__(self, filename: str):
        """Initialize values for font object.

        Args:
            filename: Filename of the font image to load

        """
        self.filename = filename
        self.metadata: Dict[str, Union[int, str]] = {}
        self.image = Image.open(self.filename)
        self.update_metadata()

    def update_metadata(self) -> None:
        """Load metadata from font png chunks."""
        sheet = png.Reader(filename=self.filename)
        chunk_list = list(sheet.chunks())

        for chunk in chunk_list:
            if re.compile(b'..Xt').match(chunk[0]):
                decoded = bytes.decode(chunk[1]).split('\x00')
                keyword = decoded[0]
                value = decoded[-1]
                if keyword != 'SHEETSTRING':
                    self.metadata[keyword] = int(value)
                else:
                    self.metadata[keyword] = value
