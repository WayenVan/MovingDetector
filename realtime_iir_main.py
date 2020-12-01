import sys
import numpy as np
import scipy.signal as signal

#import QT
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

#import filters
import IIR2Filter
import IIRFilter

sys.path.append("./webcam2rgb")
import webcam2rgb

# create a global QT application object
app = QtGui.QApplication(sys.argv)

#global counter for the framerate
counter = 0

class QtPanningPlot:

    def __init__(self,title, num_max_data=100000):
        #addvariable for caculate:

        self.win = pg.GraphicsLayoutWidget()
        self.win.setWindowTitle(title)

        self.layout = QtGui.QGridLayout()

        #all data
        self.data_speed = 0
        self.data_raw = []
        self.data_filtered = []

        #add plot
        self.plt_rawdata = pg.PlotWidget()
        self.plt_rawdata.setYRange(0,256)
        self.plt_rawdata.setXRange(0,500)
        self.curve_rawdata = self.plt_rawdata.plot()

        #add plot_filtered
        self.plt_filtered = pg.PlotWidget()
        self.plt_filtered.setYRange(0,256)
        self.plt_filtered.setXRange(0,500)
        self.curve_filtered = self.plt_filtered.plot()

        #add timer to refresh
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

        #set layout 
        self.layout.addWidget(self.plt_filtered, 0, 0)
        self.layout.addWidget(self.plt_rawdata, 1, 0)

        self.win.setLayout(self.layout)
        self.win.show()


    def update(self):
        self.data_raw = self.data_raw[-500:]
        if self.data_raw:
            self.curve_rawdata.setData(np.hstack(self.data_raw))

    def addData(self, d):
        self.data_raw.append(d)
        #filter and calculate in here


application = QtPanningPlot("helloworld")
    
def callBack(retval, data):
    b = data[0]
    g = data[1]
    r = data[2]
    application.addData(r)


camera = webcam2rgb.Webcam2rgb()

#check the samplling rate of 
camera.start(callback = callBack, cameraNumber=0)
print("camera samplerate: ", camera.cameraFs(), "Hz")

app.exec_()


camera.stop()
