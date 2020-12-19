#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Cleanup script to make transparency work for inky hats.

Attribution:
    This script is courtesy of user mikeyp on pimoroni forums.

Notes:
    Fixes issues with GIMP's transparency export by using a green screen method.

    Any pixels that should be transparent are first painted green using
    the fourth color of the colormap.

    Once the image is saved in the assets directory this script can be run to clean
    any images of greenscreen, leaving behind transparency.

"""


from PIL import Image  # type: ignore
import glob
import re
import png  # type: ignore

for sprite in glob.glob("assets/sprites/*.png"):
    pre_chunk_list = list(png.Reader(sprite).chunks())
    img = Image.open(sprite)
    img.save(sprite, transparency=3, optimize=1)
    post_chunk_list = list(png.Reader(sprite).chunks())
    for chunk in pre_chunk_list:
        if re.compile(b"..Xt").match(chunk[0]):
            post_chunk_list.insert(2, chunk)
    with open(sprite, "wb") as out_sprite:
        png.write_chunks(out_sprite, post_chunk_list)


for ui_piece in glob.glob("assets/ui/*.png"):
    pre_chunk_list = list(png.Reader(ui_piece).chunks())
    img = Image.open(ui_piece)
    img.save(ui_piece, transparency=3, optimize=1)
    post_chunk_list = list(png.Reader(ui_piece).chunks())
    for chunk in pre_chunk_list:
        if re.compile(b"..Xt").match(chunk[0]):
            post_chunk_list.insert(2, chunk)
    with open(ui_piece, "wb") as out_ui_piece:
        png.write_chunks(out_ui_piece, post_chunk_list)
