#! /usr/bin/env python

import os
import sys
import datetime as dt
from gradient import *
from PIL import Image, ImageOps, ImageDraw, ImageChops
from imutils import image_trim, HersheyDraw

SRCDIR = '/home/jardizzo/src/FLUID/sandbox/share/files'

request = {
    'font_color': '255 255 255',
    'bold_name': os.path.join(SRCDIR, 'helr65w.ttf'),
    'font_name': os.path.join(SRCDIR, 'helr65w.ttf'),
    'nasa_logo_name': os.path.join(SRCDIR, 'nasa-logo.png'),
    'gmao_logo_name': os.path.join(SRCDIR, 'gmao-logo-white.png')
    }  

for fname in sys.argv[1:]:

    # Open main image

    oname = os.path.basename(fname)

    im_main = Image.open(fname).convert("RGBA")
    im_main = image_trim(im_main)

    # Paste legend onto main.

    im_final = Image.new('RGB', (im_main.width, im_main.height), color='black')
    im_final.paste(im_main, (0, 0), im_main)

    # Apply gradient to final image

    w, h = (im_final.width, im_final.height)
    xmid = int(round(w/2))
    ymid = int(round(h/2))

    polygon = [(0, 0), (xmid, 0), (xmid, h), (0, h)]
    point1 = (0, ymid)
    point2 = (xmid, ymid)
    color1 = (0, 0, 0, 255)
    color2 = (0, 0, 0, 0)
    im_final = linear_gradient(im_final, polygon, point1, point2, color1, color2)

    # Set the font and font color

    bold_name = request['bold_name']
    font_name = request['font_name']
    font_color = request['font_color'].split()
    font_color = tuple([int(c) for c in font_color])

    # Add the title

    d1 = HersheyDraw(im_final, bold_name, 48, font_color)
    s1 = 'MERRA-2 ENSO'
    w1, h1 = d1.text_size(s1)

    d2 = HersheyDraw(im_final, bold_name, 48, font_color)
    s2 = 'COMPOSITE'
    w2, h2 = d1.text_size(s1)

    d1.draw_text(8, 8, s1)
    d2.draw_text(8, 8+h1+8, s2)

    im_final.save(oname, format='png')
