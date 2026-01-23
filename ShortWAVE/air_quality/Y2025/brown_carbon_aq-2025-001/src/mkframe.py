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

im_cbar = Image.open('brown_carbon_cbar.png').convert("RGBA")
#im_cbar = image_trim(im_cbar)
#im_cbar = im_cbar.resize((round(3840/3),round(2160/28)), Image.LANCZOS)

with open('states.json', 'r') as f:
    states = json.load(f)

with open('cities.json', 'r') as f:
    cities = json.load(f)

lons = [-115, 0]
lats = [-10.0, 50.0]
bbox = [lons[0], lats[0], lons[-1], lats[-1]]

im_main = Image.open(sys.argv[1]).convert("RGBA")
im_main = ImageMapper(im_main, bbox)

state_places = []
for state in states:
    x, y = im_main.to_pixel((state[1], state[2]))
    if x < 0 or y < 0:
        continue
    if x > 3840 or y > 2150:
        continue
    state = "{} {} {}".format(x, y, state[0].upper())
    state_places.append(state)

city_places = []
for city in cities:
    x, y = im_main.to_pixel((city[1], city[2]))
    if x < 0 or y < 0:
        continue
    if x > 3840 or y > 2150:
        continue
    city = "{} {} {}".format(x, y, city[0])
    city_places.append(city)

for fname in sys.argv[1:]:

    # Open main image

    oname = os.path.basename(fname)

    dattim = oname.split('.')[-2]
    time_dt = dt.datetime.strptime(dattim, "%Y%m%dT%H%M%S")

    # Switch timezone to EST/EDST

  # from_zone = tz.gettz('UTC')
  # to_zone = tz.gettz('America/New_York')
  # time_dt = time_dt.replace(tzinfo=from_zone).astimezone(to_zone)

    # Set the format for the time string label

    cdattim = time_dt.strftime("%d %b %Y %H:%M GMT")
    print(cdattim)

    # Paste image onto a black canvas
    # Use RGB mode (i.e. no alpha channel for the canvas)

    im_main = Image.open(fname).convert("RGBA")

    im_final = Image.new('RGB', (im_main.width, im_main.height), color='black')
    im_final.paste(im_main, (0, 0), im_main)
    im_main.close()

    # Set the font and font color

    bold_name = request['bold_name']
    font_name = request['font_name']
    font_color = request['font_color'].split()
    font_color = tuple([int(c) for c in font_color])

    # Add state names
#   im_draw_places(im_final, state_places, bold_name, 56, position='c')

    # Add city names
#   im_draw_places(im_final, city_places, bold_name, 56, position='tr', radius=15, outline='black', fill='white', width=2)

    # Add the colorbar and title

#   d1 = HersheyDraw(im_final, bold_name, 90, font_color)
#   s1 = 'Carbon Origins'
#   w1, h1 = d1.text_size(s1)

#   d2 = HersheyDraw(im_final, font_name, 45, font_color)
#   s2 = 'Aerosol Optical Thickness'
#   w2, h2 = d2.text_size(s2)

#   w4, h4 = (im_cbar.width, im_cbar.height)
#   box = round_rectangle((max(w1,w2,w4)+40, h1+h2+h4+40), 50, (0,0,0,80))
#   box = ImageOps.flip(box)
#   im_final.paste(box, (0, 0), box)
#   d1.draw_text(10, 10, s1)
#   d2.draw_text(10, 10+h1+10, s2)
#   im_final.paste(im_cbar, (10, 10+h1+10+h2+10), im_cbar)

    d1 = HersheyDraw(im_final, font_name, 90, font_color)
    s1 = 'Aerosol Optical Thickness'
    w1, h1 = d1.text_size(s1)

    w4, h4 = (im_cbar.width, im_cbar.height)
    box = round_rectangle((max(w1,w4)+40, h1+h4+30), 50, (0,0,0,80))
    box = ImageOps.flip(box)
    im_final.paste(box, (0, 0), box)
    d1.draw_text(10, 10, s1)
    im_final.paste(im_cbar, (10, 10+h1+10), im_cbar)

    # Add the model and date/time label

    d1 = HersheyDraw(im_final, bold_name, 64, font_color)
    w1, h1 = d1.text_size('GEOS 2km Replay')

    d2 = HersheyDraw(im_final, font_name, 64, font_color)
    w2, h2 = d2.text_size(cdattim)

    box = round_rectangle((max(w1,w2)+20, h1+h2+40), 50, (0,0,0,80))
    im_final.paste(box, (0, im_final.height-box.height), box)

    x = 10
    y = im_final.height - box.height + 10
    d1.draw_text(x, y, 'GEOS 2km Replay')

    y += h1 + 10
    d2.draw_text(x, y, cdattim)

    # Add logos

    box = round_rectangle((200,200), 50, (0,0,0,80))
    box = ImageOps.flip(box)
    box = ImageOps.mirror(box)
    im_final.paste(box, (im_final.width-box.width,0), box)

    xsize = 150
    x = im_final.width - xsize - 10
    y = 10
    logo_name = request['nasa_logo_name']
    xs, ys = im_paste_file(im_final, logo_name, x, y, xsize=xsize)

    y += ys + 10
    logo_name = request['gmao_logo_name']
    xs, ys = im_paste_file(im_final, logo_name, x, y, xsize=xsize, ysize=200)

    # Save the final annotated image.

    im_final.save(oname, format='png')
