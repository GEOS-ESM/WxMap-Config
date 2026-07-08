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

echo $config_path

wxmap.py --config $config_path \
         --stream CONUS2KM \
         --start_dt $sdate \
         --end_dt $edate \
         --t_deltat 1 \
         --field smoke \
         --region nam \
         --fullframe --lights_off --no_title --no_label --no_logo \
         --geometry 3840x2160 \
         --oname $NOBACKUP/ShortWAVE/wildfires/Y${year}/$catalog_id/images/$catalog_id.nasa.gmao.conus2km.analysis.smoke.image.3840x2160.%Y%m%d%H.png
