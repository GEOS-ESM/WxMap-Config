#! /usr/bin/env python

import json

gram_file = '/home/aconaty/data-services/gram/menus/5_active_campaigns/WHYMSIE.csv'
gram_template = 'https://fluid.nccs.nasa.gov/gram/total/{}x{}/'

# Read in Datagrams CSV file

with open(gram_file, 'r') as f:
    lines = f.readlines()


# Extract CSV stations and assign URLs for buoys and other.

stations = []
buoys = []
ships = []

for line in lines[1:]:

    name, lon, lat = line.strip().split(',')
    lon = lon.strip('0')
    lat = lat.strip('0')
    if lon[-1] == '.':
        lon += '0'
    if lat[-1] == '.':
        lat += '0'
    url = gram_template.format(lat, lon)

    location = ' '.join([lon, lat, name, url])

    if 'SIMB3' in name:
        buoys.append(location)
    elif 'SHIP' in name:
        ships.append(location)
    else:
        stations.append(location)

# Write out buoys to JSON file.

oname = '/discover/nobackup/projects/gmao/merra2/data/pub/supplemental/ARCSIX/buoy.json'
with open(oname, 'w') as f:
    json.dump(buoys, f)

# Write out ships to JSON file.

oname = '/discover/nobackup/projects/gmao/merra2/data/pub/supplemental/ARCSIX/ship.json'
with open(oname, 'w') as f:
    json.dump(ships, f)

# Write out stations to JSON file.

oname = '/discover/nobackup/projects/gmao/merra2/data/pub/supplemental/ARCSIX/station.json'
with open(oname, 'w') as f:
    json.dump(stations, f)
