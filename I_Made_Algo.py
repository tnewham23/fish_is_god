#!/usr/bin/env python

# RENAME THIS FILE WITH YOUR TEAM NAME.

import numpy as np
import trading_functions as tf
import plotting as pt
import rsi

nInst=100
currentPos = np.zeros(nInst)
RecentlyBought = np.zeros(nInst)
sellPrice = np.zeros(nInst)
stopLoss = np.zeros(nInst)
totalIns = 0


# QUESTION: do we know our previous position (this assumes that we do)
def getMyPosition (prcSoFar):
    global currentPos
    global RecentlyBought
    global sellPrice
    global stopLoss
    global totalIns
    (nins,nt) = prcSoFar.shape

    count = 0
    weight = 0
    maxWeight = 0.4
    rb = np.zeros(100)
    newPos = []
    
    for ins in prcSoFar:
        if currentPos[count] > 0:
            if ins[-1] < stopLoss[count]:
                currentPos[count] = 0
                totalIns -= 1 
                stopLoss[count] = 0
                sellPrice[count] = 0
            elif ins[-1] > sellPrice[count]:
                if rsi.ins_rsi(ins) > 50 and pt.SMA(ins, 10)[count] <= pt.SMA(ins, 30)[count] and ins[-1] < ins[-2]:
                    currentPos[count] = 0     
                    stopLoss[count] = 0
                    sellPrice[count] = 0 
                    totalIns -= 1            

        elif pt.SMA(ins, 10)[count] - pt.SMA(ins, 30)[count] > 0 and rsi.ins_rsi(ins) < 40:
            weight += 0.15
            if pt.ATR(ins, 7)[count] - 2.5 > 0:
                weight += 0.2
            elif RecentlyBought[count] > 0:
                weight = 0
                continue
            if tf.getInstrumentReturn(ins) < tf.averageReturn(prcSoFar):
                weight -= 0.2
            currentPos[count] = 10000*weight
            RecentlyBought[count] = 5
            totalIns += 1
            weight = 0
            stopLoss[count] = ins[-1] - 1/pt.ATR(ins, 14)[count] * 1/100 * ins[-1]
            sellPrice[count] = ins[-1] + 1/pt.ATR(ins, 7)[count] * 1/100 * ins[-1]     
        
        if RecentlyBought[count] > 0:
            RecentlyBought[count] -= 1
        count += 1        

    return currentPos