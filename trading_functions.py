import numpy as np

#Calculates the average return of all instrument since day 1 to current(in percentage form)
def averageReturn(prcSoFar):
    total = 0
    (nins,nt) = prcSoFar.shape
    for ins in prcSoFar:
        total += getInstrumentReturn(ins)
    return total/nins

#Gives the maximum and minumum returns for the instruments from day 1 to current day.
def MinMaxReturn(prcSoFar):
    minR = getInstrumentReturn(prcSoFar[0])
    minIndex = 0
    maxR = getInstrumentReturn(prcSoFar[0])
    maxIndex = 0
    count = 0
    for ins in prcSoFar:
        currentReturn = getInstrumentReturn(ins)
        if (currentReturn < minR):
            minR = currentReturn
            minIndex = count
        if (currentReturn > maxR):
            maxR = currentReturn  
            maxIndex = count
        count += 1  
    return (minR, minIndex, maxR, maxIndex)


#Gives the range of returns (with absolute value):
def rangeOfReturn(prcSoFar):
    minR = abs(getInstrumentReturn(prcSoFar[0]))
    minIndex = 0
    maxR = abs(getInstrumentReturn(prcSoFar[0]))
    maxIndex = 0
    count = 0
    for ins in prcSoFar:
        currentReturn = abs(getInstrumentReturn(ins))
        if (currentReturn < minR):
            minR = currentReturn
            minIndex = count
        if (currentReturn > maxR):
            maxR = currentReturn  
            maxIndex = count
        count += 1  
    return (minR, minIndex, maxR, maxIndex)

#Calculates the return of an instrument since day 1 to current(in percentage form) (assumes long position)
def getInstrumentReturn(ins):
    currPrice = ins[-1]
    startPrice = ins[0]
    ROI = (currPrice - startPrice)/startPrice * 100
    return ROI

#Calculates the average price of an instrument up to the current day
def averagePrice(ins):
    return ins.mean()

#Calculates the average of the relative SD of all instruments since day1 to current
def averageRSD(prcSoFar):
    total = 0
    (nins,nt) = prcSoFar.shape
    for ins in prcSoFar:
        total += relativeSD(ins)
    return total/nins

#Calculates SD as a proportion of the mean 
def relativeSD(ins):
    return ins.std()/ins.mean() * 100