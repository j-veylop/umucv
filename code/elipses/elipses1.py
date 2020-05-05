#!/usr/bin/env python

# Detección del marcador de 4 círculos
# pruébalo con:

# ./elipses0a.py --dev=dir:*.png


from umucv.stream   import autoStream
import cv2 as cv
import numpy as np
from umucv.contours import extractContours, detectEllipses
from umucv.util import mkParam, putText
from umucv.htrans import htrans, desp, rot3, scale


cv.namedWindow("elipses")
param = mkParam("elipses")
param.addParam("err",30,50)


for key,frame in autoStream():
    g = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    cs = extractContours(g, minarea=5)

    els = detectEllipses(cs, tol=param.err)

    for e in els:            
        cx,cy = int(e[0][0]), int(e[0][1])

        cv.ellipse(frame,e, color=(0,0,255))

        info = '{}'.format(g[cy,cx])
        putText(frame, info, (cx,cy),color=(255,255,255))
    
    if len(els)==4:    
        hull = cv.convexHull(np.array([(e[0][0], e[0][1]) for e in els]).astype(np.float32)).reshape(-1,2)
        #print(hull)
        vals = np.array([ g[int(y), int(x)] for x,y in hull])
        #print(vals) 
        orig = np.where(vals == max(vals))[0][0]
        #print(orig)
        hull = hull[ np.roll(np.arange(4), -orig) ]
        #print(hull)

        cv.polylines(frame, [hull.astype(int)], False, (128,0,0), 1, lineType=cv.LINE_AA)

    cv.imshow('elipses',frame)
