#! /usr/bin/env python

import os
import sys
import copy
import datetime as dt

tag = 0
for file in sys.argv[1:]:

    cdate = file.split('_')[0]
    year = int('20' + cdate[0:2])
    month = int(cdate[2:4])
    day = int(cdate[4:])

    dattim = dt.datetime(year, month, day)

    with open(file,'r') as f:

        lines = f.readlines()
     #  line = lines[1].split(',')
        
        for line in lines[1:]:

            line = line.split(',')
            ctime = line[0].strip()
            hour = int(ctime[0:2])
            minute  = int(ctime[2:])
            lat = line[5] + 'N'
            lon = line[6][1:] + 'W'

            curdattim = dattim
            if hour < 12: curdattim = dattim + dt.timedelta(hours=24)

            curdattim += dt.timedelta(hours=hour, minutes=minute)
            enddattim = curdattim + dt.timedelta(hours=24)

            sdattim = curdattim.strftime('%Y%m%d,%H%M')
            edattim = enddattim.strftime('%Y%m%d,%H%M')
            
            fill = ['-999'] * 14
            line1 = [sdattim, ' ', 'TND', lat, lon] + fill
            line2 = [edattim, ' ', 'TND', lat, lon] + fill

            print('TND%04d, NONAME, 2'%tag)
            print(','.join(line1))
            print(','.join(line2))

            tag += 1
