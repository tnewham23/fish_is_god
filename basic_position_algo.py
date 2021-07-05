#!/usr/bin/env python

# RENAME THIS FILE WITH YOUR TEAM NAME.

import numpy as np

nInst=100
currentPos = np.zeros(nInst)


# QUESTION: do we know our previous position (this assumes that we do)
def getMyPosition (prcSoFar):
    global currentPos
    (nins,nt) = prcSoFar.shape

    # increase position by 10000/(price*50) when price decreases, decrease position by 10000/(price*50) when price increases
    rpos_ls = []
    for ins_ls in prcSoFar:
        if ins_ls[-1] == ins_ls[-2]:
            rpos_ls.append(0)
        elif ins_ls[-1] > ins_ls[-2]:
            rpos_ls.append(-10000/(ins_ls[-1]*50))
        else:
            rpos_ls.append(10000/(ins_ls[-1]*50))
    rpos = np.array(rpos_ls)
    currentPos += rpos

    # The algorithm must return a vector of integers, indicating the position of each stock.
    # Position = number of shares, and can be positve or negative depending on long/short position.
    return currentPos
