from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
QVBoxLayout, QWidget, QFileDialog, QInputDialog)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt
import csv
import pandas as pd
import spm1d
class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.originalPalette = QApplication.palette()
        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox)

        self.useStylePaletteCheckBox = QCheckBox("&Use style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)

        disableWidgetsCheckBox = QCheckBox("&Disable widgets")

        self.createButtons()
        self.createButtons2()
        self.createPlotCanvas()
        self.createSpreadsheet()

        mainLayout = QGridLayout()



        mainLayout.addWidget(self.buttonGroup, 0, 0)
        mainLayout.addWidget(self.buttonGroup2, 0, 1)
        mainLayout.addWidget(self.leftGroup, 1, 1)
        mainLayout.addWidget(self.rightGroup, 1, 0)
        self.setLayout(mainLayout)

        self.setWindowTitle("jikuGUI")

    def createButtons(self):
        self.buttonGroup = QGroupBox("")
        #self.buttonGroup.setFlat(True);
        #self.buttonGroup.setStyleSheet("border:0;")
        self.buttonGroup.setGeometry(0, 0, 100, 40)
        layout = QHBoxLayout()

        self.pushButtonLoad = QtWidgets.QPushButton(self)
        self.pushButtonLoad.setText("Load Data")
        self.pushButtonLoad.clicked.connect(self.on_pushButtonLoad_clicked)
        layout.addWidget(self.pushButtonLoad)

        self.pushButtonWrite = QtWidgets.QPushButton(self)
        self.pushButtonWrite.setText("Save Data")
        self.pushButtonWrite.clicked.connect(self.on_pushButtonWrite_clicked)
        layout.addWidget(self.pushButtonWrite)

        self.pushButtonWriteAnalysis = QtWidgets.QPushButton(self)
        self.pushButtonWriteAnalysis.setText("Save Analysis")
        #self.pushButtonWrite.clicked.connect(self.on_pushButtonWrite_clicked)
        layout.addWidget(self.pushButtonWriteAnalysis)

        self.buttonGroup.setLayout(layout)

    def createButtons2(self):
        self.buttonGroup2 = QGroupBox("")
        #self.buttonGroup.setFlat(True);
        #self.buttonGroup.setStyleSheet("border:0;")
        self.buttonGroup2.setGeometry(0, 0, 100, 40)
        layout = QHBoxLayout()

        self.pushButtonPlot = QtWidgets.QPushButton(self)
        self.pushButtonPlot.setText("Plot")
        self.pushButtonPlot.clicked.connect(self.on_pushButtonPlot_clicked)

        self.pushButtonAnalysis = QtWidgets.QPushButton(self)
        self.pushButtonAnalysis.setText("Analyze")
        self.pushButtonAnalysis.clicked.connect(self.on_pushButtonAnalysis_clicked)

        layout.addWidget(self.pushButtonPlot)
        layout.addWidget(self.pushButtonAnalysis)

        self.buttonGroup2.setLayout(layout)

    def createSpreadsheet(self):
        self.rightGroup = QGroupBox("Data")
        self.tabs = QTabWidget()
        self.tableWidget = QTableWidget(10, 10)
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        self.rightGroup.setLayout(layout)

    def createPlotCanvas(self):
        self.leftGroup = QGroupBox("Statistics")
        self.tabs = QTabWidget()

        #tab1- matplotlib
        self.tab1 = QWidget()
        self.tab1.layout = QVBoxLayout(self)

        #tab2- matplotlib
        self.tab2 = QWidget()
        self.tab2.layout = QVBoxLayout(self)

        #tab3- matplotlib
        self.tab3 = QWidget()
        self.tab3.layout = QVBoxLayout(self)

        #tab3- matplotlib
        self.tab4 = QWidget()
        self.tab4.layout = QVBoxLayout(self)

        self.tabs.addTab(self.tab1,"Plot")
        self.tabs.addTab(self.tab2,"Analysis")
        self.tabs.addTab(self.tab3,"Advanced")
        self.tabs.addTab(self.tab4,"Wizard")


        layout = QVBoxLayout()
        # a figure instance to plot on


        self.figure1 = plt.figure()
        self.ax1     = self.figure1.add_axes( [0.1, 0.1, 0.8, 0.8] )
        self.canvas1 = FigureCanvas(self.figure1)

        self.figure2 = plt.figure()
        self.ax2     = self.figure2.add_axes( [0.1, 0.1, 0.8, 0.8] )
        self.canvas2 = FigureCanvas(self.figure2)

        self.dialog = QLineEdit(self)
        self.pushButtonRun = QtWidgets.QPushButton(self)
        self.pushButtonRun.setText("run")
        self.pushButtonRun.clicked.connect(self.on_pushButtonRun_clicked)

        self.tab1.layout.addWidget(self.canvas1)

        self.tab2.layout.addWidget(self.canvas2)

        self.tab3.layout.addWidget(self.dialog)
        self.tab3.layout.addWidget(self.pushButtonRun)

        self.tab1.setLayout(self.tab1.layout)
        self.tab2.setLayout(self.tab2.layout)
        self.tab3.setLayout(self.tab3.layout)

        layout.addWidget(self.tabs)
        self.leftGroup.setLayout(layout)

    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter text:')
        if ok:
                self.le.setText(str(text))

    def plot(self):
        try:
            ids = list(set(index.row() for index in self.tableWidget.selectedIndexes()))
            print(ids)
            print(self.model[ids,:].transpose())
            self.ax1.clear()
            self.ax1.plot(self.model[ids,:].transpose())
            self.canvas1.draw()
        except:
            self.ax1.clear()

    def parser(self):
        print("OK")

    def analysis(self):
        try:
            ids = list(set(index.row() for index in self.tableWidget.selectedIndexes()))
            print(ids)
            print(self.model[ids,:].transpose())
            t  = spm1d.stats.ttest(self.model[ids,:])
            ti = t.inference(alpha=0.05, two_tailed=False, interp=True)
            self.ax2.clear()
            self.ax2.plot()
            ti.plot()
            self.canvas2.draw()
        except:
            self.ax2.clear()

    def loadCsv(self):

        fileName = QFileDialog.getOpenFileName(self, 'Open file',
             './',"spreadsheets (*.xlsx *.csv)")
        print(fileName)
        df=pd.read_csv(fileName[0], sep=',',header=None)
        self.model = df.values
        print(self.model)
        print(self.model.shape)
        nrows = self.model.shape[0]
        ncols = self.model.shape[1]
        if (self.tableWidget.rowCount() != nrows):
            self.tableWidget.setRowCount(nrows)
        if (self.tableWidget.columnCount() != nrows):
            self.tableWidget.setColumnCount(ncols)
        for m in range(nrows):
                for n in range(ncols):
                    newitem = QtWidgets.QTableWidgetItem(str(self.model[m,n]))
                    self.tableWidget.setItem(m, n, newitem)

    def writeCsv(self):
        fileName = QFileDialog.getOpenFileName(self, 'save file',
             'c:\\',"Image files (*.xlsx *.csv)")
        with open(fileName[0], "w") as fileOutput:
            writer = csv.writer(fileOutput)
            for rowNumber in range(self.model.rowCount()):
                fields = [
                    self.model.data(
                        self.model.index(rowNumber, columnNumber),
                        QtCore.Qt.DisplayRole
                    )
                    for columnNumber in range(self.model.columnCount())
                ]
                writer.writerow(fields)

    @QtCore.pyqtSlot()
    def on_pushButtonWrite_clicked(self):
        self.writeCsv()

    @QtCore.pyqtSlot()
    def on_pushButtonLoad_clicked(self):
        self.loadCsv()

    @QtCore.pyqtSlot()
    def on_pushButtonPlot_clicked(self):
        self.plot()

    @QtCore.pyqtSlot()
    def on_pushButtonAnalysis_clicked(self):
        self.analysis()

    @QtCore.pyqtSlot()
    def on_pushButtonRun_clicked(self):
        self.Parser()
if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.setGeometry(400, 400, 1200, 600)
    gallery.show()
    sys.exit(app.exec_())
