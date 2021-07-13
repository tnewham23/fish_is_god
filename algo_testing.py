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
        
    return (cash, position)


if __name__ == '__main__':
    commRate = 0.0050 # Commission rate.
    dlrPosLimit = 10000 # $ position limit
    
    prcHist = loadPrices("prices250.txt")

    cash, position = algo_performance(prcHist, 50)
    
    value = cash[-250:] + position[-250:] * prcHist.T
    
    SMA10 = lambda x : plotting.SMA(x, 10)
    SMA30 = lambda x : plotting.SMA(x, 30)

    plotting.plot_instance(prcHist, [
        {'metric' : [SMA10, SMA30], 'name' : ["SMA10", "SMA30"]},
        {'metric' : plotting.vector_rsi_instance, 'bounds':[30, 70], 'name' : "RSI"},
        {'metric' : position.T, 'name' : "position", 'styles' : ['b']},
        {'metric' : value.T, 'name' : "profit/loss", 'styles' : ['b']}
    ])
    
    
    # final_PL = cash[-1] + position[-1] * prcHist[:,-1]
    # print(sum(final_PL))
    # agrees with eval.py, so hopefully the code works
