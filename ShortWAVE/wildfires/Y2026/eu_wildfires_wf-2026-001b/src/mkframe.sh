#!/bin/sh

app=`realpath $0`
app_path=`dirname $app`
config_path=`dirname $app_path`
catalog_id=`basename $config_path`
year=`echo $catalog_id | cut -d'-' -f2`

in_dir=$NOBACKUP/ShortWAVE/wildfires/Y${year}/$catalog_id/images
out_dir=$NOBACKUP/ShortWAVE/wildfires/Y${year}/$catalog_id/frames

mkdir -p $out_dir
mkframe_nolabel.py $out_dir $in_dir/$1

echo $out_dir

exit 0
