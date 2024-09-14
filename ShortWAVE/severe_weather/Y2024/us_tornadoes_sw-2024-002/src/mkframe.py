#! /usr/bin/env python

import sys
import os
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
  # im_main = image_trim(im_main)
  # im_main = im_main.crop((1, 34, 3840, 2126))
  # im_main = im_main.resize((3840, 2160), Image.ANTIALIAS)
    
    im_final = Image.new('RGB', (im_main.width, im_main.height), color='black')
    im_final.paste(im_main, (0, 0), im_main)
    im_main.close()

    # Set the font and font color

    bold_name = request['bold_name']
    font_name = request['font_name']
    font_color = request['font_color'].split()
    font_color = tuple([int(c) for c in font_color])

    # Add place names
    
    PLACES = []

    WLON = 18.0
    ELON = 32.0
    SLAT = 35.0
    NLAT = 42.0

    places = []
    for place in PLACES:
        lon, lat, name = place.split()
        x = ((float(lon) - WLON) / (ELON-WLON)) * 3840
        y = 2160 - ((float(lat) - SLAT) / (NLAT-SLAT)) * 2160
        places.append(str(int(round(x))) + ' ' + str(int(round(y))) + ' ' + name)

    im_draw_places(im_final, places, bold_name, 45)

    # Add the colorbar and title

    d1 = HersheyDraw(im_final, bold_name, 90, font_color)
    s1 = 'U.S. Tornado Outbreak'
    w1, h1 = d1.text_size(s1)

    d2 = HersheyDraw(im_final, font_name, 45, font_color)
    s2 = '24hr Accumulated Precipitation [mm]'
    w2, h2 = d2.text_size(s2)

    d3 = HersheyDraw(im_final, font_name, 36, font_color)
    s3 = '*Red polygons indicate NWS storm based warnings'
    w3, h3 = d3.text_size(s3)

    d5 = HersheyDraw(im_final, font_name, 36, font_color)
    s5 = '*White indicates elevated lightning using GEOS-CF flashrate'
    w5, h5 = d5.text_size(s5)

    im_cbar = Image.open('aprcp_cbar.png').convert("RGBA")
    im_cbar = image_trim(im_cbar)
    im_cbar = im_cbar.resize((im_final.width/3,im_final.height/28), Image.ANTIALIAS)
    w4, h4 = (im_cbar.width, im_cbar.height)
    box = round_rectangle((max(w1,w2,w3,w4)+40, h1+h2+h3+h4+h5+20+30), 50, (0,0,0,80))
    box = ImageOps.flip(box)
    im_final.paste(box, (0, 0), box)
    d1.draw_text(10, 10, s1)
    d2.draw_text(10, 10+h1+10, s2)
    im_final.paste(im_cbar, (10, 10+h1+10+h2+10), im_cbar)
    d3.draw_text(10, 10+h1+10+h2+10+h4+10, s3)
    d5.draw_text(10, 10+h1+10+h2+10+h4+10+h3+10, s5)

    # Add the model and date/time label

    d1 = HersheyDraw(im_final, bold_name, 50, font_color)
    w1, h1 = d1.text_size('GEOS Analysis')

    d2 = HersheyDraw(im_final, font_name, 50, font_color)
    w2, h2 = d2.text_size(cdattim)

    box = round_rectangle((max(w1,w2)+20, h1+h2+40), 50, (0,0,0,80))
    im_final.paste(box, (0, im_final.height-box.height), box)

    x = 10
    y = im_final.height - box.height + 10
    d1.draw_text(x, y, 'GEOS Analysis')

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
