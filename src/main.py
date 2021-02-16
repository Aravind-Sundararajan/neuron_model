from neuron import h, gui

from neuron.units import ms, mV

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

import os

class BallAndStick:
    def __init__(self, gid, window):
        self._gid = gid
        self._setup_morphology()
        self._setup_biophysics()

    def _setup_morphology(self):

        self.soma = h.Section(name='soma', cell=self)
        self.dend = h.Section(name='dend', cell=self)
        self.all = [self.soma, self.dend]
        self.dend.connect(self.soma)
        try:
            self.soma.L = self.soma.diam =  float(window.edit_soma_diameter.text())
            self.dend.L  = float(window.edit_dendrite_length.text())
            self.dend.diam  = float(window.edit_dendrite_diameter.text())
        except:
            self.soma.L = self.soma.diam =  12.6157
            self.dend.L  = 200
            self.dend.diam  = 1

    def _setup_biophysics(self):
        try:
            for sec in self.all:
                sec.Ra = float(window.edit_axial_resistance.text())    # Axial resistance in Ohm * cm
                sec.cm = float(window.edit_membrane_capacitance.text())      # Membrane capacitance in micro Farads / cm^2


            self.soma.insert('hh')



            for seg in self.soma:
                seg.hh.gnabar = float(window.edit_sodium_conductance.text())  # Sodium conductance in S/cm2
                seg.hh.gkbar = float(window.edit_potassium_conductance.text()) # Potassium conductance in S/cm2
                seg.hh.gl = float(window.edit_leak_conductance.text() )   # Leak conductance in S/cm2
                seg.hh.el = float(window.edit_reversal_potential.text())    # Reversal potential in mV

            # Insert passive current in the dendrite
            self.dend.insert('pas')
            for seg in self.dend:
                seg.pas.g = float(window.edit_passive_conductance.text())  # Passive conductance in S/cm2
                seg.pas.e = float(window.edit_leak_reversal_potential.text())    # Leak reversal potential mV
        except:
            for sec in self.all:
                sec.Ra = 100    # Axial resistance in Ohm * cm
                sec.cm = 1      # Membrane capacitance in micro Farads / cm^2
            self.soma.insert('hh')
            for seg in self.soma:
                seg.hh.gnabar = 0.12  # Sodium conductance in S/cm2
                seg.hh.gkbar = 0.036  # Potassium conductance in S/cm2
                seg.hh.gl = 0.0003    # Leak conductance in S/cm2
                seg.hh.el = -54.3     # Reversal potential in mV
            # Insert passive current in the dendrite
            self.dend.insert('pas')
            for seg in self.dend:
                seg.pas.g = 0.001  # Passive conductance in S/cm2
                seg.pas.e = -65    # Leak reversal potential mV


    def __repr__(self):
        return 'BallAndStick[{}]'.format(self._gid)

class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args):
        super().__init__(*args)
        fnameUI  = os.path.join( os.path.dirname(__file__), 'neuronmodel.ui' )
        uic.loadUi(fnameUI, self)
        self.setWindowTitle('NEURON Hodgkin–Huxley model')

    def initModel(self):
            self.cell = BallAndStick(0,self)


    def initFigures(self):

            #Descriptive figures
            self.dendrite_plot_group.layout = QtWidgets.QVBoxLayout()
            self.fig_dend = plt.figure()
            self.ax_dend    = self.fig_dend.add_axes( [0.2, 0.2, 0.7, 0.7] )
            self.canvas_dend = FigureCanvas(self.fig_dend)
            self.dendrite_plot_group.layout.addWidget(self.canvas_dend)
            self.dendrite_plot_group.setLayout(self.dendrite_plot_group.layout)
            self.ax_dend.set_xlabel('t (ms)')
            self.ax_dend.set_ylabel('v (mV)')

            #Statistics figures
            self.soma_plot_group.layout = QtWidgets.QVBoxLayout()
            self.fig_soma = plt.figure()
            self.ax_soma   = self.fig_soma.add_axes([0.2, 0.2, 0.7, 0.7])
            self.canvas_soma = FigureCanvas(self.fig_soma)
            self.soma_plot_group.layout.addWidget(self.canvas_soma)
            self.soma_plot_group.setLayout(self.soma_plot_group.layout)
            self.ax_soma.set_xlabel('t (ms)')
            self.ax_soma.set_ylabel('v (mV)')

    def plot(self):
        stim = h.IClamp(self.cell.dend(1))

        stim.get_segment()

        stim.delay = 5
        stim.dur = 1
        stim.amp = 0.1

        soma_v = h.Vector().record(self.cell.soma(0.5)._ref_v)
        dend_v = h.Vector().record(self.cell.dend(0.5)._ref_v)
        t = h.Vector().record(h._ref_t)
        amps = [0.075 * i for i in range(1, 5)]
        colors = ['green', 'blue', 'red', 'black']
        self.ax_soma.clear()
        self.ax_dend.clear()
        self.ax_dend.set_xlabel('t (ms)')
        self.ax_dend.set_ylabel('v (mV)')
        self.ax_soma.set_xlabel('t (ms)')
        self.ax_soma.set_ylabel('v (mV)')
        try:
            for amp, color in zip(amps, colors):
                stim.amp = amp

                h.finitialize(-65 * mV)

                h.continuerun(25 * ms)

                self.canvas_dend.draw()
                self.ax_dend.plot(t, dend_v,color)

                self.canvas_soma.draw()
                self.ax_soma.plot(t, soma_v,color)

            self.ax_dend.legend(["{:.2f} mV".format(elem) for elem in amps])
        except:
            self.ax_soma.clear()
            self.ax_dend.clear()

    def updateModel(self):
        self.initModel()
        self.plot()


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.setGeometry(400, 400, 800, 560)

    window.show()

    window.initFigures()

    window.initModel()

    window.plot()

    window.edit_soma_diameter.textChanged.connect(window.updateModel)
    window.edit_dendrite_length.textChanged.connect(window.updateModel)
    window.edit_dendrite_diameter.textChanged.connect(window.updateModel)
    window.edit_axial_resistance.textChanged.connect(window.updateModel)
    window.edit_membrane_capacitance.textChanged.connect(window.updateModel)
    window.edit_sodium_conductance.textChanged.connect(window.updateModel)
    window.edit_potassium_conductance.textChanged.connect(window.updateModel)
    window.edit_leak_conductance.textChanged.connect(window.updateModel)
    window.edit_reversal_potential.textChanged.connect(window.updateModel)
    window.edit_passive_conductance.textChanged.connect(window.updateModel)
    window.edit_leak_reversal_potential.textChanged.connect(window.updateModel)


    sys.exit(app.exec_())
