import numpy as np
import pandas as pd
from statistics import mean
import matplotlib.pyplot as plt

# Sum a list
def sum(ls):
    count = 0
    if ls:
        for elem in ls:
            count += elem
    return count


# Returns RSI of one instrument. Takes instrument price history and time as inputs
def ins_rsi(ins_ls, time = 14):
    up = []
    down = []
    if len(ins_ls) < time + 1:
        time = len(ins_ls) - 1
        if time == 0:
            return 50
    for i in range(time, 0, -1):
        price_before = float(ins_ls[-i - 1])
        price_today = float(ins_ls[-i])
        
        if price_before > price_today:
            down.append(price_before - price_today)
        elif price_before < price_today:
            up.append(price_today - price_before)
    up_ave = sum(up)/time
    down_ave = sum(down)/time


    # RS = Relative Strength, RSI = Relative Strength Index
    if down_ave:
        rs = up_ave/down_ave
        rsi = 100 - (100/(1+rs))
    else: # avoiding divide by 0
        rsi = 100
    
    return rsi
    


# checks rsi for each instrument using ins_rsi. Takes panda array as input
def rsi(prcSoFar, time = 14):
    (nins,nt) = prcSoFar.shape

    rsi_ls = []

    # Loop through the instruments
    for ins_ls in prcSoFar:
        # Track movements for day
        if nt < time: # Avoid index error, can only check as far as price history goes
            time = nt - 1
        rsi_ls.append(ins_rsi(ins_ls, time))
    return rsi_ls

# Standardise rsi of given instrument
def std_rsi(ins_ls, time = 14):
    rsi = ins_rsi(ins_ls, time)

    # Centre at 0
    rsi -= 50 
    # Scale to 1
    rsi = rsi / 50

    return rsi

def is_threshold_rsi(ins_ls, time = 14):
    rsi = ins_rsi(ins_ls, time)

    if rsi >= 70:
        return 1
    if rsi <= 40:
        return -1
    return 0

def EMA(ins_ls, time, prev_ema):
    return ins_ls[-1]*(2/(1+time)) + prev_ema*(1-(2/(1+time)))

def SMA(ins_ls, time):
    return mean(ins_ls[-time:])

# ------------- below was used for testing --------------- #
def loadPrices(fn):
    global nt, nInst
    df=pd.read_csv(fn, sep='\s+', header=None, index_col=None)
    nt, nInst = df.values.shape
    return (df.values).T

if __name__ == '__main__':
    nInst, nt = 0, 0
    prcAll = loadPrices("prices250.txt")


    a = []

    for t in range(50,251):
        prcHistSoFar = prcAll[:,:t]

        rsi_t = rsi(prcHistSoFar)
        a.append(rsi_t[1])

    print(a)

    plt.plot(a)
    plt.axhline(y=30, color = 'r', linestyle = '-')
    plt.axhline(y=70, color = 'r', linestyle = '-')
    plt.show()
