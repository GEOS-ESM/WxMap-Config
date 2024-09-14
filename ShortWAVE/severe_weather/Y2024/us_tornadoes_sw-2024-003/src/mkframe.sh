#!/bin/sh

app=`realpath $0`
app_path=`dirname $app`
config_path=`dirname $app_path`
catalog_id=`basename $config_path`
year=`echo $catalog_id | cut -d'-' -f2`

in_dir=$NOBACKUP/ShortWAVE/severe_weather/Y${year}/$catalog_id/images
out_dir=$NOBACKUP/ShortWAVE/severe_weather/Y${year}/$catalog_id/frames

mkdir -p $out_dir

cd $out_dir
cp -p $app_path/*.py .
cp -p $app_path/*cbar* .
cp -p $app_path/list* .
mkframe.py `cat list1` &
mkframe.py `cat list2` &
mkframe.py `cat list3` &
mkframe.py `cat list4` &

sleep 10000000

/bin/rm $out_dir/*.py
/bin/rm $out_dir/*.pyc
/bin/rm $out_dir/*cbar*

echo $out_dir

exit 0
