#!/bin/sh

source /usr/share/lmod/lmod/init/bash
module load python/GEOSpyD/Min23.5.2-0_py3.11
export PYTHONPATH=/discover/nobackup/jardizzo/software/lib/python3.11/site-packages

python flatgeobuf.py /discover/nobackup/jardizzo/lf_perimeter.fgb $NOBACKUP/maps/tmp
