import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import pandas as pd
import numpy as np
import rsi
import sys

# copied from eval.py
def loadPrices(fn):
    global nt, nInst
    df=pd.read_csv(fn, sep='\s+', header=None, index_col=None)
    nt, nInst = df.values.shape
    return (df.values).T

# takes prcHist as a numpy array
# stock_indx as the instrument of interest
# list of metrics as a list of functions which return an array of metric data from a column
# list of corresponding metric names, for legend
# supports list of lists for plotting multiple metrics on one plot (e.g SMA10, SMA25, SMA50)
def plot_instance(prcHist, list_of_metrics=None, metric_names=None):

    # setup initial plot, plot stock 0
    if list_of_metrics:
        fig, axs = plt.subplots(len(list_of_metrics) + 1, sharex=True)
    else:
        fig, axs = plt.subplots()
    
    l, = axs[0].plot(prcHist[0])
    axs[0].set_title(f"Stock: 0")
    axs[0].set_ylabel("$ price")
    axs[len(list_of_metrics)].set_xlabel("date")
    
    def initialise_aux_plots(stock_indx):    
        ls = []
        
        for i, metric in enumerate(list_of_metrics):
            metric_name = metric_names[i]
            
            # check if metric is many metrics on one plot
            if isinstance(metric, list):
                ls0 = []
                for j, metric0 in enumerate(metric):
                    metric_name0 = metric_name[j]
                    
                    metric_data = metric0(prcHist[stock_indx])
                    
                    ls0.append((axs[i + 1].plot(metric_data, "--", label=metric_name0))[0])

                axs[i + 1].legend()
                ls.append(ls0)
            
            else:
                # compute metric on data
                metric_data = metric(prcHist[stock_indx])

                # plot
                ls.append((axs[i + 1].plot(metric_data, "--", label=metric_name))[0])
                axs[i + 1].legend()
        
        return ls
    
    ls = initialise_aux_plots(0)
    
    def update_aux_plots(stock_indx, ls):
        for i, metric in enumerate(list_of_metrics):
            metric_name = metric_names[i]
            
            if isinstance(metric, list):
                for j, metric0 in enumerate(metric):
                    metric_data = metric0(prcHist[stock_indx])
                    
                    ls[i][j].set_ydata(metric_data)

                axs[i + 1].relim()
                axs[i + 1].autoscale_view()
                axs[i + 1].legend()
            
            else:
                # compute metric on data
                metric_data = metric(prcHist[stock_indx])

                # plot
                ls[i].set_ydata(metric_data)
                axs[i + 1].relim()
                axs[i + 1].autoscale_view()
                axs[i + 1].legend()
    
    # positioning of the bar/margins
    plt.subplots_adjust(bottom=0.25)

    slider_bkd_color = 'red'
    ax_stock_indx = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=slider_bkd_color)

    # create slider
    slider_index = Slider(
        ax_stock_indx, "Stock Index", 0, 100,
        valinit=0, valstep=1
    )

    # routine to be called on updates to index of interest
    def update(val):
        stock_indx = int(slider_index.val)
        l.set_ydata(prcHist[stock_indx])
        axs[0].relim()
        axs[0].autoscale_view()
        axs[0].set_title(f"Stock: {stock_indx}")
        
        update_aux_plots(stock_indx, ls)
        
        fig.canvas.draw_idle()

    slider_index.on_changed(update)

    plt.show()


# takes prcHist as numpy array
# stock_indx as the instrument of interest
def plot_rsi_instance(prcHist, stock_indx):
    x = []
    plot_b = plt.figure(2)
    # generate rsi values for each day
    for i in range(0, 250):
        if i == 0:
            x.append(50)
            continue
        prcHistSoFar = prcHist[:,:i]
        x.append(rsi.ins_rsi(prcHistSoFar[stock_indx], 14))
    
    plt.plot(x, label='RSI')
    plt.axhline(y=30, color = 'r', linestyle = '-')
    plt.axhline(y=70, color = 'r', linestyle = '-')

    plt.legend()
    plt.xlabel("Date")
    plt.ylabel("RSI")
    plt.title(f"RSI of Stock: {stock_indx}")

# example with SMA function
def SMA(data, window):
    return pd.DataFrame(data)[0].rolling(window=window).mean()

def ATR(data, window):
    TR = []
    for i in range (1, len(data)):
        tr = abs(data[i] - data[i-1])/data[i] * 100
        TR.append(tr)
    return pd.DataFrame(TR)[0].rolling(window=window).mean()

# example showing what the code can do
if __name__ == '__main__':
    nInst, nt = 0, 0
    prcHist = loadPrices("prices250.txt")
    # metrics: functions that accept a vector/array/list of data for one stock and
    #   return a corresponding vector of the calculated metric for that instrument
    SMA10 = lambda x : SMA(x, 10)
    SMA30 = lambda x : SMA(x, 30)
    SMA50 = lambda x : SMA(x, 50) 
    ATR14 = lambda x: ATR(x, 14)
    # these lambdas are just wrapper functions that pass a constant window argument
    
    # # one metric example
    # plot_instance(prcHist, 15, [SMA10], ["SMA10"])
    # plt.show()
    # 
    # # multiple metrics on one plot example
    # plot_instance(prcHist, 15, [[SMA10, SMA30]], [["SMA10", "SMA30"]])
    # plt.show()

    # multiple metrics, multiple plots
    plot_instance(prcHist, [[SMA10, SMA30], SMA50, ATR14], [["SMA10", "SMA30"], "SMA50", "ATR"])
    plt.show()
