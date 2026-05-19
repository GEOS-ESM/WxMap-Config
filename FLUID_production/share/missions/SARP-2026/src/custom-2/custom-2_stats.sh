#!/bin/sh

while read field; do

  stats.py --theme custom-2_mission --theme SARP-2026 --stream GEOSCFFC --fcst_dt 20260515T09 --start_dt 20260515T12 --end_dt 20260520 --t_deltat PT3H --field $field --region sarp --layer shading --match %Y:2026 --oname $field.stats

done

exit 0
