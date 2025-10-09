#! /usr/bin/env python

import os
import sys
import argparse

parser = argparse.ArgumentParser(description='DDF File Freeze')

parser.add_argument(
        '-o', '--odir', metavar='OUTDIR', type=str, required=True,
        help='output directory'
)
parser.add_argument(
        '-f', '--files', nargs='+', help='file(s)', required=True
)

args = parser.parse_args()

files = args.files
os.makedirs(args.odir, mode=0o755, exist_ok=True)

for file in args.files:

    print(file)

    with open(file, 'r') as f:
        lines = f.readlines()

    tdim = ''
    newlines = []
    for line in lines:
        if 'tdef' in line[0:5].lower():
            nodes = line.split()
            if len(nodes) > 2:
                tdim = nodes[1]
                nodes[1] = '500000'
                line = ' '.join(nodes) + '\n'
        newlines.append(line)

    for i, line in enumerate(newlines):
        if 'chsub' in line.lower():
            nodes = line.split()
            if nodes[2] == tdim:
                nodes[2] = '500000'
            newlines[i] = ' '.join(nodes) + '\n'

    bname = os.path.basename(file)
    oname = os.path.join(args.odir, bname)

    with open(oname, 'w') as f:
        f.writelines(newlines)

sys.exit(0)
