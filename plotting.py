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


def plot_instance(prcHist, list_of_metrics=None):
    """Plots (dynamically) stock prices against given metrics

    Parameters
    ----------
    prcHist : numpy array or list
        Stock data.
    list_of_metrics : list of dictionaries detailing the metrics passed
        Defaults to None, in which case no metrics are plotted.
        Dictionaries have 3 parameters:
            metric: the function (or list of functions) to be plotting
            metric name: a string (or list thereof) detailing the name(s) of the metric(s)
            bounds (optional): any horizontal lines to be drawn on the plot

    Returns
    -------
    None
    """


    # setup initial plot, plot stock 0
    if list_of_metrics:
        fig, axs = plt.subplots(len(list_of_metrics) + 1, sharex=True)
    else:
        # bit of a bad style trick to avoid changing the axs[0] below
        fig, ax = plt.subplots()
        axs = [ax]
    
    l, = axs[0].plot(prcHist[0])
    axs[0].set_title(f"Stock: 0")
    axs[0].set_ylabel("$ price")
    if list_of_metrics:
        axs[len(list_of_metrics)].set_xlabel("date")
    else:
        axs[0].set_xlabel("date")

    
    def initialise_aux_plots(stock_indx):    
        list_list_curves = []
        
        if not list_of_metrics:
            return list_list_curves

        for i, metric_info in enumerate(list_of_metrics):
            
            metric_name = metric_info['name']
            
            # draw horizontal lines
            if 'bounds' in metric_info.keys():
                for line in metric_info['bounds']:
                    axs[i + 1].axhline(y=line, color = 'r', linestyle = '-')

            # handle one metric being passed
            if not isinstance(metric_info['metric'], list):
                metrics = [metric_info['metric']]
                metric_name = [metric_name]
            else:
                metrics = metric_info['metric']

            curves = []
            for j, metric0 in enumerate(metrics):
                metric_name0 = metric_name[j]

                metric_data = metric0(prcHist[stock_indx])

                curves.append((axs[i + 1].plot(metric_data, "--", label=metric_name0))[0])

                axs[i + 1].legend()
            list_list_curves.append(curves)
        
        return list_list_curves
    
    def update_aux_plots(stock_indx, list_list_curves):
        if not list_of_metrics:
            return
        
        for i, metric_info in enumerate(list_of_metrics):
            
            metric_name = metric_info['name']

            # handle one metric being passed
            if not isinstance(metric_info['metric'], list):
                metrics = [metric_info['metric']]
                metric_name = [metric_name]
            else:
                metrics = metric_info['metric']

            for j, metric0 in enumerate(metrics):
                metric_data = metric0(prcHist[stock_indx])
                list_list_curves[i][j].set_ydata(metric_data)
                
            axs[i + 1].relim()
            axs[i + 1].autoscale_view()
            axs[i + 1].legend()

    list_list_curves = initialise_aux_plots(0)

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
        
        update_aux_plots(stock_indx, list_list_curves)
        
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
        x.append(rsi.ins_rsi(prcHistSoFar[stock_indx], 17))
    
    plt.plot(x, label='RSI')
    plt.axhline(y=30, color = 'r', linestyle = '-')
    plt.axhline(y=70, color = 'r', linestyle = '-')

    plt.legend()
    plt.xlabel("Date")
    plt.ylabel("RSI")
    plt.title(f"RSI of Stock: {stock_indx}")

# example of vectorising RSI function (taken directly from above)
def vector_rsi_instance(data):
    x = []
    # generate rsi values for each day
    for i in range(0, 250):
        if i == 0:
            x.append(50)
            continue
        prcHistSoFar = data[:i]
        x.append(rsi.ins_rsi(prcHistSoFar, 20))
    
    return x

# example with SMA function
def SMA(data, window):
    return pd.DataFrame(data)[0].rolling(window=window).mean()

# def SMA_optimized(data, window):
    

def ATR(data, window):
    TR = []
    # TODO: need an initial value here, otherwise off by 1 as mentioned
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
    SMA8 = lambda x : SMA(x, 8)
    SMA10 = lambda x : SMA(x, 10)
    SMA24 = lambda x : SMA(x, 24)
    SMA30 = lambda x : SMA(x, 30)
    SMA50 = lambda x : SMA(x, 50) 
    ATR14 = lambda x: ATR(x, 14)
    # these lambdas are just wrapper functions that pass a constant window argument
    
    # example: no metrics 
    # plot_instance(prcHist)

    # example: one metric 
    # plot_instance(prcHist, [{'metric' : SMA10, 'name' : 'SMA10'}])

    # example: multiple metrics on one plot 
    # plot_instance(prcHist, [{'metric' : [SMA10, SMA30], 'name' : ["SMA10", "SMA30"]}])

    # example: multiple metrics, multiple plots
    # plot_instance(prcHist, [
    #     {'metric' : [SMA10, SMA30], 'name' : ["SMA10", "SMA30"]}, 
    #     {'metric' : ATR14, 'name' : "ATR14"} # behaviour identical to passing [ATR14] and ["ATR14"]
    # ])
    
    # example: metric and bounding lines
    # plot_instance(prcHist, [
    #     {'metric' : ATR14, 'bounds':[0.1,0.7], 'name' : "ATR14"}
    # ])

    # example: plot of multiple(ish) metrics with bounds
    plot_instance(prcHist, [
        {'metric' : [SMA10, SMA30], 'name' : ["SMA10", "SMA30"]},
        {'metric' : vector_rsi_instance, 'bounds':[30, 70], 'name' : "RSI"}
    ])
    
    plt.show()
