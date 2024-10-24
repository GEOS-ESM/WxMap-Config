#! /usr/bin/env python

import sys
import os
import datetime as dt

for fname in sys.argv[1:]:

    # Open main image

    iname = os.path.basename(fname)

    dattim = iname.split('.')[-2]
    time_dt = dt.datetime.strptime(dattim, "%Y%m%d%H")

    oname = iname.split('.')[0:-2]
    oname = time_dt.strftime('.'.join(oname) + '.%Y-%m-%dT%H:%M:%S.png')
    oname = oname.replace('image', 'overlay-1')
    oname = oname.replace('t2m', 'tprcp')

    print(oname)
    os.rename(fname, oname)
