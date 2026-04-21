#!/bin/sh

TYPES="full:|anom:Anomaly|std:Stdev|diff:Departure from Neutral"
IMAGEDIR="/discover/nobackup/jardizzo/software/GEOS-ESM/WxMap-Config/ENSO_composite/src"

SRC=`dirname $0`
SRC=`realpath $SRC`
stream=$1
field=$2
var=`echo $field | cut -d'_' -f1`
title=`grep "${var}," $SRC/titles | cut -d',' -f2`

stat=`echo $field | cut -d'_' -f2`
type=`echo $TYPES | tr '|' '\n' | grep $stat | cut -d':' -f2`

echo "stream: $stream"
echo "field:  $field"
echo "type: $type"
echo "title: $title"
echo ""
echo -n "Installing..."

mkdir -p $stream/$field
cd $stream/$field

tar xvf $SRC/template.tar

find . -name "*.html" -exec ~jardizzo/bin/sub 'TITLE' "$title" {} \;
find . -name "*.html" -exec ~jardizzo/bin/sub 'FIELD' "$field" {} \;
find . -name "*.html" -exec ~jardizzo/bin/sub 'TYPE' "$type" {} \;
find . -name "*.html" -exec ~jardizzo/bin/sub 'STREAM' "$stream" {} \;

mkdir images
mkdir thumbnails

find $IMAGEDIR/$field -name "*.image.png" -exec cp {} images \;
find $IMAGEDIR/$field -name "*.icon.png" -exec cp {} thumbnails \;

echo "complete"

exit 0
