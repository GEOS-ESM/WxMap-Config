#! /usr/bin/env python

import sys
import os
import datetime as dt
from dateutil import tz
from PIL import Image, ImageOps, ImageChops

from imutils import im_paste_file, HersheyDraw

def image_trim(im, margin=0):

    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = list(diff.getbbox())
    if bbox:
        bbox[0] -= margin
        bbox[1] -= margin
        bbox[2] += margin
        bbox[3] += margin
        print(bbox)
        return im.crop(bbox)
    return im

request = {
    'font_color': '255 255 255',
    'font_name': 'helr45w.ttf',
    'date_box_name': 'date-box-curved-corner-500x100px.png',
    'logo_box_name': 'logo-box-curved-corner-350x75px.png',
    'nasa_logo_name': 'nasa-logo.png',
    'gmao_logo_name': 'gmao-logo-white.png'
    }

for fname in sys.argv[1:]:

    # Open main image

    oname = os.path.basename(fname)

    dattim = oname.split('.')[-2]
    time_dt = dt.datetime.strptime(dattim, "%Y%m%d%H")

    # Switch timezone to EST/EDST

    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/New_York')
    time_dt = time_dt.replace(tzinfo=from_zone).astimezone(to_zone)

    # Set the format for the time string label

    cdattim = time_dt.strftime("%d %b %Y %H:%M:%S %Z")
    print(cdattim)

    # Paste image onto a black canvas
    # Use RGB mode (i.e. no alpha channel for the canvas)

    im_main = Image.open(fname).convert("RGBA")
    im_main = image_trim(im_main)
    im_main = im_main.resize((2048, 1024), Image.ANTIALIAS)
    
    im_final = Image.new('RGB', (im_main.width, im_main.height), color='black')
    im_final.paste(im_main, (0, 0), im_main)
    im_main.close()

    # Set the font and font color

    font_name = request['font_name']
    font_color = request['font_color'].split()
    font_color = (255, 255, 255)

    # Paste the date shadow box onto the final image

    box_name = request['date_box_name']
    im_paste_file(im_final, box_name, 0, 925)

    # Add the date/time label

    x = 30
    y = 954
    d = HersheyDraw(im_final, font_name, 37, font_color)

    s = cdattim[0:6]
    w, h = d.text_size(s)
    d.draw_text(x, y, s)
    x += 123

    s = cdattim[6:]
    w, h = d.text_size(s)
    d.draw_text(x, y, s)

    # Paste the logo shadow box onto the final image

    box_name = request['logo_box_name']
    im_paste_file(im_final, box_name, 0, 0)

    # Add logos

    x = 51
    y = 18
    logo_name = request['nasa_logo_name']
    xs, ys = im_paste_file(im_final, logo_name, x, y, ysize=50)

    x += xs + 10
    y = 25
    logo_name = request['gmao_logo_name']
    xs, ys = im_paste_file(im_final, logo_name, x, y, ysize=35)

    # Save the final annotated image.

    im_final.save(oname, format='png')
