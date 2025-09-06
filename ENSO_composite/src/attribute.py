import sys
import ruamel.yaml as yaml

file=sys.argv[1]
ofile=sys.argv[2]

with open(file, 'r') as f:
    cfg = yaml.safe_load(f)

attributes = cfg['theme']['attribute']

for var, cdict in attributes.items():
    for entry in cdict:
        cmax = entry['cmax'] / 2.0
        x = int(round(cmax / 5.0))
        if x > 0:
            cmax = x * 5
        cint = (cmax * 2) / 10.0
        cmin = -cmax
        entry['cmax'] = cmax
        entry['cmin'] = cmin
        entry['cint'] = cint

with open(ofile, 'w') as f:
  # yaml.dump(cfg, f, default_flow_style=False)
    yaml.dump(cfg, f)

