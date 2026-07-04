#!/bin/sh

stream=$1
field=$2
title=$3

more << EOF
<tr>
<td align="left" valign="center">
<p style="font-size:24px;">&emsp;$title</p>
</td>
<td align="center" valign="center">
<a href="https://portal.nccs.nasa.gov/datashare/gmao/geos-fp/.internal/MERRA-2/ENSO_Composite/$stream/${field}_full"> <img src="thumbnails/$stream.${field}_full.icon.png" class="ImageBorder" /> </a>
</td>
<td align="center" valign="center">
<a href="https://portal.nccs.nasa.gov/datashare/gmao/geos-fp/.internal/MERRA-2/ENSO_Composite/$stream/${field}_anom"> <img src="thumbnails/$stream.${field}_anom.icon.png" class="ImageBorder" /> </a>
</td>
<td align="center" valign="center">
<a href="https://portal.nccs.nasa.gov/datashare/gmao/geos-fp/.internal/MERRA-2/ENSO_Composite/$stream/${field}_std"> <img src="thumbnails/$stream.${field}_std.icon.png" class="ImageBorder" /> </a>
</td>
<td align="center" valign="center">
<a href="https://portal.nccs.nasa.gov/datashare/gmao/geos-fp/.internal/MERRA-2/ENSO_Composite/$stream/${field}_diff"> <img src="thumbnails/$stream.${field}_diff.icon.png" class="ImageBorder" /> </a>
</td>
</tr>
EOF
