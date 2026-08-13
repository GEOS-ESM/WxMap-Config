#!/bin/sh

while read var; do

  wxmap.py --theme chem2d_mission --theme SABRE --stream G5FPFC --fcst_dt 20260808 --time_dt 20260810 --field $var --region sabre --oname '$field.$level.png'

done

exit 0
