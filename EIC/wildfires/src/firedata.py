import os
import sys
import yaml
import json
import datetime as dt

from wxutils.utils import make_dirs
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim

class FireData(object):

    def __init__(self, radius=0.25, filter=None, bbox=None):

        self.radius = radius
        self.filter = filter
        self.bbox = bbox
        self.loninc = radius
        self.latinc = radius
        self.nlon = 360.0 / self.loninc + 1
        self.nlat = 180.0 / self.latinc + 1
        self.records = {}
        self.address = {}

        if not filter:
            self.filter = ['us', 'ca']

        if not bbox:
            self.bbox = [0.25,0.25,7.0,3.5]

    def update(self, record):

        lon = record['lon']
        lat = record['lat']

        if lon >= 180.0:
            lon -= 360.0
        i = int(round((lon + 180.0) / self.loninc))
        j = int(round((lat + 90.0) / self.latinc))
        k = i + j*self.nlon

        entry = self.records.get(k, None)

        if not entry or record > entry:
            self.records[k] = record

    def geolocate(self):

        geolocator = Nominatim(user_agent="eic_fire")

        for k,record in self.records.items():

            lon = record['lon']
            lat = record['lat']

            coord = str(lat) + ' ' + str(lon)
            location = geolocator.reverse(coord, language='en')
            address = location.raw['address']

            self.address[k] = address

    def sort(self, key, maxrec=None):

        if not maxrec:
            maxrec = len(self.records.keys())

        rec = []
        for k,record in self.records.items():
            rec.append((k, record[key]))

        rec.sort(reverse=True,key=self.sorter)

        records = {}
        for r in rec[0:min(maxrec,len(rec))]:
            k = r[0]
            records[k] = self.records[k]

        self.records = records

    def sorter(self, rec):
        return rec[1]

    def write(self, fname, filter=None, bbox=None):

        n = 0
        regions = {}

        if not bbox:
            bbox = self.bbox

        if not filter:
            filter = self.filter

        for k,record in self.records.items():

            lon = record['lon']
            lat = record['lat']
            farea = record.get('farea', 0.0)

            rlon = round(lon*100)/100.0
            rlat = round(lat*100)/100.0
            coord = str(lat) + ' ' + str(lon)

            address = self.address.get(k, None)

            if address:
                code = address.get('country_code', None)

                if not code:
                    continue

                if filter and code not in filter:
                    continue      

                county = address.get('county', '')
                state = address.get('state', '')
                addr = county + ', ' + state
            else:
                addr = record.get('fname', '')

            lat1 = rlat - bbox[1]
            lon1 = rlon - bbox[0]

            lat2 = rlat + bbox[1]
            lon2 = rlon + bbox[0]

            LAT1 = rlat - bbox[3]
            LON1 = rlon - bbox[2]

            LAT2 = rlat + bbox[3]
            LON2 = rlon + bbox[2]

            if lon1 < -180.0:
                lon1 += 360.0
                lon2 = lon1 + bbox[0]*2

            if lon2 > 360.0:
                lon2 -= 360.0
                lon1 = lon2 - bbox[0]*2

            if LON1 < -180.0:
                LON1 += 360.0
                LON2 = LON1 + bbox[2]*2

            if LON2 > 360.0:
                LON2 -= 360.0
                LON1 = LON2 - bbox[2]*2

            name = "region-%03d"%(n,)
            regions[name] = {
                      'long_name': name,
                      'lat': "{} {}".format(LAT1, LAT2),
                      'lon': "{} {}".format(LON1, LON2),
                      'mpdset': 'hires',
                      'mpvals': '',
                      'frame': 'off',
                      'place': ["{} {} {}".format(lon1, lat1-0.02, addr)],
                      'area': ["{} {} {} {}".format(lon1,lat1,lon2,lat2)],
                      'fire_marker': ["{} {}".format(rlon, rlat)],
                      'fire_size': float(farea)
                    }

            n += 1

        region = {'region': regions}

        make_dirs(os.path.dirname(fname))
        with open(fname, 'w') as outfile:
            yaml.dump(region, outfile, default_flow_style=False)

    def writeJSON(self, fname, filter=None, bbox=None):

        locations = []
        for k,record in self.records.items():

            lon = record['lon']
            lat = record['lat']

            rlon = round(lon*100)/100.0
            rlat = round(lat*100)/100.0
            coord = str(lon) + ' ' + str(lat)
            locations.append(coord)

        make_dirs(os.path.dirname(fname))
        with open(fname, 'w') as outfile:
            json.dump(locations,outfile)

class FireRecord(dict):

    def __init__(self, dct=None):

        if not dct:
            dct = {}

        super().__init__(dct)

    def __gt__(self, other):

        if self['duration'] > other['duration']:
            return True

        if self['farea'] > other['farea']:
            return True

        if self['frp'] > other['frp']:
            return True

        return False
