#! /usr/bin/env python

import sys
import os
from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None

iname = sys.argv[1]
oname = sys.argv[2]

immap = Image.open(iname).convert("L")

# Change luminosity of image except where very dark.

in_data  = immap.getdata()
out_data = []
for i in range(0, len(in_data)):

    L = in_data[i]
 #  if L <= 5:
    if L <= 8:
        out_data.append(0)
    else:
        out_data.append(min(L+75,255))

immap.putdata(out_data)

print(immap.size)
im_final = Image.new('RGB', immap.size, color='black')
im_final.paste(immap, (0, 0), immap)
im_final.save(oname, format='png')
