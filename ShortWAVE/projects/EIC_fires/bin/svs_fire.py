#! /usr/bin/env python

import os
import re
import argparse
import datetime as dt
import ruamel.yaml as yaml

from myutils import read_yaml
from urllib.request import urlopen

# Get command-line arguments
# ==========================

parser = argparse.ArgumentParser(description='SVS Fire Detection')

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
cfg = config['svs']

url = ref_date.strftime(cfg['url'])
fname = ref_date.strftime(cfg['fluid_file'])

# Read data from remote server
# ============================

data = urlopen(url)
text = data.read().decode('utf-8').replace('\t','')

# Parse input data stream
# =======================

regions = {}
for line in text.split('\n'):
    if not line:
        continue

    line = line.split()
    id = int(line[0][-3:]) - 1
    lat = float(line[1])
    lon = float(line[2])
    long_name = ' '.join(line[3:])

    name = "event-%03d"%(id,)
    regions[name] = {
              'fire_name': long_name,
              'fire_id': 'unknown',
              'fire_center': "{} {}".format(lon, lat),
              'fire_size': 999.0
            }

# Write out event information
# ===========================

region = {'event': regions, 'region': regions}

os.makedirs(os.path.dirname(fname), mode=0o755, exist_ok=True)
with open(fname, 'w') as outfile:
    yaml.dump(region, outfile, default_flow_style=False)
