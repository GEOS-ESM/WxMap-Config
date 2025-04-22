#! /usr/bin/env python

import sys
import yaml
import html
import argparse
import geopandas as gpd
import datetime as dt

from urllib.request import urlopen

from firedata import FireData, FireRecord
from wxutils.utils import *

# Get command-line arguments
# ==========================

parser = argparse.ArgumentParser(description='EONET Fire Detection')

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
cfg = config['eonet']

collection = cfg['collection']
time_window = parse_duration(cfg['time_window'])
min_duration = cfg['min_duration']
min_area = cfg['min_area']
limit = cfg['limit']
shape_file = ref_date.strftime(cfg['shape_file'])
fluid_file = ref_date.strftime(cfg['fluid_file'])
csv_file = ref_date.strftime(cfg['csv_file'])

# Get Fire Data from the EONET API
# ================================

end_date = dt.datetime.strptime(dattim, "%Y%m%d%H%M%S")
start_date = end_date - time_window
sdate = start_date.strftime("%Y-%m-%d")
edate = end_date.strftime("%Y-%m-%d")

print("Start Date =", start_date)
print("End Date =", end_date)
print("Min Area =", min_area)

#target_url = 'https://eonet.gsfc.nasa.gov/api/v3/events/geojson?source=IRWIN'
target_url = 'https://eonet.gsfc.nasa.gov/api/v3/events/geojson?source=IRWIN&start=$sdate&end=$edate&status=open'
target_url = str_replace(target_url, sdate=sdate, edate=edate)
print(target_url)
data = urlopen(target_url)

text = data.read().decode('utf-8').replace('\t','')
text = html.unescape(text)
buf = yaml.safe_load(text)

df = gpd.GeoDataFrame.from_features(buf)

# Save perimeters into shapefile
# ==============================

shape_file = time_dt.strftime(shape_file)
make_dirs(os.path.dirname(shape_file))

#dfout = df.set_crs("epsg:4326")
#dfout.to_file(shape_file)

# Bin the centroids of the polygons
# =================================

fdata = FireData()

df["centroid"] = df.centroid
centroid = df["centroid"]
title = df["title"]
descr = df["description"]
area = df["magnitudeValue"]

for i,p in enumerate(centroid):

    if area.iloc[i] < 75.0:
        continue

    record = FireRecord()
    record['lon'] = p.x
    record['lat'] = p.y
    record['fname'] = title.iloc[i]
    record['descr'] = descr.iloc[i]
    record['farea'] = area.iloc[i]
    record['frp'] = 0
    record['duration'] = 0

    print(record)
    fdata.update(record)

#fdata.combine()
#fdata.geolocate()
fdata.write(fluid_file, filter=('us','ca'))
#fdata.write(csv_file, filter=('us','ca'))
