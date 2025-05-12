#! /usr/bin/env python

import sys
import os
from PIL import Image, ImageOps

from imutils import *

background = '/discover/nobackup/jardizzo/maps/BlackMarble_2016/BlackMarble_2016_4320x2160.enhanced.png'
im_bkg = Image.open(background).convert("RGBA")

for fname in sys.argv[1:]:

    oname = os.path.basename(fname)

    im_main = Image.open(fname).convert("RGBA")
    im_final = Image.new('RGB', (im_main.width, im_main.height), color='black')
    im_final.paste(im_bkg, (0, 0), im_bkg)
    im_final.paste(im_main, (0, 0), im_main)
    im_main.close()

    # Save the final annotated image.

    im_final.save(oname, format='png')
