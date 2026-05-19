#!/bin/sh

while read field; do

  stats.py --theme custom-2_mission --theme SARP-2026 --stream GEOSCFFC --fcst_dt 20260501T09 --start_dt 20260501T12 --end_dt 20260506 --t_deltat PT3H --field $field --region sarp --layer shading --match %Y:2026 --oname $field.stats

# wxmap.py --theme custom-2_mission --theme SARP-2026 --stream GEOSCFFC --fcst_dt 20260422T09 --start_dt 20260422T12 --end_dt 20260427 --t_deltat PT3H --field $field --region sarp --lights_off --oname '/discover/nobackup/jardizzo/SARP-2026/%%Y%%m%%d_%%H/custom-2/$field/$level/custom-2.GEOS-CF.$field.$level.%Y%m%dT%H.png'

# wxmap.py --theme custom-2_mission --theme SARP-2026 --stream GEOSCFFC --fcst_dt 20260422T09 --time_dt 20260422T12 --t_deltat PT3H --field $field --region sarp --geometry 200x150 --fullframe --lights_off --plot_only --oname '/discover/nobackup/jardizzo/SARP-2026/%%Y%%m%%d_%%H/custom-2/$field/$level/thumb.png'

done

exit 0
