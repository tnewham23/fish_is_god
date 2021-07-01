#!/usr/bin/env python

import numpy as np

nInst=100
currentPos = np.zeros(nInst)

def getMyPosition (prcSoFar):
    global currentPos
    (nins,nt) = prcSoFar.shape
    rpos = np.array([int(x) for x in 1000 * np.random.randn(nins)])
    currentPos += rpos
    return currentPos

    
