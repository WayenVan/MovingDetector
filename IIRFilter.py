from math import cos
import scipy.signal as signal
import numpy as np
from IIR2Filter import IIR2Filter
import matplotlib.pyplot as plt

class IIRFilter:
    def __init__(self, sos: np.ndarray):

        self.sos_filters = []
        #generate 2nd order filters
        for index in range(sos.shape[0]):
            ba = sos[index]
            filter_tmp = IIR2Filter(ba[0], ba[1], ba[2], ba[3], ba[4], ba[5])
            self.sos_filters.append(filter_tmp)
    
    def filter(self,x):  #x as input  acc_input=accumulator input
        output = x
        for filter in self.sos_filters:
            output = filter.filter(output)
        return output


if(__name__ == "__main__"):
    fs = 1000
    T = 1/fs
    n = 1000
    x = np.linspace(0,(n-1)*T, n)
    y = 3*np.cos(2*np.pi*80*x)+np.cos(2*np.pi*200*x)+np.cos(2*np.pi*300*x)

    sos = signal.cheby1(8, 1, 100/fs*2, output='sos')

    result = np.array([])
    filter = IIRFilter(sos)
    for yi in y:
        result = np.append(result, filter.filter(yi))
    
    plt.plot(y, label="raw data")
    plt.plot(result, label = "filtered")
    plt.legend()
    plt.show()