import sys
import numpy as np
from pyqtgraph.widgets.GroupBox import GroupBox
import scipy.signal as signal

#import QT
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QRadioButton, QLineEdit, QVBoxLayout, QCheckBox
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
        self.data_handled = []

        #design filter:
        self.filter_highpass = IIRFilter.IIRFilter(signal.cheby2(8, 40, 0.1/30.0*2, 
                                        btype='highpass', 
                                        output='sos'))
        self.filter_lowpass = IIRFilter.IIRFilter(signal.cheby2(4, 60, 7.5/30.0*2, 
                                        btype='lowpass', 
                                        output='sos'))

        #add widgets in qt
        self.plt = pg.PlotWidget(background='w')
        self.plt.setYRange(0,256)
        self.plt.setXRange(0,500)
        self.plt.setMouseEnabled(x=False, y=False)
        self.curve = self.plt.plot()

        #add Radio buttons
        self.select_box = GroupBox("filter")
        self.select_boxlayout = QtGui.QGridLayout()
        self.rb_filter1 = QCheckBox("remove DC")
        self.rb_filter2 = QCheckBox("remove High")
        self.rb_filter1.setChecked(True)
        self.rb_filter2.setChecked(True)
        self.select_boxlayout.addWidget(self.rb_filter1, 0, 0)
        self.select_boxlayout.addWidget(self.rb_filter2, 0, 1)
        self.select_box.setLayout(self.select_boxlayout)
        
        #add output text
        self.output_box = GroupBox("Output")
        self.label = QLabel()
        self.label.setText("the period of the Jie pai qi")
        self.output_line = QLineEdit()
        self.output_boxlayout = QtGui.QGridLayout()
        self.output_boxlayout.addWidget(self.label, 0, 0)
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


    def update(self):
        self.data_raw = self.data_raw[-500:]
        self.data_handled = self.data_handled[-500:]
    
        if self.data_handled:
            self.plt.setYRange(0, 256)
            self.curve.setData(np.hstack(self.data_handled))
        
        if not (self.rb_filter1.isChecked() and self.rb_filter2.isChecked()):
            self.label.setText("select all filter to start detection")
        else:
            self.label.setText("the period is {}".format(1))
    
    def addData(self, d):
        self.data_raw.append(d)
        dh = d
        
        if self.rb_filter1.isChecked():
            dh = self.filter_highpass.filter(dh)
        if self.rb_filter2.isChecked():
            dh = self.filter_lowpass.filter(dh)
        
        if self.rb_filter1.isChecked() and self.rb_filter2.isChecked():
            #detection
            pass
        
        
        #impelement detect function here!
        self.data_handled.append(dh)


