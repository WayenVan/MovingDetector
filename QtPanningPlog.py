import sys
from PyQt5.QtGui import QRegularExpressionValidator, qAlpha
import numpy as np
from pyqtgraph.functions import mkPen
from pyqtgraph.graphicsItems.DateAxisItem import DAY_HOUR_ZOOM_LEVEL
from pyqtgraph.widgets.GroupBox import GroupBox
import scipy.signal as signal

#import QT
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

from PyQt5.QtWidgets import QGridLayout, QLabel, QCheckBox, QPushButton, QPlainTextEdit, QTextEdit
from PyQt5.QtCore import Qt

#import filters
import IIRFilter

import time

class PersonDetector:
    """a class to detect if a person move"""
    def __init__(self, min_difference):
        self.min_difference = min_difference #the min drop to define a person passing by
        self.data_previous = 0 # data buffer of the previous one
        self.drop = 0 # the total light drop 
    
    def detect(self, newData):
        if newData<self.data_previous:
            # calculate accumulation of a continous drop
            self.drop+=(self.data_previous - newData)
            self._update(newData)
            return False
        else: #drop stop or pixel become higher
            if self.drop >= self.min_difference: # if total drop larger than we defined, it means something pass throw the webcam
                self.drop = 0
                self._update(newData)
                return True
            else: 
                self.drop = 0
                self._update(newData)
                return False

    def clean(self):
        #clean all the data of this detector
        self.drop = 0
        self.data_previous = 0

    def _update(self, newData):
        #update previous data
        self.data_previous = newData


class LogBrowser(QtGui.QMainWindow):
    """a log browser to view"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("log browser")
        self.setGeometry(400, 100, 400, 400)

        self.log_view = QTextEdit()

        self.setCentralWidget(self.log_view)

    def append(self, str):
        self.log_view.append(str)

class QtPanningPlot:

    def __init__(self,title, num_max_data=100000):

        #data and filter for calculating
        self.data_raw = []
        self.data_handled = []
        self.output_buffer = []

        self.detector = PersonDetector(70)

        #design filter:
        self.filter_lowpass = IIRFilter.IIRFilter(signal.cheby2(4, 100, 7.0/30.0*2, 
                                        btype='lowpass', 
                                        output='sos'))
        self.filter_mv185 = IIRFilter.IIRFilter(signal.cheby2(6, 10, [1.75/30.0*2, 1.95/30*2],
                                        btype='bandstop',
                                        output='sos'))

        #text window
        self.log_win = LogBrowser()
        

        #main window
        self.win = pg.GraphicsLayoutWidget()
        self.win.setWindowTitle(title)
        self.win.setBackground('w')
        self.layout = QtGui.QGridLayout()                             

        #add widgets in qt
        self.plt = pg.PlotWidget(background='w')
        self.plt.setYRange(0,256)
        self.plt.setXRange(0,500)
        self.plt.setMouseEnabled(x=False, y=False)
        pen_line = mkPen(width=4, color='10A5F5')
        pen_axis = mkPen(width=5, color='808080')
        self.plt.getAxis('bottom').setPen(pen_axis)
        self.plt.getAxis('bottom').setTextPen(pen_axis)
        self.plt.getAxis('left').setPen(pen_axis)
        self.plt.getAxis('left').setTextPen(pen_axis)
        

        self.curve = self.plt.plot(pen=pen_line)

        #add Radio buttons
        self.select_box = GroupBox("filter")
        self.select_boxlayout = QtGui.QGridLayout()
        self.rb_lowpss = QCheckBox("remove High")
        self.rb_lowpss.setChecked(True)
        self.rb_mv185 = QCheckBox("remove 1.85Hz")
        self.rb_mv185.setChecked(True)
        self.select_boxlayout.addWidget(self.rb_lowpss, 0, 0)
        self.select_boxlayout.addWidget(self.rb_mv185, 0, 1)
        self.select_box.setLayout(self.select_boxlayout)
        
        #add output text and log button
        self.output_box = GroupBox("Output")
        self.b_log = QPushButton("Open log")
        self.b_log.clicked.connect(self.openLog)
        self.label = QLabel()
        self.label.setText("the period of the Jie pai qi")
        self.output_boxlayout = QtGui.QGridLayout()
        self.output_boxlayout.addWidget(self.label, 0, 0)
        self.output_boxlayout.addWidget(self.b_log, 0, 1, alignment=Qt.AlignRight)
        self.output_box.setLayout(self.output_boxlayout)
        
        #add timer to refresh
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

        #set layout 
        self.layout.addWidget(self.plt, 0, 0)
        self.layout.addWidget(self.select_box, 1, 0)
        self.layout.addWidget(self.output_box, 3, 0)

        self.win.setLayout(self.layout)
        self.win.show()

    def openLog(self):
        self.log_win.show()

    def update(self):
        self.data_raw = self.data_raw[-500:]
        self.data_handled = self.data_handled[-500:]
    
        if self.data_handled:
            self.curve.setData(np.hstack(self.data_handled))
    
    def addData(self, d):
        self.data_raw.append(d)
        dh = d
        
        #do all filter
        if self.rb_lowpss.isChecked():
            dh = self.filter_lowpass.filter(dh)
        
        if self.rb_mv185.isChecked():
            dh = self.filter_mv185.filter(dh)

        #detect if someone pass by
        if (self.rb_lowpss.isChecked() and self.rb_mv185.isChecked()):
            detect_result = self.detector.detect(dh)
            if(detect_result):
                #update log file and text on the window
                seconds = time.time()
                local_time = time.ctime(seconds)

                self.label.setText("A person pass at {}".format(local_time))
                self.log_win.append("A person pass at {}\n".format(local_time))

                log_file = open("history.log", 'a')
                log_file.write("A person pass at {}".format(local_time))
                log_file.close()
        else:
            self.detector.clean()
            self.label.setText("Select all filter to start detect")


        self.data_handled.append(dh)


