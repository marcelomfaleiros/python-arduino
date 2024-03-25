# encoding: utf-8

import sys
from PyQt5.QtWidgets import *
import numpy as np
from scipy.interpolate import interp1d
import pyqtgraph as pg
import matplotlib.pyplot as plt
import visa
from pyvisa.constants import StopBits, Parity
import os
import time
import keyboard

def plot(x, y):
   dia = str(time.strftime("%c"))
   titulo = edgraph.text() + "\n" + dia            
   plt.title(titulo)
   plt.xlabel("Voltage (V)")
   plt.ylabel("Current (A)")
   plt.grid(linestyle="--")
   plt.plot(x, y)
    
def save_setup(x, y):
   script_dir = os.path.dirname(__file__)
   results_dir = os.path.join(script_dir, "Results/")
   if not os.path.isdir(results_dir):
       os.makedirs(results_dir)
   dispsave = edgraph.get() + ".txt"
   f = open(results_dir + dispsave, "w")
   for i in range(len(x)):
       f.write("%.2f %.12f\n" % (x[i], y[i]))
   f.close()
   picture = edgraph.text() + ".png"   
   plt.savefig(results_dir + picture)
   plt.close()
   
def arduino_comm(x):
   arduino.write(x)

def keithley_reset():
   keithley.write("smua.reset()")

def keithley_off():
   keithley.write("smua.source.output = smua.OUTPUT_OFF")
   keithley.write("smua.source.levelv = 0")

def keithley_setup():
   keithley_reset()   
   keithley.write("smua.source.func = smua.OUTPUT_DCVOLTS")
   keithley.write("display.smua.measure.func = ")
   keithley.write("smua.measure.autorangei = 1")
   keithley.write("smua.measure.autozero = smua.AUTOZERO_AUTO")
   Ilimit = edIlimit.text()
   keithley.write("smua.source.limiti = " + Ilimit)
   tdelay = edtdelay.text()
   keithley.write("smua.measure.delay = " + tdelay)

def keithley_setV():
   setV = edsetV.text()
   if float(setV) > 0:
      keithley.write("smua.source.levelv = " + setV)
      keithley.write("smua.source.output = smua.OUTPUT_ON")
   elif float(setV) == 0:
      keithley.write("smua.source.output = smua.OUTPUT_OFF")
      keithley.write("smua.source.levelv = 0")

def meas_IV():
   x = []
   y = []
   sVi = edVstart.text()
   Vi = float(sVi)
   sVf = edVstop.text()  
   Vf = float(sVf)
   Vstep = float(edVstep.text())
   stdelay = edtdelay.text()
   tdelay = float(stdelay)
   keithley_setup()     
   keithley.write("smua.source.levelv = " + sVi)
   keithley.write("smua.source.output = smua.OUTPUT_ON")
   pw = pg.plot(title="JxV curve")   
   while (Vi <= Vf):
      if keyboard.is_pressed("Escape"):
            break
      meas = keithley.query("print(smua.measure.i())")  
      x.append(Vi)             
      y.append(float(meas))
      pw.plot(x, y , pen = 'y', clear = False)                               
      pg.QtGui.QApplication.processEvents()
      time.sleep(.1)    
      Vi += Vstep      
      keithley.write("smua.source.levelv = " + str(Vi))
   plot(x, y)
   save_setup(x, y)
   arduino_comm("100")
   keithley_reset()
      
def meas_V():   
   x = []
   y = []
   sV = edVconst.text()
   V = float(sV)
   st_step = edtime.text()
   ti = 0
   t_step = float(st_step)
   st_range = edtrange.text()
   t_range = float(edtrange.text())
   keithley_setup()      
   keithley.write("smua.source.levelv = " + sV)
   keithley.write("smua.source.output = smua.OUTPUT_ON")
   pw = pg.plot(title="JxV curve")     
   while (ti <= t_range):
      if keyboard.is_pressed("Escape"):
            break
      meas = keithley.query("print(smua.measure.i())")            
      x.append(ti)
      y.append(float(meas))
      pw.plot(x, y , pen = 'y', clear = False)                               
      pg.QtGui.QApplication.processEvents()
      ti += t_step      
      time.sleep(t_step)         
   plot(x, y)
   save_setup(x, y)
   arduino_comm("100")
   keithley_reset()   

def close():
   arduino_comm("100")
   keithley_reset()   
   pg.close()
   pg.win.close()
   janela.destroy()
app = QApplication(sys.argv)

w = QWidget()
w.setGeometry(10, 50, 280, 540)
w.setWindowTitle('IV / It curve')

rm = visa.ResourceManager()
#keithley = rm.open_resource("GPIB0::26")
#arduino = rm.open_resource("COM3", baud_rate = 9600)

btVxt = QPushButton('Reset Keithley', w)
btVxt.move(50, 20)
btVxt.clicked.connect(keithley_reset)

btclose = QPushButton('Close window', w)
btclose.move(150, 20)
btclose.clicked.connect(close)

btD1 = QPushButton('D1', w)
btD1.move(20, 80)
btD1.clicked.connect(lambda: arduino_comm("1"))         
btD2 = QPushButton('D2', w)
btD2.move(20, 110)
btD2.clicked.connect(lambda: arduino_comm("2"))
btD3 = QPushButton('D3', w)
btD3.move(100, 80)
btD3.clicked.connect(lambda: arduino_comm("3"))
btD4 = QPushButton('D4', w)
btD4.move(100, 110)
btD4.clicked.connect(lambda: arduino_comm("4"))
btD1 = QPushButton('D1', w)
btD1.move(20, 80)
btDoff = QPushButton('Devices OFF', w)
btDoff.move(180, 95)
btDoff.clicked.connect(lambda: arduino_comm("100"))

edIlimit = QLineEdit(w)
edIlimit.move(20, 160)
lIlimit = QLabel('I limit', w)
lIlimit.move(140, 162)

btIV = QPushButton('I x V', w)
btIV.move(20, 200)
btIV.clicked.connect(meas_IV)

edVstart = QLineEdit(w)
edVstart.move(20, 230)
lVstart = QLabel('V start', w)
lVstart.move(140, 232)

edVstop = QLineEdit(w)
edVstop.move(20, 250)
lVstop = QLabel('V stop', w)
lVstop.move(140, 252)

edVstep = QLineEdit(w)
edVstep.move(20, 270)
lVstep = QLabel('V step', w)
lVstep.move(140, 272)

edtdelay = QLineEdit(w)
edtdelay.move(20, 290)
ltdelay = QLabel('Time delay', w)
ltdelay.move(140, 292)

btIV = QPushButton('Const. V', w)
btIV.move(20, 320)
btIV.clicked.connect(meas_V)

edVconst = QLineEdit(w)
edVconst.move(20, 350)
lVconst = QLabel('V', w)
lVconst.move(140, 352)

edtime = QLineEdit(w)
edtime.move(20, 370)
lVtime = QLabel('time step', w)
lVtime.move(140, 372)

edtrange = QLineEdit(w)
edtrange.move(20, 390)
ltrange = QLabel('time range', w)
ltrange.move(140, 392)

lgraph = QLabel('(Press ESC to stop measuring, data will be saved)', w)
lgraph.move(20, 425)

btsetV = QPushButton('Set Keithley voltage', w)
btsetV.move(20, 450)
btsetV.clicked.connect(keithley_setV)
edsetV = QLineEdit(w)
edsetV.move(140, 452)

edgraph = QLineEdit(w)
edgraph.move(20, 490)
lgraph = QLabel('Plot/Data title', w)
lgraph.move(140, 492)

w.show()

sys.exit(app.exec_())
