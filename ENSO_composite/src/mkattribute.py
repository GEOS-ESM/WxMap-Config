#! /usr/bin/env python

import os
import sys
import ruamel.yaml as yaml

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

    cmin = 0.0
    cmean = cmean / N
    range = cmax - cmin
    low = cmin + range * 0.25
    high = cmax - range * 0.25

  # cmin = cmin + 0.1 * range
  # cmax = cmax - 0.1 * range
    range = cmax - cmin
    cint = round(range / 10.0)
    cmin = int(cmin - cmin%cint)
    cmax = int(cmax - cmax%cint)

    d = {}
    d['$region'] = region
    d['cmin'] = cmin
    d['cmax'] = cmax
    d['cint'] = cint
    if cmean <= low:
        d['scale'] = 'exp_scale'
    if cmean >= high:
        d['scale'] = 'log_scale'

    attribute.append(d)

cfg = {}
cfg['theme'] = {}
cfg['theme']['attribute'] = {}
cfg['theme']['attribute'][field + '_attr'] = attribute
with open('tt.yaml', 'w') as f:
    yaml.dump(cfg, f)
