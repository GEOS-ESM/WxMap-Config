#! /usr/bin/env python

import sys
import os
import datetime as dt
from dateutil import tz
from PIL import Image, ImageOps

from imutils import *

def color2alpha(img, color):

    datas = img.getdata()

    new_data = []
    for item in datas:
        if item[0] == color[0] and item[1] == color[1] and item[2] == color[2]:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    img.putdata(new_data)

request = {
    'font_color': '255 255 255',
    'bold_name': '/home/jardizzo/src/FLUID/sandbox/share/files/helr65w.ttf',
    'font_name': '/home/jardizzo/src/FLUID/sandbox/share/files/helr65w.ttf',
    'nasa_logo_name': '/home/jardizzo/src/FLUID/sandbox/share/files/nasa-logo.png',
    'gmao_logo_name': '/home/jardizzo/src/FLUID/sandbox/share/files/gmao-logo-white.png'
    }

#im_map  = Image.open('map_alpha.png').convert("RGBA")
im_map  = Image.open('tpw_land_mask.png').convert("RGBA")
color2alpha(im_map, (0,0,0))
im_cbar = Image.open('tpw-2_cbar.png').convert("RGBA")
im_cbar = image_trim(im_cbar)
im_cbar = im_cbar.resize((round(3840/3), round(2160/28)), Image.LANCZOS)

im_vert_cbar = Image.open('aprcp_vertical_cbar.png').convert("RGBA")
im_vert_cbar = image_trim(im_vert_cbar)
im_vert_cbar = im_vert_cbar.resize((round(2160/28), round(3840/3)), Image.LANCZOS)

# Set up the California alpha mask

#img = Image.open('west-coast_mask.png').convert("RGBA")
img = Image.open('map_hatch.png').convert("RGBA")
cal_mask = Image.new('L', img.size, 0)
data_mask  = img.getdata()

alpha = []
for i in range(0, len(data_mask)):

    mask = data_mask[i]
    if mask[0] == 255 and mask[1] == 255 and mask[2] == 0:
        alpha.append(255)
    else:
        alpha.append(0)

cal_mask.putdata(alpha)

# Define the total precip image name

TPRECIP = '../tprcp/mediterranean_fl-2026-001.nasa.gmao.geos-fp.analysis.tprcp.image.3840x2160.%Y%m%d%H.png'


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
  # im_main = im_main.resize((3840, 2160), Image.LANCZOS)

    pname = time_dt.strftime(TPRECIP)
    im_precip = Image.open(pname).convert("RGBA")
    im_precip.putalpha(cal_mask)
    
    im_final = Image.new('RGB', (im_main.width, im_main.height), color='black')
    im_final.paste(im_main, (0, 0), im_main)
    im_final.paste(im_map, (0, 0), im_map)
    im_final.paste(im_precip, (0, 0), im_precip)
    im_main.close()

    # Set the font and font color

    bold_name = request['bold_name']
    font_name = request['font_name']
    font_color = request['font_color'].split()
    font_color = tuple([int(c) for c in font_color])

    # Add place names
    
    places = []

    im_draw_places(im_final, places, bold_name, 45)

    # Add the colorbar and title

    d1 = HersheyDraw(im_final, bold_name, 90, font_color)
    s1 = 'Western Mediterranean Flooding'
    w1, h1 = d1.text_size(s1)

    d2 = HersheyDraw(im_final, font_name, 45, font_color)
  # s2 = 'Total Precipitable Water `b[kg m-2]`n / Sea Level Pressure `b[mb]`n'
    s2 = 'Total Precipitable Water `b[kg m-2]`n'
    w2, h2 = d2.text_size(s2)

    w3, h3 = (im_cbar.width, im_cbar.height)
  # box = round_rectangle((max(w1,w2,w3)+40, h1+h2+h3+20+20), 50, (0,0,0,80))
    box = round_rectangle((w1+40, h1+20), 50, (0,0,0,80))
    box = ImageOps.flip(box)
    im_final.paste(box, (0, 0), box)
    d1.draw_text(10, 10, s1)
  # d2.draw_text(10, 10+h1+10, s2)
  # im_final.paste(im_cbar, (10, 10+h1+10+h2+10), im_cbar)

    # Add the vertical colorbar

    d1 = HersheyDraw(im_final, font_name, 24, font_color)
    s1 = 'Precip'
    w1, h1 = d1.text_size(s1)

    d2 = HersheyDraw(im_final, font_name, 24, font_color)
    s2 = '(mm)'
    w2, h2 = d2.text_size(s2)

    w, h = (im_vert_cbar.width, im_vert_cbar.height)
    box = round_rectangle((max(w,w1,w2)+30, 10+h+10+h2+10+h1+10), 50, (0,0,0,80))
    box = ImageOps.mirror(box)
    im_final.paste(box, (3840-box.width, round(2160/2-box.height/2)), box)

    x = 3840-box.width/2 - w1/2
    y = 2160/2-box.height/2 + 10
    d1.draw_text(x, y, s1)

    x = 3840-box.width/2 - w2/2
    y = y + h1 + 10
    d2.draw_text(x, y, s2)

    x = round(3840-box.width/2 - w/2)
    y = round(y + h2 + 10)
    im_final.paste(im_vert_cbar, (x,y), im_vert_cbar)

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

    overlay = []
    final_data  = im_final.getdata()
    for i in range(0, len(data_mask)):
    
        mask = data_mask[i]
        fdata = final_data[i]
        if mask[0] == 255 and mask[1] == 0 and mask[2] == 0:
            overlay.append((0,0,0,255))
        else:
            overlay.append(fdata)

    im_final.putdata(overlay)

    im_final.save(oname, format='png')
