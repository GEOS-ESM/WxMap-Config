#! /usr/bin/env python

import sys
import math
import numpy as np

FORMAT = lambda x: np.format_float_positional(x, precision=10, trim='-')

def format_float(num):
  """Formats a float to keep only two non-zero digits after the decimal point."""
# s = str(float(num))
  s = '{:.20f}'.format(num)
  if 'e' in s:
    return s  # Avoid issues with scientific notation
  if '.' not in s:
    return s
  integer_part, decimal_part = s.split('.')
  first_two_nonzero = ''.join(filter(str.isdigit, decimal_part))[:2]
  if not first_two_nonzero:
      return integer_part
  return f"{integer_part}.{first_two_nonzero}"

def myround(n):
    if n == 0:
        return 0
    sgn = -1 if n < 0 else 1
    scale = int(-math.floor(math.log10(abs(n))))
    if scale <= 0:
        scale = 5
    factor = 10**scale
    return sgn*math.floor(abs(n)*factor)/factor

def keep_non_zero_decimals(number):
    number_string = '{:.20f}'.format(number)
    print(number_string)
    if '.' not in number_string:
        return number_string
    integer_part, decimal_part = number_string.split('.')
    non_zero_decimal = decimal_part.rstrip('0')
    if non_zero_decimal:
      return f"{integer_part}.{non_zero_decimal}"
    return integer_part

def set_clevs(cmin, cmax, cint):
    """"""      
    if cmin is None: return 
    if cmax is None: return
    if cint is None: return

    vmin = float(cmin)
    vmax = float(cmax)
    vint = float(cint)

    v    = vmin
    cout = []

    for v in np.arange(vmin, vmax+vint/2.0, vint):
        cout.append(f"{v:.10f}".rstrip('0'))
        v += vint
        
    return ' '.join(cout)

def refine_clevs(clevs, nsub, type):
    
    clevs_f = []
    clevs = [ float(clev) for clev in clevs.split() if clev != ' ' ]

    for index, clev in enumerate(clevs[0:-1]):

        dclev = ( clevs[index+1] - clev ) / float(str(nsub))
        clevs_f.append(f"{clev:.10f}".rstrip('0'))

        for ns in range(2,nsub+1):
            clev_f = clev + float(str((ns-1))) * dclev
            clevs_f.append(f"{clev_f:.10f}".rstrip('0'))

    clevs_f.append(f"{clevs[-1]:.10f}".rstrip('0'))

    return ' '.join(clevs_f)

def refine_clevs_new(clevs, nsub, type):

    clevs_f = []
    levels = []
    clevs = [float(clev) for clev in clevs.split() if clev != ' ']

    for index, clev in enumerate(clevs[0:-1]):
        levels = np.linspace(clev, clevs[index+1], nsub+1, dtype=float)
      # clevs_f += [f"{level:.10f}".rstrip('0') for level in levels[0:-1]]
        clevs_f += [FORMAT(level) for level in levels[0:-1]]

    clevs_f.append(FORMAT(levels[-1]))

    return ' '.join(clevs_f)

#levels = np.linspace(0.0, 1.0, 200, dtype=float)

if len(sys.argv) <= 2:
    clevs = sys.argv[1]
else:
    clevs = set_clevs(sys.argv[1], sys.argv[2], sys.argv[3])

clevs_refined = refine_clevs(clevs, 20, '')
clevs_refined_new = refine_clevs_new(clevs, 20, '')

print(clevs_refined)
print('--------')
print(clevs_refined_new)
#clevs2 = np.linspace(0.0, 1.0, 101, dtype=float, retstep=True)
#print(clevs2)
