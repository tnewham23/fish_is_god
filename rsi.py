import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Sum a list
def sum(ls):
    count = 0
    if ls:
        for elem in ls:
            count += elem
    return count


# Returns RSI of one instrument. Takes instrument price history and time as inputs
def ins_rsi(ins_ls, time):
    up = []
    down = []
    for i in range(time, 0, -1):
        price_before = float(ins_ls[-i - 1])
        price_today = float(ins_ls[-i])
        
        if price_before > price_today:
            up.append(price_before - price_today)
        elif price_before < price_today:
            down.append(price_today - price_before)
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


# ------------- below was used for testing --------------- #
def loadPrices(fn):
    global nt, nInst
    df=pd.read_csv(fn, sep='\s+', header=None, index_col=None)
    nt, nInst = df.values.shape
    return (df.values).T

pricesFile="./prices250.txt"
prcAll = loadPrices(pricesFile)
print ("Loaded %d instruments for %d days" % (nInst, nt))

x = []
for t in range(0,100):
    x.append([])

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
