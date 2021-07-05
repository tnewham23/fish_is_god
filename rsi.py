import numpy as np

def sum(ls):
    count = 0
    if ls:
        for elem in ls:
            count += elem
    return count


# Returns RSI of one instrument
def ins_rsi(ins_ls, time):
    up = []
    down = []
    for i in range(time, 0, -1):
        price_before = int(ins_ls[i - 1])
        price_today = int(ins_ls[i])
        
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
    


# checks rsi for each instrument
def rsi(prcSoFar, time = 14):
    (nins,nt) = prcSoFar.shape

    rsi_ls = []

    # Loop through the instruments
    for ins_ls in prcSoFar:
        # Track movements for day
        if nt <= 15:
            time = nt - 1
        rsi_ls.append(ins_rsi(ins_ls, time))
    return rsi_ls



