#! /usr/bin/env python

import os
import sys
import copy
import math
import gridstat as gstat
import wxservice
import interface
import gradsdataservice as dataservice
import gradsmapservice as mapservice

from request import *

def set_alpha(cmin, cmax):

    alpha = []

    if cmin > 0.0:
        alpha.append("0.000 0.000 0.000")
        alpha.append("0.200 0.000 0.000")
        alpha.append("0.400 1.000 1.000")
        alpha.append("1.000 1.000 1.000")
        return alpha

    if cmax < 0.0:
        alpha.append("0.000 1.000 1.000")
        alpha.append("0.600 1.000 1.000")
        alpha.append("0.800 0.000 0.000")
        alpha.append("1.000 0.000 0.000")
        return alpha
    
    r = (0.0 - cmin) / (cmax - cmin)
    r1 = r - 0.2
    r2 = r + 0.2

    if r1 < 0.0:
        adj = -r1
        r1 += adj
        r  += adj
        r2 += adj

    if r2 > 1.0:
        adj = r2 - 1.0
        r1 -= adj
        r  -= adj
        r2 -= adj

    if r1 == 0.0:
        alpha.append("0.000 0.000 0.000")
    else:
        alpha.append("0.000 1.000 1.000")
        alpha.append("%0.3f 1.000 1.000"%(r1,))

    alpha.append("%0.3f 0.000 0.000"%(r,))

    if r2 == 1.0:
        alpha.append("1.000 1.000 1.000")
    else:
        alpha.append("%0.3f 1.000 1.000"%(r2,))
        alpha.append("1.000 1.000 1.000")

    return alpha

request = Request(interface.parse_args(sys.argv[1:]))

wx = wxservice.WXService(request)

ds = dataservice.Service()
ms = mapservice.Service()

wx.register(dataservice = ds)
wx.register(mapservice  = ms)

playlist = wx.playlist()
template = request['match'].split(':')
layer    = request['layer']

tab4=4*' '
tab6=6*' '
tab8=8*' '

with open('tt.out', 'a') as f:

    for play in playlist:
        
        for request in play:
        
            for r in request:
        
                t = r['time_dt']
                keyval = template
                token  = t.strftime(keyval[0])
                values = keyval[1].split(',')
        
                plot   = wx.get_plot(r)[-1]
                layers = plot.get_layer_stack('layer_names')
                layer  = layers[2]
                index = 2
    
                f.write(tab4+r['field']+':\n')
                f.write(tab6+layer+':\n')
                f.write(tab8+'cdict: '+r['field']+'cdict:\n')
