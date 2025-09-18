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

cat >tt <<EOF
shortwave:

  configs: [$config_path]
  stream: CONUS2KM
  start_dt: P0D
  end_dt: P30DT23H
  t_deltat: PT30M
  options: --fullframe --lights_off --no_title --no_label --no_logo --geometry 4320x2160
  oname: $NOBACKUP/Aerosols_at_Night/images/aerosols_at_night.nasa.gmao.conus2km.analysis.aod.base.4320x2160.%Y-%m-%dT%H:%M:00.png
  levels: [0]
  fields: [aod]
  regions: [global]
EOF
