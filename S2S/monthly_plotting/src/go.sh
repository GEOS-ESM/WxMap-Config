#!/bin/sh

cwd=`pwd`
config_path=`dirname $cwd`

wxmap.py --config $config_path --stream S2SENS --fcst_dt 20250101 --time_dt 20250201 --field totexttau_anom --region glb --oname '$field.$region.png'
