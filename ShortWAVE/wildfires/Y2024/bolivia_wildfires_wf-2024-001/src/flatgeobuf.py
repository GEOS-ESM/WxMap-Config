import os
import sys
import argparse
import geopandas as gpd
import datetime as dt

# Get command-line arguments
# ==========================

parser = argparse.ArgumentParser(description='EIS Fire Detection')

parser.add_argument('filename', metavar='filename', type=str,
       help='FlatGeobuf file')
parser.add_argument('outdir', metavar='outdir', type=str,
       help='output directory')

args = parser.parse_args()

start_dt = dt.datetime(2024, 7, 15, 0)
end_dt = dt.datetime(2024, 9, 15, 0)
inchrs = dt.timedelta(hours=12)

df = gpd.read_file(args.filename)
template = os.path.join(args.outdir, '%Y%m%d%p')

os.makedirs(args.outdir, mode=0o755, exist_ok=True) 

time_dt = start_dt
while time_dt <= end_dt:

    ctime = time_dt.strftime("%Y-%m-%dT%H:00:00")
    dfout = df[(df['t'] == ctime)]

    dfout = dfout.to_crs(crs="epsg:4326",epsg=4326)
    dfout = dfout.set_crs("epsg:4326")

    oname = time_dt.strftime(template)
    dfout.to_file(oname)

    time_dt += inchrs
