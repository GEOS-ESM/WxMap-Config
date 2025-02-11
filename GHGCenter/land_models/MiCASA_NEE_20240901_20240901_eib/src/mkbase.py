#! /usr/bin/env python

import sys
import os
import datetime as dt
from dateutil import tz
from PIL import Image, ImageOps

from imutils import *

for fname in sys.argv[1:]:

    # Open main image

    oname = os.path.basename(fname)

    # Paste image onto a black canvas
    # Use RGB mode (i.e. no alpha channel for the canvas)

    im_main = Image.open(fname).convert("RGBA")
    im_main = image_trim(im_main)
  # im_main = im_main.crop((1, 34, 3839, 2125))
    im_main = im_main.resize((3840, 2160), Image.ANTIALIAS)
    
    im_final = Image.new('RGB', (im_main.width, im_main.height), color='black')
    im_final.paste(im_main, (0, 0), im_main)
    im_main.close()

    im_final.save(oname, format='png')
