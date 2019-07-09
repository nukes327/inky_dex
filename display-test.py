import time
from inky import InkyPHAT
from PIL import Image, ImageDraw

inky_display = InkyPHAT('yellow')
inky_display.set_border(inky_display.BLACK)

img = Image.open('dex-background.png')

for i in (2, 3, 5, 6, 8, 9):
    try:
        sprite = Image.open('sprites/{0:03d}-2s.png'.format(i))
    except IOError:
        continue
    
    if sprite is not None:
        print('Current sprite is {0:03d}-2s.png'.format(i))
        img.paste(sprite, (6, 7))
        inky_display.set_image(img)
        inky_display.show()
        time.sleep(1)

#sprite = Image.open('sprites/004-2s.png')

#img.paste(sprite, (6 , 7))
#inky_display.set_image(img)
#inky_display.show()
