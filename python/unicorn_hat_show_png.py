#!/usr/bin/env python

import time
from sys import exit
import sys

try:
    from PIL import Image
except ImportError:
    exit('This script requires the pillow module\nInstall with: sudo pip install pillow')

import unicornhathd


print("""Unicorn HAT HD: Show a PNG image!
""")

unicornhathd.rotation(180)
unicornhathd.brightness(0.6)

width, height = unicornhathd.get_shape()

#img = Image.open('lofi.png'')
print("Opening " + sys.argv[1])
img = Image.open(sys.argv[1])
#img = Image.open('unicorn_hat_icons/Door-icon.png')
#img = Image.open('ic-bed.png')

try:
    for o_x in range(int(img.size[0] / width)):
        for o_y in range(int(img.size[1] / height)):

            valid = False
            for x in range(width):
                for y in range(height):
                    pixel = img.getpixel(((o_x * width) + y, (o_y * height) + x))
                    r, g, b = int(pixel[0]), int(pixel[1]), int(pixel[2])
                    if r or g or b:
                        valid = True
                    unicornhathd.set_pixel(x, y, r, g, b)

            if valid:
                unicornhathd.show()
                time.sleep(0.5)

    time.sleep(2)

except KeyboardInterrupt:
    print("done")

finally:     
    unicornhathd.off()
