#! /usr/bin/env python

import os
import sys
import argparse
import datetime as dt
from PIL import Image, ImageOps, ImageDraw, ImageChops
from hershey_draw import *

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
        return im.crop(bbox)
    return im

def image_scale(im, xsize=None):

    if not xsize:
        return im

    ratio   = float(im.size[1]) / float(im.size[0])
    ysize   = int(xsize * ratio)

    return im.resize((xsize, ysize), Image.ANTIALIAS)

# Retrieve command-line arguments
# ===============================

parser = argparse.ArgumentParser(description='Annotates Hyperwall Frames')
parser.add_argument('-o', '--output-name', metavar='output name', type=str,
                    required=True, help='output filename')
parser.add_argument('-i', '--input-files', metavar='input files',
                    type=str, nargs='+', default=[])

args = parser.parse_args()

oname = args.output_name
bname = os.path.basename(oname)
files = args.input_files
var = bname.split('_')[5]

odir = os.path.dirname(files[0])
#os.makedirs(odir, mode=0o755, exist_ok=True)

# Determine title based on output variable name
# =============================================

TITLES = {"T2M": 'S2S_2.1 T2M Anomaly (`ao`nC)',
          "Precip": 'S2S_2.1 Precip Anomaly (mm/day)',
          "SST": 'S2S_2.1 SST Anomaly (`ao`nC)',
          "SSS": 'S2S_2.1 SSS Anomaly'
         }

varname = TITLES[var]

# Create canvas for combining panels
# (assume that all panels are the same size)
# ==========================================

header = 500
footer = 500
margin = 20
spacing = 20

im = image_trim(Image.open(files[0]).convert("RGBA"))
im = image_scale(im, 600)
width  = im.width * 3 + margin*2 + spacing*2
height = im.height * 9 + header + footer + spacing*2
im.close()

canvas = Image.new('RGB', (width, height), color='white')

# Create header elements on canvas
# ================================

color = (0, 0, 0)
bfont = '/home/jardizzo/src/FLUID/sandbox/share/files/helr65w.ttf'

x = margin
y = margin
d = HersheyDraw(canvas, bfont, 48, color)
w, h = d.text_size(varname)
d.draw_text(x, y, varname)

y += h + margin

#field = files[0].split('.')[-5]
#im = image_trim(Image.open(field+'.cbar.png').convert("RGBA"))
#im = image_scale(im, 1200)
#canvas.paste(im, (width/2-im.width/2, y), im)

#y += im.height + margin

# Loop over input frames and annotate
# ===================================

icol = 0
for fname in files:

    dattim = fname.split('.')[-2]
    time_dt = dt.datetime.strptime(dattim, "%Y%m%d")
    dattim = fname.split('.')[-3]
    fcst_dt = dt.datetime.strptime(dattim, "%Y%m%d")

    title = '%b %Y Release: %%b Ensemble Mean'
    title = fcst_dt.strftime(title)
    title = time_dt.strftime(title)

    # Crop the image to remove any border space.
    # ==========================================

    im = image_trim(Image.open(fname).convert("RGBA"))
    im = image_scale(im, 600)

    d = HersheyDraw(canvas, bfont, 28, color)
    s = title
    w, h = d.text_size(s)
    d.draw_text(x + im.width/2 - w/2, y, s)

    canvas.paste(im, (x, y+h+5), im)

    icol += 1
    if icol == 1:
        icol = 0
        x = margin
        y += im.height + h + 5 + spacing
    else:
        x = x + im.width + spacing

    im.close()

image_trim(canvas, 10).save(oname, format='png')

sys.exit(0)
