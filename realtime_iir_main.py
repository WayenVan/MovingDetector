import sys
import numpy as np
import scipy.signal as signal
import pickle

#import QT
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

#import filters
import IIR2Filter
import IIRFilter

sys.path.append("./webcam2rgb")
import webcam2rgb
#import pannal
from QtPanningPlog import *

# create a global QT application object
app = QtGui.QApplication(sys.argv)
panningPlot = QtPanningPlot("helloworld")

#data episode
dataEpisode = []
    
def callBack(retval, data):
    b = data[0]
    g = data[1]
    r = data[2]
    panningPlot.addData(r)

    #save data episode
    global dataEpisode
    dataEpisode = panningPlot.data_raw

camera = webcam2rgb.Webcam2rgb()

#check the samplling rate of 
camera.start(callback = callBack, cameraNumber=0)
print("camera samplerate: ", camera.cameraFs(), "Hz")

app.exec_()

#save data episode for better design filter
print(dataEpisode)
f = open("./data/data_clip.dat", 'wb')
pickle.dump(dataEpisode, f)
f.close()

camera.stop()
