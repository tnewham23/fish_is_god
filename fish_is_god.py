#!/usr/bin/env python

# RENAME THIS FILE WITH YOUR TEAM NAME.

import numpy as np
import regression as r
import rsi
import trading_functions as tf

nInst=100
currentPos = np.zeros(nInst)
# Checks correlation between instruments based on first 250 days of analysis
corrMatrix = r.corr_mat("./prices250.txt")
counter = 0

def getMyPosition (prcSoFar):
    global currentPos
    global corrMatrix
    global counter
    (nins,nt) = prcSoFar.shape
    # Reset size to try and reduce huge positions which restrict backswing
    counter += 1
    if counter % 50 == 0:
        for index in range(50):
            currentPos[index] *= 0.5

    # increase position by 10000/(price*50) when price decreases, decrease position by 10000/(price*50) when price increases
    for index, ins_ls in enumerate(prcSoFar):
        # Relative Strength Index for 14 days used to signal a trend/movement in volatile stock
        rsi_t = rsi.ins_rsi(ins_ls)
        # If index is less than 50 (or rsi impacted) use moving average algorithm
        if index < 50 or rsi_t > 69 or rsi_t < 31:
            # Calculate small moving average over 10 and 30 days (including from previous day)
            sma10 = rsi.SMA(ins_ls, 10)
            prev_sma10 = rsi.SMA(ins_ls[:-1], 10)
            sma30 = rsi.SMA(ins_ls, 30)
            prev_sma30 = rsi.SMA(ins_ls[:-1], 30)

            # If moving average in upward increasing trend, then buy 
            if (sma10 - sma30) > 0 and abs(sma10 - sma30) > sma10*0.02:
                # Reduce number usually volatile stock in opposite direction (since high rsi)
                if index > 50:
                    currentPos[index] -= (5000/(ins_ls[-1]))
                    continue
                if abs(sma10 - sma30) > abs(prev_sma10 - prev_sma30):
                    # Optimisation to encourage a backwards swing in the case of a large change in price
                    if abs(sma10 - sma30) > sma10*0.04:
                        currentPos[index] += 5000/(ins_ls[-1])

                    # Use correlation matrix to apply trend from this instrument to other similar instruments
                    # Note correlation with itself is equal to 1
                    for i in range(50):
                        currentPos[i] += (5000/(ins_ls[-1])) * (corrMatrix[index][i]**1)*abs(corrMatrix[index][i]**1)
                elif abs(sma10 - sma30) < abs(prev_sma10 - prev_sma30):
                    for i in range(50):
                        currentPos[i] -= (1000/(ins_ls[-1])) * (corrMatrix[index][i]**1)*abs(corrMatrix[index][i]**1)
            # Similar to above but in opposite direction
            elif (sma10 - sma30) < 0 and abs(sma10 - sma30) > sma10*0.02:
                if index > 50:
                    currentPos[index] -= -5000/(ins_ls[-1])
                    continue

                if abs(sma10 - sma30) > abs(prev_sma10 - prev_sma30):

                    if abs(sma10 - sma30) > sma10*0.04:
                        currentPos[index] += -5000/(ins_ls[-1])

                    for i in range(50):
                        currentPos[i] += (-5000/(ins_ls[-1])) * (corrMatrix[index][i]**1)*abs(corrMatrix[index][i]**1) 

                elif abs(sma10 - sma30) < abs(prev_sma10 - prev_sma30):
                    for i in range(50):
                        currentPos[i] -= (-1000/(ins_ls[-1])) * (corrMatrix[index][i]**1)*abs(corrMatrix[index][i]**1) 

        else:
            # Instrument is volatile, use day to day trading assuming the opposite move move is likely to happen
            # If current price is larger than previous price, short instrument
            if ins_ls[-1] > ins_ls[-2]:
                currentPos[index] = (-10000/(ins_ls[-1]))
            else: # Price decreased (or remained same), take long position
                currentPos[index] = (10000/(ins_ls[-1]))

    # The algorithm must return a vector of integers, indicating the position of each stock.
    # Position = number of shares, and can be positve or negative depending on long/short position.
    return currentPos

    
