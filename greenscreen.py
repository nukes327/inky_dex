#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script courtesy of user mikeyp on pimoroni forums.

Fixes issues with GIMP's transparency export by using a green screen
in GIMP and replacing the green with transparency using PIL.
"""

from PIL import Image
import glob

for sprite in glob.glob("sprites/*.png"):
    img = Image.open(sprite)
    img.save(sprite, transparency = 3, optimize = 1)
