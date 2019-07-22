#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This file is a quick use hacky file for rapid testing of image work.
Additionally, new functions are like to be tested here first
"""

import configparser
import os
import time
#from inky import InkyPHAT, InkyWHAT
from PIL import Image, ImageDraw

"""
Turns out if you have red in an image, but the display is set to black, it'll display as gray.
This will be convenient for quickly testing code that dynamically displays sprites on the screen
A 2 second refresh time allows for more rapid testing than a 15 second refresh time
"""

def init_config():
    config = configparser.ConfigParser()
    config['DEFAULT'] = {
            'type': '',
            'color': ''}
    with open('dex.ini', 'w+') as conffile:
        config.write(conffile)

if not os.path.isfile('dex.ini'):
    print('No config found, generating an empty one')
    init_config()
    exit()

dex_config = configparser.ConfigParser()

with open('dex.ini') as conffile:
    dex_config.read_file(conffile)

if dex_config['DEFAULT']['type'] == 'what':
    from inky import InkyWHAT
    inky_display = InkyWHAT(dex_config['DEFAULT']['color'])
elif dex_config['DEFAULT']['type'] == 'phat':
    from inky import InkyPHAT
    inky_display = InkyPHAT(dex_config['DEFAULT']['color'])
else:
    print("Valid types are 'what' and 'phat'")
    exit()

inky_display.set_border(inky_display.BLACK)

#img = Image.open('dex-background.png')
img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
font = Image.open('gscfont.png')

def create_mask(source, mask=(inky_display.WHITE, inky_display.BLACK, inky_display.RED)):
    mask_image = Image.new("1", source.size)
    w, h = source.size
    for x in range(w):
        for y in range(h):
            p = source.getpixel((x, y))
            if p in mask:
                mask_image.putpixel((x, y), 255)
    return mask_image

def gsc_format(entry):
    return entry.replace("'d", 'ⓓ').replace("'l", 'ⓛ').replace("'m", 'ⓜ').replace("'r", 'ⓡ').replace("'s", 'ⓢ').replace("'t", 'ⓣ').replace("'v", 'ⓥ')

def entry_split(entry, line_split = 17, num_lines = 7):
    words = entry.split(' ')
    line_index = 0
    line_strings = [''] * num_lines

    for i in range(len(words)):
        if ((len(line_strings[line_index]) == line_split - 2 and len(words[i]) > 2)
         or (len(line_strings[line_index]) == line_split - 1 and len(words[i]) > 1)
         or (len(line_strings[line_index]) == line_split)):
            line_index += 1
        if len(line_strings[line_index]) + len(words[i]) <= line_split:
            line_strings[line_index] += words[i]
            if len(line_strings[line_index]) < line_split:
                line_strings[line_index] += ' '
        else:
            split_index = line_split - len(line_strings[line_index]) - 1
            line_strings[line_index] += words[i][:split_index] + '-'
            line_index += 1
            line_strings[line_index] += words[i][split_index:] + ' '

    return line_strings

def char_display(x, y, character, char_width = 8, char_height = 8):
    sheet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ():;[]abcdefghijklmnopqrstuvwxyz      ÄÖÜäöü          ⓓⓛⓜⓡⓢⓣⓥ       ⓃⓄ'①②-  ?!.&é ▷▶▼♂$×./,♀0123456789"
    sheet_x = (sheet.index(character) % 16) * char_width
    sheet_y = (int(sheet.index(character) / 16)) * char_height

    char_sprite = font.crop((sheet_x, sheet_y, sheet_x + char_width, sheet_y + char_height))
    img.paste(char_sprite, (x, y))

def line_display(x, y, line, char_width = 8, char_height = 8):
    for character, index in zip(line, range(len(line))):
        char_display(x + char_width * index, y, character, char_width, char_height)

def lines_display(x, y, lines, char_width = 8, char_height = 8, line_gap = 4):
    for line, index in zip(lines, range(len(lines))):
        line_display(x, y + index * (char_height + line_gap), line, char_width, char_height)

def entry_display(entry, char_width = 8, char_height = 8, line_gap = 4):
    lines_display(71, 23, entry_split(gsc_format(entry)))

def dex_data_display(number, height, weight, species, classification):
    line_display(45, 69, '{0:03d}'.format(number))

    char_display(47, 81, '.')
    line_display(33, 81, '{: >2s}'.format(str(height).split('.')[0]))
    line_display(52, 81, str(height).split('.')[1])

    char_display(41, 93, '.')
    line_display(19, 93, '{: >3s}'.format(str(weight).split('.')[0]))
    line_display(46, 93, str(weight).split('.')[1])

    line_display(71, 1, species)
    line_display(71, 12, classification + '①②')

    sprite_display(7, 7, number)

    footprint_display(195, 1, number)


def sprite_display(x, y, number, form = 0, version = 1):
    sprite_sheet = Image.open('sprites/{:03d}.png'.format(number))
    sprite = sprite_sheet.crop((0, 56 * version, 55, 55 + 56 * version))
    img.paste(sprite, (x, y), create_mask(sprite))

def footprint_display(x, y, number):
    sprite_sheet = Image.open('sprites/{:03d}.png'.format(number))
    footprint = sprite_sheet.crop((0, 112, 15, 127))
    img.paste(footprint, (x, y))


entry_display("For no reason, it jumps and splashes about, making it easy for predators like Pidgeotto to catch it mid-jump.")
dex_data_display(129, 0.9, 10.0, 'MAGIKARP', 'FISH')

img = img.rotate(180)
inky_display.set_image(img)
inky_display.show()
