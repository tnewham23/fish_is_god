import plotting
import numpy as np
import pandas as pd

from basic_position_algo import getMyPosition as getPosition

# copied from eval.py
def loadPrices(fn):
    global nt, nInst
    df=pd.read_csv(fn, sep='\s+', header=None, index_col=None)
    nt, nInst = df.values.shape
    return (df.values).T


# modified from eval.py
def algo_performance(prcHist, numDays):
    #2d arrays to store cash, positions for each unit 
    # (days * stocks)
    cash = np.zeros((nt + 1, nInst)) 
    position = np.zeros((nt + 1, nInst)) #2d array to store daily positions
    totDVolume = 0
    value = 0
    todayPLL = []
    # (_,nt) = prcHist.shape

    for t in range(nt + 1 - numDays,nt + 1):
        prcHistSoFar = prcHist[:,:t]
        
        # get and correct positions
        newPosOrig = getPosition(prcHistSoFar)
        curPrices = prcHistSoFar[:,-1] 
        posLimits = np.array([int(x) for x in dlrPosLimit / curPrices])
        newPos = np.array([int(p) for p in np.clip(newPosOrig, -posLimits, posLimits)])

        # calculate change in position
        deltaPos = newPos - position[t - 1]
        
        # update position
        position[t] = np.array(newPos)
        
        dvolumes = curPrices * np.abs(deltaPos)
        # dvolume = np.sum(dvolumes)
        # totDVolume += dvolume
        comm = dvolumes * commRate

        # print(deltaPos)
        cash[t] = cash[t - 1] - (curPrices * deltaPos + comm)
        
        
        # posValue = curPos.dot(curPrices)
        # todayPL = cash + posValue - value
        # todayPLL.append(todayPL)
        # value = cash + posValue
        # ret = 0.0
        # if (totDVolume > 0):
            # ret = value / totDVolume
        # print ("Day %d value: %.2lf todayPL: $%.2lf $-traded: %.0lf return: %.5lf frac0: %.4lf frac1: %.4lf" % (t,value, todayPL, totDVolume, ret, frac0, frac1))
    # pll = np.array(todayPLL)
    # (plmu,plstd) = (np.mean(pll), np.std(pll))
    # annSharpe = 0.0
    # if (plstd > 0):
        # annSharpe = 16 * plmu / plstd
    return (cash, position)

# implement algo performance on particular stock

if __name__ == '__main__':
    commRate = 0.0050 # Commission rate.
    dlrPosLimit = 10000 # $ position limit
    
    prcHist = loadPrices("prices250.txt")

    cash, position = algo_performance(prcHist, 50)
    
    # print(position[-1])
    # final_PL = cash[-1] + position[-1] * prcHist[:,-1]
    # print(sum(final_PL))
