#!/bin/sh

stat=$1
files=`find *_${stat} -name "*.pacific.013.icon.png"`

for file in $files; do
    name=`basename $file`
    nodes=`echo $name | cut -d'.' -f1-2`
    name=$nodes.png
    cp $file thumbnails/$name
done

exit 0
