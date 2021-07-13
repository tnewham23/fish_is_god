import numpy as np
import pandas as pd
#from math import sqrt
#from sklearn import metrics
#from sklearn import linear_model
#from sklearn.model_selection import train_test_split
from eval import loadPrices
import trading_functions


pricesFile="./prices250.txt"
#prcAll = loadPrices(pricesFile)

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



corrMatrix = corr_mat(pricesFile)
pos_cor = cor_ins(corrMatrix, 0.9)
print(f"Instruments with positive correlation above 0.9 = {pos_cor}")
neg_cor = cor_ins(corrMatrix, -0.9, False)
print(f"Instruments with negative correlation below 0.9 = {neg_cor}")

print(corrMatrix)