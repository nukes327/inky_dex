#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Utility functions used in multiple dex files."""

from PIL import Image  # type: ignore
from typing import Tuple


def create_mask(source: Image.Image, mask: Tuple[int, int, int] = (0, 1, 2)) -> Image.Image:
    """Create an image mask for pasting purposes.

    Args:
        source: Image to create the mask from
        mask:   Tuple containing colormap indices to be masked

                Default values are equivalent to white, black, and red
                for an inky display

    Returns:
        An image mask for the source image

    Attribution:
        This method was written by the folks at pimoroni, and can be found within
        their examples for their inky displays.

    """
    mask_image = Image.new("1", source.size)
    w, h = source.size
    for x in range(w):
        for y in range(h):
            p = source.getpixel((x, y))
            if p in mask:
                mask_image.putpixel((x, y), 255)
    return mask_image


def get_real_bounds(source: Image.Image) -> Tuple[int, int, int, int]:
    """Calculate non-transparent area of an image.

    Args:
        source: Image to calculate bounds of

    Returns:
        4-tuple as (x1, y1, x2, y2)

    """
    remap = list(range(256))
    remap[3] = 0
    remap[0] = 3
    return source.remap_palette(remap).getbbox()
