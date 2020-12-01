
class IIR2Filter:
    #2nd order IIR filter
    def __init__(self,_b0,_b1,_b2,_a0,_a1,_a2,):
        self.a0 = _a0
        self.a1 = _a1
        self.a2 = _a2
        self.b0 = _b0
        self.b1 = _b1
        self.b2 = _b2
        self.buffer1 = 0
        self.buffer2 = 0
    
    def filter(self,x):  #x as input  acc_input=accumulator input
        #IIR PART
        acc_input = float()
        acc_output = float()
        acc_input = x*self.a0 - self.buffer1*self.a1 - self.buffer2*self.a2

        #FIR part 
        #acc_output = acc_input * self.b0 + self.buffer1*self.b1
        acc_output = acc_input * self.b0 + self.buffer1*self.b1+ self.buffer2*self.b2
        self.buffer2 = self.buffer1
        self.buffer1 = acc_input
        
        return acc_output