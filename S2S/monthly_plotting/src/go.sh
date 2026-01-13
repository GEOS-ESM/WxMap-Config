#!/bin/sh

stream=$1
field=$2
region=$3

config_base=/discover/nobackup/jardizzo/software/GEOS-ESM/WxMap-Config/S2S/monthly_plotting
config_stream=/discover/nobackup/jardizzo/software/GEOS-ESM/WxMap-Config/S2S/monthly_plotting/$stream

wxmap.py --config $config_base --config $config_stream --stream $stream --fcst_dt 20250801 --time_dt 20250801 --field $field --region $region --oname '$stream.ensmean_%%Y^%%b_${field}_fcst_$region.png'

