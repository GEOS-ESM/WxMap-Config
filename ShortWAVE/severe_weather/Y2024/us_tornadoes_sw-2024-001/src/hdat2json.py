#! /usr/bin/env python

import os
import sys
import json
import time

def read_track_data(file):
                
    feature = {}       
    rows    = []
                
    with open(file,'r') as f: lines = f.readlines()
                
    for line in lines:
                   
        line = " ".join(line.split())
        columns = [s.strip() for s in line.split(',') if s != '']
                 
        if len(columns) == 3:
            name = "_".join(columns[0:-1])
            rows = []
            feature[name] = rows
        else: 
            rows.append(columns)
                   
    return feature

def track_unpack(record):
        
    date, time, dummy, type, lat, lon = record[0:6]
    dattim = date+time
    year = int(dattim[0:4])
    month = int(dattim[4:6])
    day = int(dattim[6:8])
    hour = int(dattim[8:10])
      
    rlon = float(lon[0:-1])
    rlat = float(lat[0:-1])
    if lon[-1] == 'W': rlon *= -1.0
    if lat[-1] == 'S': rlat *= -1.0 

    return (year, month, day, hour, type, rlat, rlon)

tdata = read_track_data(sys.argv[1])

tnew = {}
for name, records in iter(tdata.items()):

    urecords = []

    for rec in records:
        print (rec)
        year, month, day, hour, type, rlat, rlon = track_unpack(rec)
        urecords.append( (year, month, day, hour, type, rlat, rlon) )

    tnew[name] = urecords

#tdata = json.dumps(tnew)
with open(sys.argv[2], 'w') as f:
    json.dump(tnew, f)
  # f.write(tdata)
