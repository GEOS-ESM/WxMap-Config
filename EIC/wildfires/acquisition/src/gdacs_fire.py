#! /usr/bin/env python

import sys
import yaml
import geopandas as gpd
import datetime as dt
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
from gdacs.api import GDACSAPIReader

client = GDACSAPIReader()

#events = client.latest_events()
wf_events = client.latest_events(event_type="WF")

print(wf_events)
