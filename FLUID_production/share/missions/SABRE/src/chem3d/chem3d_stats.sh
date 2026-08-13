#!/bin/sh

while read field; do

  stats.py --theme chem3d_mission --theme SABRE --stream G5FPFC --fcst_dt 20260811 --start_dt 20260811 --end_dt 20260816 --t_deltat PT3H --field $field --region sabre --layer shading --match %Y:2026 --oname $field.stats

done

exit 0
