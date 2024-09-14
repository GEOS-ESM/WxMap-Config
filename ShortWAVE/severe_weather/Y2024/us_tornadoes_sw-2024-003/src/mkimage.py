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

    dattim = oname.split('.')[-2]
    dattim = dattim.split('_')
    dattim = ''.join(dattim[-2:])
    time_dt = dt.datetime.strptime(dattim, "%Y%m%d%H%M")
    datlab = time_dt.strftime("%Y-%m-%dT%H:00:00")

    oname = 'us_tornadoes_sw-2024-003.nasa.gmao.geos-fp.conus_2km_replay.max_uphelicity.image.2160p.' + datlab + '.png'

    # Paste image onto a black canvas
    # Use RGB mode (i.e. no alpha channel for the canvas)

    im_main = Image.open(fname).convert("RGBA")
    im_main = im_main.resize((3840, 2160), Image.ANTIALIAS)
    
    im_final = Image.new('RGB', (im_main.width, im_main.height), color='black')
    im_final.paste(im_main, (0, 0), im_main)
    im_main.close()

    # Save the final image.

    im_final.save(oname, format='png')
