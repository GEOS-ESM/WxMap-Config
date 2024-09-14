#!/bin/sh

app=`realpath $0`
app_path=`dirname $app`
config_path=`dirname $app_path`
catalog_id=`basename $config_path`
year=`echo $catalog_id | cut -d'-' -f2`

out_dir=$NOBACKUP/ShortWAVE/severe_weather/Y${year}/$catalog_id/images

mkdir -p $out_dir

cd $out_dir
cp -p $app_path/*.py .
cp -p $app_path/*cbar* .
cp -p $app_path/list* .
mkimage.py `cat list1` &
mkimage.py `cat list2` &
mkimage.py `cat list3` &
mkimage.py `cat list4` &

sleep 10000000

/bin/rm $out_dir/*.py
/bin/rm $out_dir/*.pyc
/bin/rm $out_dir/*cbar*

echo $out_dir

exit 0
