# encoding: utf-8

import sys
from PyQt5.QtWidgets import *
import numpy as np
from scipy.interpolate import interp1d
import pyqtgraph as pg
import matplotlib.pyplot as plt
import pyfirmata
from pyfirmata import Arduino, util
import visa
from pyvisa.constants import StopBits, Parity
import os
import time
import keyboard
from functools import partial

def save_plot(x, y):
   dia = str(time.strftime("%c"))
   titulo = edgraph.text() + "\n" + dia   
   plt.title(titulo)
   plt.xlabel("Voltage (V)")
   plt.ylabel("Current Density (mA/cm2)")
   plt.grid(linestyle="--")   
   plt.plot(x, y)
   #plt.show()

def save_setup(x, y, z, effc_up, effv_up, effc_down, effv_down):
   script_dir = os.path.dirname(__file__)
   results_dir = os.path.join(script_dir, "Results/")
   if not os.path.isdir(results_dir):
       os.makedirs(results_dir)
   dispsave = edgraph.text() + ".txt"
   device = edgraph.text() + ' data' + ".txt"
   f = open(results_dir + dispsave, "w")
   for i in range(len(x)):
       f.write("%.2f %.12f %.12f\n" % (x[i], y[i], z[i]))      
   f.close()
   g = open(results_dir + device, "w")
   g.write('Uphill efficiency\n\n')
   for j in range(len(effv_up)):        
      g.write("%.7s %.5f\n\n" % (effc_up[j], effv_up[j]))
   g.write('\n\n')
   g.write('Downhill efficiency\n\n')
   for h in range(len(effv_down)):
        g.write("%.9s %.5f\n\n" % (effc_down[h], effv_down[h]))    
   g.close()
   picture = dispsave + ".png"   
   plt.savefig(results_dir + picture)   
   plt.close()
   
def arduino_comm(x):
   if x == 100:
      for j in [2, 4, 6, 8]:
         arduino.digital[j].write(1)
   else:
      for i in [2, 4, 6, 8]:
         arduino.digital[i].write(1)
      arduino.digital[x].write(0)
   

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

def meas():   
   xup = []
   yup = []
   zup = []
   xdown = []
   ydown = []
   zdown = []
   sds = edds.text()
   ds = float(sds)
   sVi = edVstart.text()
   Vi = float(sVi)
   sVf = edVstop.text()  
   Vf = float(sVf)
   Vstep = float(edVstep.text())
   arrayV = np.arange(start=Vi, stop=Vf+Vstep, step=Vstep)
   xV = np.around(arrayV,3)       
   keithley_setup()         
   keithley.write(":OUTP ON")
   pw = pg.plot(title="JxV curve")
   for V in xV:
      if keyboard.is_pressed('Escape'):
         break
      keithley.write(":SOUR:VOLT:LEV " + str(V))
      meas = keithley.query(":MEAS?")
      curr = float(meas)
      currdens = -1*curr*1000/ds
      xup.append(V)       
      yup.append(currdens)
      zup.append(curr)
      pw.plot(xup, yup, pen = 'y', clear = False)
      pg.QtGui.QApplication.processEvents()
   sdtordelay = eddtordelay.text()
   dtordelay = int(sdtordelay)
   time.sleep(dtordelay)
   for V in xV[::-1]:
      if keyboard.is_pressed('Escape'):
         break
      keithley.write(":SOUR:VOLT:LEV " + str(V))
      meas = keithley.query(":MEAS?")
      curr = float(meas)
      currdens = -1*curr*1000/ds
      xdown.append(V)       
      ydown.append(currdens)
      zdown.append(curr)
      pw.plot(xdown, ydown, pen = 'y', clear = False)
      pg.QtGui.QApplication.processEvents()
   
   return xup, yup, xdown, ydown, zup, zdown
                                          
def calc_efficiency(xup, yup, xdown, ydown):   
   Pluz = 100

   xup = np.array(xup)
   yup = np.array(yup)      
   power_up = [i*j for i,j in zip(xup,yup)]   
   max_power_up_index = power_up.index(max(power_up))   
   xmp_up = xup[max_power_up_index]
   ymp_up = yup[max_power_up_index]   
   P_up = xmp_up*ymp_up
   indV0_up = np.where(xup == 0.0)
   Jsc_up = yup[indV0_up[0][0]]
   lbJscfr.setText(str(Jsc_up))
   for i in range(4):
        ypos_up = [j for j in yup if j > 0]
        yneg_up = [k for k in yup if k < 0]
        arry_up = [yneg_up[len(yneg_up)-2], yneg_up[len(yneg_up)-1], ypos_up[0], ypos_up[1]]
        arrx_up = []
        for i in arry_up:
           for j in range(len(yup)):
               if i == yup[j]:
                  arrx_up.append(xup[j])
        xup = np.linspace(arrx_up[0], arrx_up[-1], num=1000, endpoint=True)
        f_up = interp1d(arrx_up, arry_up)
        yup = f_up(xup)
        indy_up = np.where(ypos_up == min(ypos_up))
        Voc_up = xup[indy_up[0][0]]
   lbVocfr.setText(str(Voc_up))
   FF_up = P_up/(Voc_up*Jsc_up)
   Eff_up = (Jsc_up*Voc_up*FF_up/Pluz)*100
   lbFFfr.setText(str(FF_up))
   lbEfffr.setText(str(Eff_up))
   headerup = ['Jsc_up', 'Voc_up', 'FF_up', 'Eff_up']
   valuesup = [Jsc_up, Voc_up, FF_up, Eff_up]
             
   xdown = np.array(xdown)
   ydown = np.array(ydown)
   power_down = [i*j for i,j in zip(xdown,ydown)]   
   max_power_down_index = power_down.index(max(power_down))   
   xmp_down = xdown[max_power_down_index]
   ymp_down = ydown[max_power_down_index]   
   P_down = xmp_down*ymp_down   
   indV0_down = np.where(xdown == 0.0)    
   Jsc_down = ydown[indV0_down[0][0]]
   lbJscbr.setText(str(Jsc_down))     
   for i in range(4):
        ypos_down = [j for j in ydown if j > 0]
        yneg_down = [k for k in ydown if k < 0]
        arry_down = [yneg_down[len(yneg_down)-2], yneg_down[len(yneg_down)-1], ypos_down[0], ypos_down[1]]
        arrx_down = []
        for i in arry_down:
           for j in range(len(ydown)):
               if i == ydown[j]:
                  arrx_down.append(xdown[j])
        xdown = np.linspace(arrx_down[0], arrx_down[-1], num=1000, endpoint=True)
        f_down = interp1d(arrx_down, arry_down)
        ydown = f_down(xdown)
        indy_down = np.where(ypos_down == min(ypos_down))
        Voc_down = xdown[indy_down[0][0]]
   lbVocbr.setText(str(Voc_down))   
   FF_down = P_down/(Voc_down*Jsc_down)
   Eff_down = (Jsc_down*Voc_down*FF_down/Pluz)*100
   lbFFbr.setText(str(FF_down))
   lbEffbr.setText(str(Eff_down))
   headerdown = ['Jsc_down', 'Voc_down', 'FF_down', 'Eff_down']
   valuesdown = [Jsc_down, Voc_down, FF_down, Eff_down]
   
   return headerup, valuesup, headerdown, valuesdown

def trigger():
   measurement = meas()   
   xup = measurement[0] 
   yup = measurement[1] 
   xdown = measurement[2]
   ydown = measurement[3]
   zup = measurement[4] 
   zdown = measurement[5]   
   eff = calc_efficiency(xup, yup, xdown, ydown)   
   effc_up = eff[0]
   effv_up = eff[1]
   effc_down = eff[2]
   effv_down = eff[3]
   x = xup + xdown
   y = yup + ydown
   z = zup + zdown
   print(z)
   save_plot(x, y)         
   save_setup(x, y, z, effc_up, effv_up, effc_down, effv_down) 
       
   arduino_comm("100")
   keithley_reset()

def close():
   arduino_comm(100)
   keithley_reset()   
   pg.close()
   pg.win.close()
   janela.destroy()
           
app = QApplication(sys.argv)

w = QWidget()
w.setGeometry(10, 50, 280, 780)
w.setWindowTitle('JV curve')

rm = visa.ResourceManager()
keithley = rm.open_resource("COM5", baud_rate=9600, data_bits=8, parity=Parity.none, stop_bits=StopBits.one)
arduino = pyfirmata.Arduino('COM4')
for i in (2, 4, 6, 8):
   arduino.digital[i].write(1)

btVxt = QPushButton('Reset Keithley', w)
btVxt.move(50, 20)
btVxt.clicked.connect(keithley_reset)

btclose = QPushButton('Close window', w)
btclose.move(150, 20)
btclose.clicked.connect(close)

btD1 = QPushButton('D1', w)
btD1.move(20, 80)
btD1.clicked.connect(partial(arduino_comm, 2))         
btD2 = QPushButton('D2', w)
btD2.move(20, 110)
btD2.clicked.connect(partial(arduino_comm, 4))
btD3 = QPushButton('D3', w)
btD3.move(100, 80)
btD3.clicked.connect(partial(arduino_comm, 6))
btD4 = QPushButton('D4', w)
btD4.move(100, 110)
btD4.clicked.connect(partial(arduino_comm, 8))
btDoff = QPushButton('Devices OFF', w)
btDoff.move(180, 95)
btDoff.clicked.connect(partial(arduino_comm, 100))

edds = QLineEdit(w)
edds.move(20, 150)
lds = QLabel('Device surface (cm2)', w)
lds.move(140, 152)

edIlimit = QLineEdit(w)
edIlimit.move(20, 180)
lIlimit = QLabel('I limit (A)', w)
lIlimit.move(140, 182)

btIV = QPushButton('I x V', w)
btIV.move(20, 210)
btIV.clicked.connect(trigger)

edVstart = QLineEdit(w)
edVstart.move(20, 248)
lVstart = QLabel('V start (V)', w)
lVstart.move(140, 250)

edVstop = QLineEdit(w)
edVstop.move(20, 270)
lVstop = QLabel('V stop (V)', w)
lVstop.move(140, 272)

edVstep = QLineEdit(w)
edVstep.move(20, 292)
lVstep = QLabel('V step (V)', w)
lVstep.move(140, 294)

edtdelay = QLineEdit(w)
edtdelay.move(20, 330)
ltdelay = QLabel('Time delay (s)', w)
ltdelay.move(140, 332)

btsetV = QPushButton('Set Keithley voltage', w)
btsetV.move(20, 370)
btsetV.clicked.connect(keithley_setV)
edsetV = QLineEdit(w)
edsetV.move(140, 372)

edgraph = QLineEdit(w)
edgraph.move(20, 410)
lgraph = QLabel('Plot/Data title', w)
lgraph.move(140, 412)

eddtordelay = QLineEdit(w)
eddtordelay.move(20, 450)
ldtordelay = QLabel('Direct-to-Reverse delay (s)', w)
ldtordelay.move(140, 452)

lstop = QLabel('(Press ESC to stop measuring, data will be saved)', w)
lstop.move(20, 480)

lbJscf = QLabel('Jsc (Up): ', w)
lbJscf.move(20, 520)
lbJscfr = QLabel('X                                             ', w)
lbJscfr.move(120, 520)

lbVocf = QLabel('Voc (Up): ', w)
lbVocf.move(20, 550)
lbVocfr = QLabel('X                                             ', w)
lbVocfr.move(120, 550)    
    
lbFFf = QLabel('FF (Up): ', w)
lbFFf.move(20, 580)
lbFFfr = QLabel('X                                              ', w)
lbFFfr.move(120, 580)    
    
lbEfff = QLabel('Eff (Up): ', w)
lbEfff.move(20, 610)
lbEfffr = QLabel('X                                             ', w)
lbEfffr.move(120, 610)

lbJscb = QLabel('Jsc (Down): ', w)
lbJscb.move(20, 640)
lbJscbr = QLabel('X                                              ', w)
lbJscbr.move(120, 640)

lbVocb = QLabel('Voc (Down): ', w)
lbVocb.move(20, 670)
lbVocbr = QLabel('X                                              ', w)
lbVocbr.move(120, 670)

lbFFb = QLabel('FF (Down): ', w)
lbFFb.move(20, 700)
lbFFbr = QLabel('X                                               ', w)
lbFFbr.move(120, 700)

lbEffb = QLabel('Eff (Down): ', w)
lbEffb.move(20, 730)
lbEffbr = QLabel('X                                              ', w)
lbEffbr.move(120, 730)

w.show()

sys.exit(app.exec_())
