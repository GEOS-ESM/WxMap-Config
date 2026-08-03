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

odir = sys.argv[1]
os.makedirs(odir, mode=0o755, exist_ok=True)

for fname in sys.argv[2:]:

    # Open main image

    oname = os.path.basename(fname)
    oname = oname.replace('base', 'timestamp')
    oname = os.path.join(odir, oname)

    dattim = oname.split('.')[-2]
    time_dt = dt.datetime.strptime(dattim, "%Y%m%dT%H%M%S")

    # Switch timezone to EST/EDST

  # from_zone = tz.gettz('UTC')
  # to_zone = tz.gettz('America/New_York')
  # time_dt = time_dt.replace(tzinfo=from_zone).astimezone(to_zone)

    # Set the format for the time string label

    cdattim = time_dt.strftime("%d %b %Y %H:00 UTC")
    print(cdattim)

    # Paste image onto a black canvas
    # Use RGB mode (i.e. no alpha channel for the canvas)

    im_final = Image.new('RGBA', (7680,3840), color=(0,0,0,0))

    # Set the font and font color

    bold_name = request['bold_name']
    font_name = request['font_name']
    font_color = request['font_color'].split()
    font_color = tuple([int(c) for c in font_color])

    # Add the model and date/time label

    model_color = font_color
    model = 'GEOS-CAM Replay'

    d1 = HersheyDraw(im_final, bold_name, 100, model_color)
    w1, h1 = d1.text_size(model)

    d2 = HersheyDraw(im_final, font_name, 100, model_color)
    w2, h2 = d2.text_size(cdattim)

    box = round_rectangle((max(w1,w2)+20, h1+h2+40), 50, (0,0,0,80))
    im_final.paste(box, (0, im_final.height-box.height), box)

    x = 10
    y = im_final.height - box.height + 10
    d1.draw_text(x, y, model)

    y += h1 + 10
    d2.draw_text(x, y, cdattim)

    # Save the final annotated image.

    im_final.save(oname, format='png')
