# Python File for GUI

from FYPUI import Ui_MainWindow
from pyqtgraph.Qt import QtGui
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from datetime import datetime
from pathlib import Path
import pyads
import pandas as pd
import numpy as np
import pyqtgraph as pg
import sys
import os
import time


# TWINCAT Initialisation
PLC_IP = '192.168.0.111.1.1'
plc = pyads.Connection(PLC_IP, 851)
plc.open()

class MainWindow(qtw.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)       
        self.setupUi(self)
        self.setMinimumSize(1300,1000)

    ## Add all additional functionality below ##
    
    # Button Click Handling
        self.btn_pumpflow.clicked.connect(self.btnpress_pumpflow)
        self.btn_motoramp.clicked.connect(self.btnpress_motoramp)
        self.btn_motorfreq.clicked.connect(self.btnpress_motorfreq)
        self.btn_changedir.clicked.connect(self.getDirectory)
    
    # Initialise Progress Bar + Progress text for idle
        self.progressBar.setValue(0)
        self.progresstext.setText('System is currently idle')
    
    # Initialise current directory:
        directory = os.getcwd()
        self.currentDirLabel.setText(directory)
       
    # Initialise plot
        self.plot1.plot()
        self.plot2.plot([0, 0.1, 0.2, 0.3, 0.4],np.array([4,4,4,4,4]), pen='r')
    
    # Directory selection for saving .csv file
    def getDirectory(self):
        response = qtw.QFileDialog.getExistingDirectory(self, 'Select a folder')
        self.currentDirLabel.setText(response)
        if response == '':
            self.currentDirLabel.setText(os.getcwd())
        return response
       
        
            
    # Pump Flow Button
    def btnpress_pumpflow(self):
        msg = qtw.QMessageBox.warning(self,'The setup will change', 'Are you sure?', qtw.QMessageBox.Ok|qtw.QMessageBox.Cancel) #Error Message Box
        switch = 2 #plc.read_by_name('MAIN.switch')
        if msg == qtw.QMessageBox.Cancel:
            qtw.QMessageBox.close
        elif msg == qtw.QMessageBox.Ok:
            if switch != 1:
                self.progressbar_transition()
            plc.write_by_name('MAIN.switch', 1)
            arr1_vals = plc.read_by_name('MAIN.arr1', pyads.PLCTYPE_ARR_REAL(100))
            time_vals = plc.read_by_name('MAIN.t',pyads.PLCTYPE_ARR_REAL(100))
            self.rawdatatocsv(arr1_vals, time_vals)
            self.sin_loop()
            switch = 0
            self.progressbar_run()
            self.plot1.clear()
    
    # Motor Frequency Button
    def btnpress_motorfreq(self):
        msg = qtw.QMessageBox.warning(self,'The setup will change', 'Are you sure?', qtw.QMessageBox.Ok|qtw.QMessageBox.Cancel)
        switch = plc.read_by_name('MAIN.switch')
        if msg == qtw.QMessageBox.Cancel:
            qtw.QMessageBox.close
        elif msg == qtw.QMessageBox.Ok:
            if switch != 2:
                self.progressbar_transition()
            plc.write_by_name('MAIN.switch', 2)
            arr1_vals = plc.read_by_name('MAIN.arr1', pyads.PLCTYPE_ARR_REAL(100))
            time_vals = plc.read_by_name('MAIN.t',pyads.PLCTYPE_ARR_REAL(100))
            self.rawdatatocsv(arr1_vals, time_vals)
            self.cos_loop()
            self.progressbar_run()
            self.plot1.clear()      

    # Motor Amplitude Button
    def btnpress_motoramp(self):
        msg = qtw.QMessageBox.warning(self,'The setup will change', 'Are you sure?', qtw.QMessageBox.Ok|qtw.QMessageBox.Cancel)
        switch = plc.read_by_name('MAIN.switch')
        if msg == qtw.QMessageBox.Cancel:
            qtw.QMessageBox.close
        elif msg == qtw.QMessageBox.Ok:
            if switch != 3:
                self.progressbar_transition()
            plc.write_by_name('MAIN.switch', 3)
            arr1_vals = plc.read_by_name('MAIN.arr1', pyads.PLCTYPE_ARR_REAL(100))
            time_vals = plc.read_by_name('MAIN.t',pyads.PLCTYPE_ARR_REAL(100))
            self.rawdatatocsv(arr1_vals, time_vals)           
            self.progressbar_run()
            self.plot1.clear()
    
    ## Progress Bar + Progress Bar Text
    def progressbar_idle(self): # Initialising empty
        qtw.QProgressBar.setValue(0)
        qtw.QLabel.setText(self.progresstext, 'System is idle')

    def progressbar_transition(self):  # Progress bar during transition = yellow
        qtw.QProgressBar.setStyleSheet(self, "QProgressBar::chunk "
        "{"
        "background-color: yellow;"
        "}")
        qtw.QLabel.setText(self.progresstext, 'Transitioning Setup')
        for i in range(100):
            time.sleep(0.1)
            self.progressBar.setValue(i+1)
        self.progresstext.setText('Transitioning')
                
    def progressbar_run(self):  # Progress bar during run = green
        qtw.QLabel.setText(self.progresstext, 'In progress')
        qtw.QProgressBar.setStyleSheet(self, "QProgressBar::chunk "
        "{"
        "background-color: green;"
        "}")
        for i in range(100):
            time.sleep(0.1)
            self.progressBar.setValue(i+1)
        self.progresstext.setText('Experiment Complete')
        qtw.QMessageBox.information(self,'Done','Press OK to continue')
        self.progressBar.setValue(0)
        self.plot1.plot()
        self.progresstext.setText('System is idle')

    # Live plot of experiment data
    # Hangs when running with progress bar
    """
    def updateplot(self):
        timer = time.localtime()
        points = 100
        X = np.arange(points)
        Y = np.sin(np.arange(points)/points*3*np.pi+time.time())
        C = pg.mkPen(color='r',width=10)
        self.plot1.plot(X,Y,pen='r',clear=True)  
        qtc.QTimer.singleShot(1, self.updateplot)
    """

    # Display sin function in Plot 1:
    def sin_loop(self):
        x = np.linspace(-np.pi, np.pi, 201)
        y = np.sin(x)
        self.plot1.plot(x,y, pen='y')

    # Display cos function in Plot 1:
    def cos_loop(self):
        x = np.linspace(-np.pi, np.pi, 201)
        y = np.cos(x)
        self.plot1.plot(x,y, pen='y')

    # Storing data to Dataframe and into a csv:
    def rawdatatocsv(self, rdata, tdata):
        df = pd.DataFrame()
        rdata_col = np.array(rdata)
        tdata_col = np.array(tdata)
        df['Time(s)'] = tdata_col.tolist()
        df['Amplitude(mm)'] = rdata_col.tolist()
        path = 'C:/Users/viswa/FYPS12021/rawdata/'
        now = datetime.now()
        stamp = now.strftime("%d-%m-%Y__%H-%M-%S")
        df.to_csv(rf'{path}rawdata_{stamp}.csv',index= False, header=True)

        
            
            
        
## Add all additional functionality above ##


if __name__ == '__main__':
    app = qtw.QApplication([])
    widget = MainWindow()
    widget.show()
    

    app.exec()