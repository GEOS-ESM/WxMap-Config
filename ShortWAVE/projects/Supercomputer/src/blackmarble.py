#! /usr/bin/env python
"""
    Reads NASA BlackMarble 500m regional tiles and assembles
    a global image at the user-specified dimensions.

    This application is very useful for creating BlackMarble basemaps
    using the highest available resolution to yield the best quality.

    Usage
    -----
    geometry : string
        output image size in pixels (e.g. --geometry 2048x1024)
        Note: best to use 2:1 aspect ratio for a global image.
    grayscale: boolean
        generates a grayscale BlackMarble image (e.g. --grayscale)

    Dependencies
    ------------
    BlackMarble full resolution (500m) imagery obtained from:

    https://earthobservatory.nasa.gov/features/NightLights/page3.php

    Returns
    -------
    0: Success

"""

import sys
import os
from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None

template = '/discover/nobackup/jardizzo/maps/BlackMarble_2016/BlackMarble_2016_%panel.jpg'
oname = '/discover/nobackup/jardizzo/maps/BlackMarble_2016/BlackMarble_2016_18000x9000.png'
panels = ['A','B','C','D']

width = 21600 * 4
height = 21600 * 2

imout = Image.new('RGB', (width, height), color='black')

for row in range(1,3):

    for col in range(1,5):

        id = panels[col-1] + str(row)
        print(f'Pasting panel {id}')
        fname = template.replace('%panel', id)
        img = Image.open(fname).convert("RGBA")   

        xp = (col-1) * 21600
        yp = (row-1) * 21600

        imout.paste(img, (xp, yp), img)
        img.close()


imout = imout.resize((18000, 9000), Image.LANCZOS).convert('LA')
#imfinal = Image.new('RGB', (4320, 2160), color='black')
#imfinal.paste(imout, (0,0), imout)
imout.save(oname, format='png')
