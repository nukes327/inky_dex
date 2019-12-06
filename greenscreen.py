#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Cleanup script to make transparency work for inky hats.

Attribution:
    This script is courtesy of user mikeyp on pimoroni forums.

Notes:
    Fixes issues with GIMP's transparency export by using a green screen method.

    Any pixels that should be transparent are first painted green using
    the fourth color of the colormap.

    Once the image is saved in the sprites directory this script can be run to clean
    any images of greenscreen, leaving behind transparency.

"""


from PIL import Image  # type: ignore
import glob

for sprite in glob.glob("assets/sprites/*.png"):
    img = Image.open(sprite)
    img.save(sprite, transparency=3, optimize=1)
