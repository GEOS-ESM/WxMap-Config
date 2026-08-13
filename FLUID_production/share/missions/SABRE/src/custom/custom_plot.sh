#!/bin/sh

while read var; do

  wxmap.py --theme custom_mission --theme SABRE --stream G5FPFC --fcst_dt 20260810 --time_dt 20260811 --field $var --region sabre --oname '$field.$level.png'

done

exit 0
