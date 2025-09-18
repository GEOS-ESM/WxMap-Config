#! /usr/bin/env python

import sys
import numpy as np

FLOAT_FORMAT = lambda x: np.format_float_positional(x, precision=10, trim='-')

number = -15.000000012423450000005
print(FLOAT_FORMAT(number))
print(f"{number:.10f}".rstrip('0'))

number = 0.1
print(FLOAT_FORMAT(number))
print(f"{number:.10f}".rstrip('0'))
