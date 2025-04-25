#! /usr/bin/env python

import sys
import os
from PIL import Image

from imutils import *

fname = sys.argv[1]

img = Image.open(fname).convert("RGBA")
img = image_trim(img)
img.save(fname, format='png')
img.close()
