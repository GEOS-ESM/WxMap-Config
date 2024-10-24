#! /usr/bin/env python

import sys
import os
import json
import datetime as dt
from dateutil import tz
from PIL import Image, ImageOps

from imutils import *

request = {
    'font_color': '255 255 255',
    'bold_name': '/home/jardizzo/src/FLUID/sandbox/share/files/helr65w.ttf',
    'font_name': '/home/jardizzo/src/FLUID/sandbox/share/files/helr65w.ttf',
    'nasa_logo_name': '/home/jardizzo/src/FLUID/sandbox/share/files/nasa-logo.png',
    'gmao_logo_name': '/home/jardizzo/src/FLUID/sandbox/share/files/gmao-logo-white.png'
    }

im_cbar = Image.open('tprcp_cbar.png').convert("RGBA")
im_cbar = image_trim(im_cbar)
im_cbar = im_cbar.resize((3840/3, 2160/28), Image.ANTIALIAS)

with open('states.json', 'r') as f:
    states = json.load(f)

lons = [-92.0, -66.0]
lats = [25.0, 39.0]
bbox = [lons[0], lats[0], lons[-1], lats[-1]]

for fname in sys.argv[1:]:

    # Open main image

    oname = os.path.basename(fname)

    dattim = oname.split('.')[-2]
    time_dt = dt.datetime.strptime(dattim, "%Y%m%d%H")

    # Switch timezone to EST/EDST

  # from_zone = tz.gettz('UTC')
  # to_zone = tz.gettz('America/New_York')
  # time_dt = time_dt.replace(tzinfo=from_zone).astimezone(to_zone)

    # Set the format for the time string label

    cdattim = time_dt.strftime("%d %b %Y %H:00 GMT")
    print(cdattim)

    # Paste image onto a black canvas
    # Use RGB mode (i.e. no alpha channel for the canvas)

    im_main = Image.open(fname).convert("RGBA")
    im_main = ImageMapper(im_main, bbox)
  # im_main = im_main.resize((3840, 2160), Image.ANTIALIAS)

    state_places = []
    for state in states:
        x, y = im_main.to_pixel((state[1], state[2]))
        if x < 0 or y < 0:
            continue
        if x > 3840 or y > 2150:
            continue
        state = "{} {} {}".format(x, y, state[0].upper())
        state_places.append(state)
    
    im_main = im_main.img
    im_final = Image.new('RGB', (im_main.width, im_main.height), color='black')
    im_final.paste(im_main, (0, 0), im_main)
    im_main.close()

    # Set the font and font color

    bold_name = request['bold_name']
    font_name = request['font_name']
    font_color = request['font_color'].split()
    font_color = tuple([int(c) for c in font_color])

    # Add state names
    im_draw_places(im_final, state_places, bold_name, 28, position='c')

    # Save the final annotated image.

    im_final.save(oname, format='png')