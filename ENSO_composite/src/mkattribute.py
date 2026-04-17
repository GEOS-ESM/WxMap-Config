#! /usr/bin/env python

import os
import sys
import numpy as np
import ruamel.yaml as yaml

def round_nearest(number, base):
    x = base * round(number / base)
    return int(x*10000) / 10000.0

def interval(range, increment):

    if range == 0:
        return 0

    x = range / float(increment)

    i = 1
    cint = round(x, i)

    while cint == 0:
        i += 1
        cint = round(x, i)

    if cint > 1:
        return round(cint)
    else:
        return cint

attribute = []
name = os.path.basename(sys.argv[1])
field = name.split('.')[0]

for file in sys.argv[1:]:

    name = os.path.basename(file)
    region = name.split('.')[1]

    with open(file, 'r') as f:
        lines = f.readlines()

    N = 0
    for line in lines:
        buf = line.strip().split(',')
        rmin = float(buf[1])
        rmax = float(buf[2])
        rmean = float(buf[3])

        if N == 0:
            cmin = rmin
            cmax = rmax
            cmean = rmean
        else:
            if rmin < cmin:
                cmin = rmin
            if rmax > cmax:
                cmax = rmax
            cmean += rmean

        N += 1

    if 'std' in field:
        cmin = 0.0
        cmean = cmean / N
        range = cmax - cmin
        low = cmin + range * 0.25
        high = cmax - range * 0.25
        cint = interval(range, 10.0)
      # cmin = int(cmin - cmin%cint)
        cmax = round_nearest(cmax, cint)

    elif 'anom' in field:

        if abs(cmin) >= abs(cmax):
            cmin = -abs(cmin)
            cmax = abs(cmin)
        else:
            cmin = -abs(cmax)
            cmax = abs(cmax)

        cmean = cmean / N
        range = cmax - cmin
        low = None
        high = None
        cint = interval(range, 10.0)
        cmax = round_nearest(cmax, cint)
        cmin = -cmax

    else:

        cmean = cmean / N
        range = cmax - cmin
        cmin = cmin + 0.1 * range
        cmax = cmax - 0.1 * range
        low = cmin + range * 0.25
        high = cmax - range * 0.25
        cint = interval(range, 10.0)
        cmin = round_nearest(cmin, cint)
        cmax = round_nearest(cmax, cint)

    d = {}
    d['$region'] = region
    d['cmin'] = cmin
    d['cmax'] = cmax
    d['cint'] = cint
    if low is not None and cmean <= low:
        d['scale'] = 'exp_scale'
    if high is not None and cmean >= high:
        d['scale'] = 'log_scale'

    attribute.append(d)

cfg = {}
cfg['theme'] = {}
cfg['theme']['attribute'] = {}
cfg['theme']['attribute'][field + '_attr'] = attribute
with open('tt.yaml', 'w') as f:
    yaml.dump(cfg, f)
