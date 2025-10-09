#! /usr/bin/env python

import yaml
import html
import geopandas as gpd
from urllib.request import urlopen
from owslib.ogcapi.features import Features

from wxutils.utils import *

def get_eis(start_dt, end_dt, **kwargs):


    url = kwargs['url']
    min_area = kwargs.get('min_area', 75)
    min_duration = kwargs.get('min_duration', 2)
    collection = kwargs.get('collection', 'public.eis_fire_lf_perimeter_nrt')
    bbox = kwargs.get('bbox', ['-175.0', '20.0', '-60.0', '70.0'])
    limit = kwargs.get('limit', 9999)
    
    start_date = start_dt.strftime("%Y-%m-%dT%H:%M:%S+00:00")
    end_date = end_dt.strftime("%Y-%m-%dT%H:%M:%S+00:00")
    filter = "farea>{} AND duration>{}".format(min_area, min_duration)

    w = Features(url=url)
    
    print(start_date, end_date)
    perm_results = w.collection_items(
        collection,  # name of the dataset we want
        datetime=[start_date + "/" + end_date],  # date range
        limit=limit,  # max number of items returned
        bbox = bbox
    #   filter=filter   # additional filters based on queryable fields
    )

    df = gpd.GeoDataFrame.from_features(perm_results["features"])

    return df

#------------------------------------------------------------------------------


def get_eonet(start_dt, end_dt, **kwargs):

    url = kwargs['url']

    sdate = start_dt.strftime("%Y-%m-%d")
    edate = end_dt.strftime("%Y-%m-%d")

    url += '&start=$sdate&end=$edate'
    target_url = str_replace(url, sdate=sdate, edate=edate)
    data = urlopen(target_url)

    text = data.read().decode('utf-8').replace('\t','')
    text = html.unescape(text)
    buf = yaml.safe_load(text)

    df = gpd.GeoDataFrame.from_features(buf)

    return df
