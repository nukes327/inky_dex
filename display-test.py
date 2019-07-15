"""
This file is a quick use hacky file for rapid testing of image work.
Additionally, new functions are like to be tested here first
"""

import time
from inky import InkyPHAT
from PIL import Image, ImageDraw

"""
Turns out if you have red in an image, but the display is set to black, it'll display as gray.
This will be convenient for quickly testing code that dynamically displays sprites on the screen
A 2 second refresh time allows for more rapid testing than a 15 second refresh time
"""
inky_display = InkyPHAT('black')
inky_display.set_border(inky_display.BLACK)

img = Image.open('johto-test.png')

def entry_split(entry):
    words = entry.split(' ')
    line_index = 0
    line_strings = ['', '', '', '', '', '', '']

    for i in range(len(words)):
        if ((len(line_strings[line_index]) == 15 and len(words[i]) > 2)
         or (len(line_strings[line_index]) == 16 and len(words[i]) > 1)
         or (len(line_strings[line_index]) == 17)):
            line_index += 1
        if len(line_strings[line_index]) + len(words[i]) <= 17:
            line_strings[line_index] += words[i]
            if len(line_strings[line_index]) < 17:
                line_strings[line_index] += ' '
        else:
            split_index = 17 - len(line_strings[line_index]) - 1
            line_strings[line_index] += words[i][:split_index] + '-'
            line_index += 1
            line_strings[line_index] += words[i][split_index:] + ' '
    
    return line_strings

#for i in (2, 3, 5, 6, 8, 9):
#    try:
#        sprite = Image.open('sprites/{0:03d}-2s.png'.format(i))
#    except IOError:
#        continue
#    
#    if sprite is not None:
#        print('Current sprite is {0:03d}-2s.png'.format(i))
#        img.paste(sprite, (7, 7))
#        inky_display.set_image(img)
#        inky_display.show()
#        time.sleep(1)

#sprite = Image.open('sprites/004-2s.png')

#img.paste(sprite, (7 , 7))
inky_display.set_image(img)
inky_display.show()

print(entry_split('A legend says that its body glows in seven colors. A rainbow is said to form behind it when it flies.'))
