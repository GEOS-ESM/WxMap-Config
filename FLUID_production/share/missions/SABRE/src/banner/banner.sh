#!/bin/sh

var=$1
level=$2

wxmap.py --theme chem3d_mission --theme SABRE --stream G5FPFC --fcst_dt 20260811 --time_dt 20260812 --field $var --level $level --region banner --oname 'banner.png' --config ./banner.yml --geometry 1820x342 --lights_off --fullframe --plot_only

exit 0
