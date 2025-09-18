#! /usr/bin/env python

import sys
import math
import numpy as np
from clevs import *

def refine_clevs_log1(clevs, nsub, type):

    clevs_f = []
    clevs = [ float(clev) for clev in clevs.split() if clev != ' ' ]
        
    for index, clev in enumerate(clevs[0:-1]):
            
        dclev = ( math.log(clevs[index+1]) - math.log(clev) ) / nsub
        clevs_f.append(str(clev))
                
        for ns in range(2,nsub+1):
            clev_f = math.log(clev) + (ns-1) * dclev
            clev_f = math.exp(clev_f)
            clev_f = f"{clev_f:.10f}".rstrip('0')
            clevs_f.append(clev_f)
                
    clevs_f.append(str(clevs[-1]))
    return clevs_f

def refine_clevs_old(clevs, nsub, type):
    
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

if len(sys.argv) <= 3:
    clevs = sys.argv[1]
    nsub = int(sys.argv[2])
else:
    clevs = set_clevs(sys.argv[1], sys.argv[2], sys.argv[3])
    nsub = int(sys.argv[4])

#clevs_refined = refine_clevs_old(clevs, nsub, '')
clevs_refined_new = refine_clevs(clevs, nsub, 'log')
clevs_refined_log1 = refine_clevs_log1(clevs, nsub, '')

print(clevs_refined_new)
print('--------')
print(clevs_refined_log1)
