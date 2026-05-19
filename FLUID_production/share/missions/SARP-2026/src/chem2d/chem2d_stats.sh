#!/bin/sh

while read field; do

  stats.py --theme chem2d_mission --theme SARP-2026 --stream G5FPFC --fcst_dt 20260514 --start_dt 20260514T06 --end_dt 20260523T18 --t_deltat PT3H --field $field --region sarp --layer shading --match %Y:2026 --oname $field.stats

done

exit 0
