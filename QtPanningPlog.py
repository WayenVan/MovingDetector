import sys
import numpy as np
from pyqtgraph.widgets.GroupBox import GroupBox
import scipy.signal as signal

#import QT
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QRadioButton, QLineEdit, QVBoxLayout
from PyQt5 import QtWidgets

#import filters
import IIR2Filter
import IIRFilter


class QtPanningPlot:

    def __init__(self,title, num_max_data=100000):
        #addvariable for caculate:

        self.win = pg.GraphicsLayoutWidget()
        self.win.setWindowTitle(title)
        self.win.setBackground('w')
        self.layout = QtGui.QGridLayout()



        #data and filter for calculating
        self.data_speed = 0
        self.data_raw = []
        self.data_filtered = []

        #design filter:
        self.filter_lowpass = IIRFilter.IIRFilter(signal.cheby2(8, 40, 0.1*2, 
                                        btype='highpass', 
                                        output='sos'))

        #add widgets in qt
        self.plt = pg.PlotWidget(background='w')
        self.plt.setYRange(0,256)
        self.plt.setXRange(0,500)
        self.plt.setMouseEnabled(x=False, y=False)
        self.curve = self.plt.plot()

        #add Radio buttons
        self.rb_rawdata = QRadioButton("Raw data")
        self.rb_rawdata.setChecked(True)
        self.rb_filtered = QRadioButton("Filtered data")

        self.groupbox = GroupBox()
        #add output
        self.label = QLabel()
        self.label.setText("Output")
        self.output_line = QLineEdit()
        self.boxlayout = QtGui.QGridLayout()
        self.boxlayout.addWidget(self.label, 0, 0)
        self.boxlayout.addWidget(self.output_line, 0, 1)
        self.groupbox.setLayout(self.boxlayout)
        
        #add timer to refresh
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

        #set layout 
        self.layout.addWidget(self.plt, 0, 0)
        self.layout.addWidget(self.rb_rawdata, 1, 0)
        self.layout.addWidget(self.rb_filtered, 2, 0)
        self.layout.addWidget(self.groupbox, 3, 0)


        self.win.setLayout(self.layout)
        self.win.show()


    def update(self):
        self.data_raw = self.data_raw[-500:]
        self.data_filtered = self.data_filtered[-500:]
        
        if self.rb_rawdata.isChecked():
            if self.data_raw:
                self.plt.setYRange(0,256)
                self.curve.setData(np.hstack(self.data_raw))
        if self.rb_filtered.isChecked():
            if self.data_filtered:
                self.plt.setYRange(-40,40)
                self.curve.setData(np.hstack(self.data_filtered))
    
    def addData(self, d):
        self.data_raw.append(d)
        #filter and calculate in here
        self.data_filtered.append(self.filter_lowpass.filter(d))


