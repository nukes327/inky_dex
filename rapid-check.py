#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This file is for quick back-to-back sprite checks, 1 second display each before moving on
Modify the numbers in modified_list to the changed/new sprites
"""

modified_list = []

import time
from inky import InkyPHAT
from PIL import Image, ImageDraw

inky_display = InkyPHAT('black')
inky_display.set_border(inky_display.BLACK)

img = Image.open('dex-background.png')


for i in modified_list:
    try:
        sprite = Image.open('sprites/{0:03d}-2s.png'.format(i))
    except IOError:
        continue
    
    if sprite is not None:
        print('Current sprite is {0:03d}-2s.png'.format(i))
        img.paste(sprite, (7, 7))
        inky_display.set_image(img)
        inky_display.show()
        time.sleep(1)
