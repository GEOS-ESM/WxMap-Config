#! /usr/bin/env python

import os
import sys
import argparse
import geopandas as gpd
import datetime as dt

from fire_data import FireData, FireRecord
from wxutils.utils import *
from datetime import datetime, timedelta
from owslib.ogcapi.features import Features

from wxutils.utils import *

# Get command-line arguments
# ==========================

parser = argparse.ArgumentParser(description='EIS Fire Detection')

parser.add_argument('datetime', metavar='datetime', type=str,
       help='ISO datetime as ccyy-mm-ddThh:mm:ss')
parser.add_argument('config', metavar='config', type=str,
       help='YAML configuration')
parser.add_argument('-t', '--target', metavar='target', type=str,
                    default='eis', help='Targeted config theme')

args = parser.parse_args()

dattim = re.sub('[^0-9]', '', args.datetime+'000000')[0:14]
idate = int(dattim[0:8])
itime = int(dattim[8:14])
time_dt = dt.datetime.strptime(dattim,'%Y%m%d%H%M%S')
ref_date = dt.datetime.strptime(dattim[0:8],'%Y%m%d')

# Retrieve configuration parameters
# =================================

config = read_yaml(args.config)
cfg = config[args.target]

url = cfg['url']
collection = cfg['collection']
time_window = parse_duration(cfg['time_window'])
time_lag = parse_duration(cfg['time_lag'])
bbox = cfg['bbox']
min_duration = cfg['min_duration']
min_area = cfg['min_area']
maxrec = cfg['limit']
shape_file = ref_date.strftime(cfg['shape_file'])
fluid_file = ref_date.strftime(cfg['fluid_file'])
csv_file = ref_date.strftime(cfg['csv_file'])

w = Features(url=url)

# Get the most recent fire perimeters
# most_recent_time = max(*perm["extent"]["temporal"]["interval"])
# ===============================================================

end_date = dt.datetime.strptime(dattim, "%Y%m%d%H%M%S")
start_date = end_date - time_window
end_date += parse_duration('PT23H59M59S')
#end_date = end_date - time_lag
    
start_date = start_date.strftime("%Y-%m-%dT%H:%M:%S+00:00")
end_date = end_date.strftime("%Y-%m-%dT%H:%M:%S+00:00")
filter = "farea>{} AND duration>{}".format(min_area, min_duration)
    
print("Start Date =", start_date)
print("End Date =", end_date)
print(filter)

features = []
for page in range(0, maxrec, 100):

    limit = min(100, maxrec-page)

    print(page, limit)
    perm_results = w.collection_items(
        collection,  # name of the dataset we want
        datetime=[start_date + "/" + end_date],  # date range
        limit=limit,  # max number of items returned
        offset=page,
        bbox = bbox
    #   filter=filter   # additional filters based on queryable fields
    )

    features.extend(perm_results["features"])


df = gpd.GeoDataFrame.from_features(features)

# Save perimeters into shapefile
# ==============================

shape_file = time_dt.strftime(shape_file)
#make_dirs(os.path.dirname(shape_file))
#os.makedirs(shape_file)

if os.path.exists(shape_file):
    for filename in os.listdir(shape_file):
        file_path = os.path.join(shape_file, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
    os.rmdir(shape_file)

dfout = df.set_crs("epsg:4326")
dfout.to_file(shape_file)

# Bin the centroids of the perimeter polygons
# ===========================================

fdata = FireData()

df["centroid"] = df.centroid
centroid = df["centroid"]
meanfrp = df["meanfrp"]
farea = df["farea"]
duration = df["duration"]

for i,p in enumerate(centroid):

    record = FireRecord()
    record['lon'] = p.x
    record['lat'] = p.y
    record['duration'] = duration.iloc[i]
    record['farea'] = farea.iloc[i]
    record['frp'] = meanfrp.iloc[i]

    fdata.update(record)

#fdata.combine()
#fdata.geolocate()
fdata.write(fluid_file, filter=('us','ca'))
#fdata.write(csv_file, filter=('us','ca'))
