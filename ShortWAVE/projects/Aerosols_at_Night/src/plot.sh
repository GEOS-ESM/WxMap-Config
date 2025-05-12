#!/bin/sh

if [ $# -ne 2 ]; then
  echo "Usage: $0 [sccyymmdd] [eccyymmdd]" 2>&1
  exit 1
fi

sdate=$1
edate=$2

app=`realpath $0`
app_path=`dirname $app`
config_path=`dirname $app_path`
#catalog_id=`basename $config_path`
#year=`echo $catalog_id | cut -d'-' -f2`

wxmap.py --config $config_path \
         --stream CONUS2KM \
         --start_dt $sdate \
         --end_dt $edate \
         --t_deltat 1 \
         --field aod \
         --region global \
         --fullframe --lights_off --no_title --no_label --no_logo \
         --geometry 4320x2160 \
         --oname $NOBACKUP/Aerosols_at_Night/images/aerosols_at_night.nasa.gmao.conus2km.analysis.aod.image.2160p.%Y%m%d%H.png
