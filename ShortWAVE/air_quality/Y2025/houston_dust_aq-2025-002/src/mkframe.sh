#!/bin/sh

app=`realpath $0`
app_path=`dirname $app`
config_path=`dirname $app_path`
catalog_id=`basename $config_path`
year=`echo $catalog_id | cut -d'-' -f2`

#in_dir=$NOBACKUP/ShortWAVE/air_quality/Y${year}/$catalog_id/images
in_dir=/discover/nobackup/dao_ops/jardizzo/ShortWAVE/air_quality/Y2025/houston_dust_aq-2025-002/images
out_dir=$NOBACKUP/ShortWAVE/air_quality/Y${year}/$catalog_id/frames

mkdir -p $out_dir

cd $out_dir
cp -p $app_path/*.py .
cp -p $app_path/*.json .
cp -p $app_path/*cbar* .
mkframe.py $in_dir/*.png

/bin/rm $out_dir/*.py
/bin/rm $out_dir/*.json
/bin/rm $out_dir/*.pyc
/bin/rm $out_dir/*cbar*

echo $out_dir

exit 0
