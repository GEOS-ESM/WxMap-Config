import os
import sys
import json
import ruamel.yaml as yaml
import datetime as dt

from wxutils.utils import make_dirs
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
from ruamel.yaml.scalarstring import SingleQuotedScalarString

class FireData(object):

    def __init__(self, radius=0.25, filter=None):

        self.radius = radius
        self.filter = filter
        self.loninc = radius
        self.latinc = radius
        self.nlon = 360.0 / self.loninc + 1
        self.nlat = 180.0 / self.latinc + 1
        self.records = {}
        self.address = {}

        if not filter:
            self.filter = ['us', 'ca']

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

    def write(self, fname, filter=None):

        n = 0
        regions = {}

        if not filter:
            filter = self.filter

        for k,record in self.records.items():

            id = record.get('id', 'missing')
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

            name = "event-%03d"%(n,)
            regions[name] = {
                      'fire_name': addr,
                      'fire_id': id,
                      'fire_center': "{} {}".format(rlon, rlat),
                      'fire_size': float(farea)
                    }

            n += 1

        region = {'event': regions, 'region': regions}

        make_dirs(os.path.dirname(fname))
        with open(fname, 'w') as outfile:
            yaml.dump(region, outfile, default_flow_style=False)

    def writeJSON(self, fname, filter=None):

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
