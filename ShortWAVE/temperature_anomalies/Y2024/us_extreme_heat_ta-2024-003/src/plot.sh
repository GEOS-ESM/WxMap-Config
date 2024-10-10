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
catalog_id=`basename $config_path`
year=`echo $catalog_id | cut -d'-' -f2`

wxmap.py --config $config_path \
         --stream GEOSANA \
         --start_dt $sdate \
         --end_dt ${edate}T21 \
         --t_deltat 3 \
         --field epv \
         --level 200 \
         --region nam-hwl \
         --fullframe --lights_off --no_title --no_label --no_logo \
         --geometry 3840x2160 \
         --oname $NOBACKUP/ShortWAVE/temperature_anomalies/Y${year}/$catalog_id/images/$catalog_id.nasa.gmao.geos-fp.analysis.epv.image.2160p.%Y%m%d%H.png
