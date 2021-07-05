import numpy as np

#Calculates the average return of all instrument since day 1 to current(in percentage form)
def averageReturn(prcSoFar):
    total = 0
    (nins,nt) = prcSoFar.shape
    for ins in prcSoFar:
        total += getInstrumentReturn(ins)
    return total/nins

#Calculates the return of an instrument since day 1 to current(in percentage form)
def getInstrumentReturn(ins):
    currPrice = ins[-1]
    startPrice = ins[0]
    ROI = (currPrice - startPrice)/startPrice * 100
    return ROI