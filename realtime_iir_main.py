import sys
from time import sleep
import numpy as np
import scipy.signal as signal
import pickle

#import QT
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

from MainWindow import *

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

#calculate num of data
counter = 0
time_pre = 0
def callBack2(retaval, data):
    global counter
    global time_pre

    #to eliminate jitter, every interval between datas should larger than 0.01
    now = time.time()
    if (now- time_pre)>0.010:
        counter += 1
    time_pre = now



camera = webcam2rgb.Webcam2rgb()
print("start calculating sampling rate")

#check the samplling rate of camera
time_pre = time.time() #initiate time
camera.start(callback = callBack2, cameraNumber=0)
#sleep 5 seconds to calculate sample rate
time.sleep(5)
print("camera samplerate: {}Hz".format(counter/5.0))
camera.stop()

camera.start(callback = callBack, cameraNumber=0)
#print("camera samplerate: ", camera.cameraFs(), "Hz")

app.exec_()


camera.stop()
