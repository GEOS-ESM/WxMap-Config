import sys
import json

with open(sys.argv[1], 'r') as f:
    stations = json.load(f)

print('<map name="stations">')
for station in stations:

    x = station['x']
    y = station['y']
    r = station['r']
    name = station['hover']
    url = station['url']

    print(f'  <area shape="circle" coords="{x},{y},{r}" alt="{name}" title="{name}" href="{url}">')

print('</map>')
