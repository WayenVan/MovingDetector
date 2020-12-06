import sys
import numpy as np
import scipy.signal as signal
import pickle

#import QT
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

from QtPanningPlog import *

sys.path.append("./webcam2rgb")
import webcam2rgb
#import pannal

# create a global QT application object
app = QtGui.QApplication(sys.argv)
#panningPlot = QtPanningPlot("helloworld")
main_window = MainWindow("person detect system")

    
def callBack(retval, data):
    b = data[0]
    g = data[1]
    r = data[2]
    main_window.addData(r)

camera = webcam2rgb.Webcam2rgb()

#check the samplling rate of 
camera.start(callback = callBack, cameraNumber=0)
print("camera samplerate: ", camera.cameraFs(), "Hz")

app.exec_()

#save data episode for better design filter
f = open("./data/data_clip.dat", 'wb')
#pickle.dump(panningPlot.data_raw, f)
f.close()

camera.stop()
