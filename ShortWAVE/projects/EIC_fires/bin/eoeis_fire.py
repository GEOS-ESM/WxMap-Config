#! /usr/bin/env python

import sys
import argparse
import geopandas as gpd
import datetime as dt

from fire_api import *
from fire_data import FireData, FireRecord
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
cfg = config['eoeis']
cfg_eis = config['eis']

one_day = parse_duration('P1D')
time_window = parse_duration(cfg['time_window'])
shape_file = ref_date.strftime(cfg['shape_file'])
fluid_file = ref_date.strftime(cfg['fluid_file'])
csv_file = ref_date.strftime(cfg['csv_file'])

# Get Fire Data Using the EONET and EIS APIs
# ==========================================

end_date = dt.datetime.strptime(dattim, "%Y%m%d%H%M%S")
start_date = end_date - time_window
end_date += parse_duration('PT23H59M59S')

eonet = get_eonet(start_date, end_date, **cfg).set_crs("EPSG:2163")
eis = get_eis(start_date, end_date, **cfg_eis).set_crs("EPSG:2163")
eis = eis.sort_values(by='t').drop_duplicates(subset='fireid', keep='last')
buf = eis.geometry.buffer(0.07)
eis['geometry'] = buf

df = gpd.sjoin(eonet, eis, how='inner', predicate='within')
#df = gpd.overlay(eonet, eis, how='intersection')
#df = gpd.sjoin(eonet, eis, how='inner', predicate='intersects')

# Save perimeters into shapefile
# ==============================

shape_file = time_dt.strftime(shape_file)
make_dirs(os.path.dirname(shape_file))

# Bin the centroids of the polygons
# =================================

fdata = FireData()

df["centroid"] = df.centroid
centroid = df["centroid"]
id = df["id"]
title = df["title"]
descr = df["description"]
#area = df["magnitudeValue"]
area = df["farea"]

for i,p in enumerate(centroid):

    acres = round(float(area.iloc[i]) * 247.105)
    if acres < 75.0:
        continue

    record = FireRecord()
    record['lon'] = p.x
    record['lat'] = p.y
    record['fname'] = title.iloc[i]
    record['id'] = id.iloc[i]
    record['descr'] = descr.iloc[i]
    record['farea'] = acres
    record['frp'] = 0
    record['duration'] = 0

    print(record)
    fdata.update(record)

#fdata.combine()
#fdata.geolocate()
fdata.sort(key='farea', maxrec=100)
fdata.write(fluid_file, filter=('us','ca'))
#fdata.write(csv_file, filter=('us','ca'))
