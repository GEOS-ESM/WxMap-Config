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

wxmap.py --config $config_path \
         --stream MiCASA \
         --start_dt $sdate \
         --end_dt ${edate}T21 \
         --t_deltat 1 \
         --field MCNPP \
         --fullframe --lights_off --no_title --no_label --no_logo \
         --geometry 3840x2160 \
         --oname $NOBACKUP/GHGCenter/MiCASA/$catalog_id/images/$catalog_id.nasa.gmao.MiCASA.analysis.NEE.image.2160p.%Y%m%d%H.png
