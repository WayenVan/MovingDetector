import scipy.signal as signal
import numpy as np
from IIR2Filter import IIR2Filter

class IIRFilter:
    def __init__(self, sos):

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
    sos = signal.cheby1(8, 10, 0.1*2, output='sos')
    filter = IIRFilter(sos)
    data = 10
    y = x.filter(data)
    print(y)