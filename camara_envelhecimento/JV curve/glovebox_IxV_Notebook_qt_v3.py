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
   plt.ylabel("Current Density (mA/cm2)")
   plt.grid(linestyle="--")
   plt.plot(x, y)

def save_setup(x, y, z):
   script_dir = os.path.dirname(__file__)
   results_dir = os.path.join(script_dir, "Results/")
   if not os.path.isdir(results_dir):
       os.makedirs(results_dir)
   dispsave = edgraph.text() + ".txt"
   f = open(results_dir + dispsave, "w")
   for i in range(len(x)):
       f.write("%.2f %.12f\n" % (x[i], y[i], y[i]))
   f.write(eff_subida+'\n')   
   f.write(eff_descida)
   f.close()
   picture = edgraph.text() + ".png"   
   plt.savefig(results_dir + picture)
   plt.close()
   
def arduino_comm(x):
   arduino.write(x)

def keithley_reset():
   keithley.write("*RST")

def keithley_off():
   keithley.write(":OUTP OFF")
   keithley.write(":SOUR:VOLT:LEV 0")
    
def keithley_setup():
   keithley.write("*RST")   
   keithley.write(":SOUR:FUNC VOLT")   
   keithley.write(":SOUR:VOLT:RANG:AUTO 1")
   keithley.write(":SENS:FUNC 'CURR:DC' ")
   keithley.write(":SENS:CURR:RANG:AUTO 1")
   keithley.write(":FORM:ELEM CURR")
   Ilimit = edIlimit.text()
   keithley.write(":SENS:CURR:PROT " + Ilimit)
   tdelay = edtdelay.text()
   keithley.write(":SOUR:DEL " + tdelay)

def keithley_setV():
    keithley_setup()    
    setV = edsetV.text()
    if float(setV) > 0:
       keithley.write(":SOUR:VOLT:MODE FIXED")
       keithley.write(":SOUR:VOLT:RANG:AUTO 1")
       keithley.write(":SOUR:VOLT:LEV " + setV)
       keithley.write(":SENS:CURR:PROT 1")
       keithley.write(":OUTP ON")
    elif float(setV) == 0:
       keithley.write(":OUTP OFF")
       keithley.write(":SOUR:VOLT:LEV 0")

def calc_efficiency(x, y):
   header = ["Jsc", "Voc", "FF", "Eff"]
   curdensity = -1*(y*1000/0.12)
   Pluz = 100  
   power = [i*j for i,j in zip(x,curdensity)]
   max_power_index = power.index(max(power))
   xmp = x[max_power_index]
   ymp = curdensity[max_power_index]
   P = xmp*ymp
   indV0 = np.where(x == 0.0)
   Jsc = curdensity[indV0[0][0]]

   xv = x
   yv = y

   for i in range(4):
        ypos = [j for j in yv if j > 0]
        yneg = [k for k in yv if k < 0]
        arry = [yneg[len(yneg)-2], yneg[len(yneg)-1], ypos[0], ypos[1]]
        arrx = []        
        for i in arry:
                for j in range(len(yv)):
                        if i == yv[j]:
                                arrx.append(xv[j]) 
        xv = np.linspace(arrx[0], arrx[-1], num=1000, endpoint=True)
        f = interp1d(arrx, arry)
        yv = f(xv)
        indy = np.where(ypos == min(ypos))
        Voc = xv[indy[0][0]]
  
   FF = P/(Voc*Jsc)
   Eff = (Jsc*Voc*FF/Pluz)*100

   return header, Voc, Jsc, FF, Eff, power  

def meas():
    x = []
    y = []
    z = []
    sVi = edVstart.text()
    Vi = float(sVi)
    sVf = edVstop.text()  
    Vf = float(sVf)
    Vstep = float(edVstep.text())
    arrayV = np.arange(start=Vi, stop=Vf+Vstep, step=Vstep)
    xV = np.around(arrayV,3)
    stdelay = edtdelay.text()
    tdelay = float(stdelay)
    keithley_setup()         
    keithley.write(":OUTP ON")
    pw = pg.plot(title="JxV curve")      
    for V in xV:
        if keyboard.is_pressed('Escape'):
           jump = True
           break
        keithley.write(":SOUR:VOLT:LEV " + str(V))
        meas = keithley.query(":MEAS?")
        curr = float(meas)*1000/0.12
        x.append(V)             
        y.append(curr)
        z.append(V*curr)
        pw.plot(x, np.negative(y) , pen = 'y', clear = False)                               
        pg.QtGui.QApplication.processEvents()
        time.sleep(.1)    
    eff_up = str(calc_efficiency(x, y))        
    lbJscfr = QLabel(str(eff_up[2]), w)
    lbJscfr.move(60, 460)   
    lbVocfr = QLabel(str(eff_up[1]), w)
    lbVocfr.move(60, 490)
    lbFFfr = QLabel(str(eff_up[3]), w)
    lbFFfr.move(60, 520)
    lbEfffr = QLabel(str(eff_up[4]), w)
    lbEfffr.move(60, 550)
    
    time.sleep(3)
    
    if jump == False:
       for j in xV[::-1]:
           if keyboard.is_pressed('Escape'):
              break
           keithley.write(":SOUR:VOLT:LEV " + str(V))
           meas = keithley.query(":MEAS?")
           curr = (-1)*float(meas)*1000/0.12
           x.append(V)        
           y.append(curr)
           pw.plot(x, y, pen = 'y', clear = False)                                
           pg.QtGui.QApplication.processEvents()             
       eff_down = str(calc_efficiency(x, y))
       lbJscb = QLabel(str(eff_up[2]), w)
       lbJscb.move(20, 580)   
       lbVocb = QLabel(str(eff_up[1]), w)
       lbVocb.move(20, 610)
       lbFFb = QLabel(str(eff_up[3]), w)
       lbFFb.move(20, 640)
       lbEffb = QLabel(str(eff_up[4]), w)
       lbEffb.move(20, 670)
    
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
w.setGeometry(10, 50, 280, 750)
w.setWindowTitle('JV curve')

#rm = visa.ResourceManager()
#keithley = rm.open_resource("COM5", baud_rate=9600, data_bits=8, parity=Parity.none, stop_bits=StopBits.one)
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
btDoff = QPushButton('Devices OFF', w)
btDoff.move(180, 95)
btDoff.clicked.connect(lambda: arduino_comm("100"))

edIlimit = QLineEdit(w)
edIlimit.move(20, 160)
lIlimit = QLabel('I limit', w)
lIlimit.move(140, 162)

btIV = QPushButton('I x V', w)
btIV.move(20, 200)
btIV.clicked.connect(meas)

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

btsetV = QPushButton('Set Keithley voltage', w)
btsetV.move(20, 330)
btsetV.clicked.connect(keithley_setV)
edsetV = QLineEdit(w)
edsetV.move(140, 332)

edgraph = QLineEdit(w)
edgraph.move(20, 370)
lgraph = QLabel('Plot/Data title', w)
lgraph.move(140, 372)

lgraph = QLabel('(Press ESC to stop measuring, data will be saved)', w)
lgraph.move(20, 410)

lbJscf = QLabel('Jsc (Up): ', w)
lbJscf.move(20, 460)   
lbVocf = QLabel('Voc (Up): ', w)
lbVocf.move(20, 490)
lbFFf = QLabel('FF (Up): ', w)
lbFFf.move(20, 520)
lbEfff = QLabel('Eff (Up): ', w)
lbEfff.move(20, 550)

lbJscb = QLabel('Jsc (Down): ', w)
lbJscb.move(20, 580)   
lbVocb = QLabel('Voc (Down): ', w)
lbVocb.move(20, 610)
lbFFb = QLabel('FF (Down): ', w)
lbFFb.move(20, 640)
lbEffb = QLabel('Eff (Down): ', w)
lbEffb.move(20, 670)

w.show()

sys.exit(app.exec_())
