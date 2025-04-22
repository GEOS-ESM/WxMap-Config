#! /usr/bin/env python

import sys
import argparse
import datetime as dt

from firedata import FireData, FireRecord
from wxutils.utils import *
from datetime import datetime, timedelta

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

# Get command-line arguments
# ==========================

parser = argparse.ArgumentParser(description='EIS Fire Detection')

parser.add_argument('datetime', metavar='datetime', type=str,
       help='ISO datetime as ccyy-mm-ddThh:mm:ss')
parser.add_argument('config', metavar='config', type=str,
       help='YAML configuration')

args = parser.parse_args()

dattim = re.sub('[^0-9]', '', args.datetime+'000000')[0:14]
idate = int(dattim[0:8])
itime = int(dattim[8:14])
time_dt = dt.datetime.strptime(dattim,'%Y%m%d%H%M%S')
ref_date = dt.datetime.strptime(dattim[0:8],'%Y%m%d')

# Retrieve configuration parameters
# =================================

config = read_yaml(args.config)
cfg = config['firms']

time_window = parse_duration(cfg['time_window'])
bbox = cfg['bbox']
min_duration = cfg['min_duration']
min_area = cfg['min_area']
limit = cfg['limit']
shape_file = ref_date.strftime(cfg['shape_file'])
fluid_file = ref_date.strftime(cfg['fluid_file'])
json_file = ref_date.strftime(cfg['json_file'])
csv_file = ref_date.strftime(cfg['csv_file'])

# Get the fire data from the FIRMS API
# ====================================

end_date = dt.datetime.strptime(dattim, "%Y%m%d%H%M%S")
start_date = end_date - time_window
    
print("Start Date =", start_date)
print("End Date =", end_date)

url_link = "https://firms.modaps.eosdis.nasa.gov/api/area/csv/1d2a6ac399b1a34639f788c6c701cd6c/VIIRS_NOAA20_NRT/-174,10,-60,70/7/%Y-%m-%d"
url_link = ref_date.strftime(url_link)
content = urlopen(url_link)

fdata = FireData()

for i, line in enumerate(content):
    if i==0:
        continue
    line = line.decode('UTF-8').strip().split(',')

    frp = float(line[12])
    if frp < 25.0:
        continue

    record = FireRecord()
    record['lon'] = float(line[1])
    record['lat'] = float(line[0])
    record['duration'] = 0
    record['farea'] = 0
    record['frp'] = float(line[12])

    fdata.update(record)

#fdata.combine()
#fdata.geolocate()
fdata.write(fluid_file, filter=('us','ca'))
fdata.writeJSON(json_file, filter=('us','ca'))
#fdata.write(csv_file, filter=('us','ca'))
