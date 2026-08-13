#!/bin/sh

while read field; do

  stats.py --theme custom-2_mission --theme SABRE --stream GEOSCFFC --fcst_dt 20260810T09 --start_dt 20260810T12 --end_dt 20260815 --t_deltat PT3H --field $field --region sabre --layer shading --match %Y:2026 --oname $field.stats

done

exit 0
