import numpy as np
import pandas as pd
import trading_functions

def loadPrices(fn):
    global nt, nInst
    df=pd.read_csv(fn, sep='\s+', header=None, index_col=None)
    nt, nInst = df.values.shape
    return (df.values).T

pricesFile="./prices250.txt"

# Returns correlation matrix
def corr_mat(price_file):
    df=pd.read_csv(pricesFile, sep='\s+', header=None, index_col=None)
    corrMatrix = (df).corr()
    return corrMatrix

# returns index of correlated instruments above (or below) a given threshold
def cor_ins(corrMatrix, threshold, above = True):
    results = []
    i = 0
    while i < 100:
        j = i + 1
        while j < 100:
            if above:
                if corrMatrix[i][j] >= threshold:
                    indices = (i,j)
                    results.append(indices)
            else:
                if corrMatrix[i][j] <= threshold:
                    indices = (i,j)
                    results.append(indices)
            j += 1
        i += 1
    return results


if __name__ == '__main__':
    corrMatrix = corr_mat(pricesFile)
    pos_cor = cor_ins(corrMatrix, 0.9)
    print(f"Instruments with positive correlation above 0.9 = {pos_cor}")
    neg_cor = cor_ins(corrMatrix, -0.9, False)
    print(f"Instruments with negative correlation below 0.9 = {neg_cor}")

    print(corrMatrix)