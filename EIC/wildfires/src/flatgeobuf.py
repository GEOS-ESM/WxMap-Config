#! /usr/bin/env python

import sys
import argparse
import geopandas as gpd
import datetime as dt

from wxutils.utils import *
#from datetime import datetime, timedelta

def str2dt(s):

  times = []
  for t in s:
      times.append(dt.datetime.strptime(t, "%Y-%m-%dT%H:%M:%S"))

  return times

# Get command-line arguments
# ==========================

parser = argparse.ArgumentParser(description='EIS Fire Detection')

parser.add_argument('datetime', metavar='datetime', type=str,
       help='ISO datetime as ccyy-mm-ddThh:mm:ss')
parser.add_argument('filename', metavar='filename', type=str,
       help='FlatGeobuf file')

args = parser.parse_args()

dattim = re.sub('[^0-9]', '', args.datetime+'000000')[0:14]
idate = int(dattim[0:8])
itime = int(dattim[8:14])
time_dt = dt.datetime.strptime(dattim,'%Y%m%d%H%M%S')
ref_date = dt.datetime.strptime(dattim[0:8],'%Y%m%d')

start_dt = dt.datetime(2024, 7, 15, 0)
end_dt = dt.datetime(2024, 9, 15, 0)
inchrs = dt.timedelta(hours=12)

df = gpd.read_file(args.filename)
template = '/discover/nobackup/jardizzo/maps/Bolivia_AMPM/Bolivia_%Y%m%d%p'

time_dt = start_dt
while time_dt <= end_dt:

    ctime = time_dt.strftime("%Y-%m-%dT%H:00:00")
    dfout = df[(df['t'] == ctime)]

    dfout = dfout.to_crs(crs="epsg:4326",epsg=4326)
    dfout = dfout.set_crs("epsg:4326")

    oname = time_dt.strftime(template)
    dfout.to_file(oname)

    time_dt += inchrs
