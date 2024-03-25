# encoding: utf-8

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from functools import partial
import visa
import os
import time
import keyboard
   

def arduino_comm(x):
   arduino.write(x)

def keithley_setV():
   setV = edsetV.get()
   if float(setV) > 0:
      keithley.write("smua.source.levelv = " + setV)
      keithley.write("smua.source.output = smua.OUTPUT_ON")
   elif float(setV) == 0:
      keithley_off()

def keithley_setup():
   keithley_reset()   
   keithley.write("smua.source.func = smua.OUTPUT_DCVOLTS")
   keithley.write("smua.measure.autorangei = 1")
   keithley.write("smua.measure.autozero = smua.AUTOZERO_AUTO")
   Ilimit = edIlimit.get()
   keithley.write("smua.source.limiti = " + Ilimit)
   tdelay = edtdelay.get()
   keithley.write("smua.measure.delay = " + tdelay)

def keithley_reset():
   keithley.write("smua.reset()")

def keithley_off():
   keithley.write("smua.source.output = smua.OUTPUT_OFF")
   keithley.write("smua.source.levelv = 0")

def plot_setup():
   dia = str(time.strftime("%c"))
   titulo = edgraph.get() + "\n" + dia
   a.clear()
   a.set_title(titulo)
   a.set_xlabel("Voltage (V)")
   a.set_ylabel("Current (A)")
   a.grid(linestyle="--")

def save_setup(x, y):
   script_dir = os.path.dirname(__file__)
   results_dir = os.path.join(script_dir, "Results/")
   if not os.path.isdir(results_dir):
       os.makedirs(results_dir)
   dispsave = edgraph.get() + ".txt"
   f = open(results_dir + dispsave, "w")
   for i in range(len(x)):
       f.write("%.2f %.6f\n" % (x[i], y[i]))
   f.close()
   picture = edgraph.get() + ".png"
   plt.savefig(results_dir + picture)

def meas_IV():
   x = []
   y = []
   sVi = edVstart.get()
   Vi = float(sVi)
   sVf = edVstop.get()  
   Vf = float(sVf)
   Vstep = float(edVstep.get())
   stdelay = edtdelay.get()
   tdelay = float(stdelay)
   keithley_setup()     
   keithley.write("smua.source.levelv = " + sVi)
   keithley.write("smua.source.output = smua.OUTPUT_ON")
   plot_setup()   
   while (Vi <= Vf):
      if keyboard.is_pressed("Escape"):
            break
      meas = keithley.query("print(smua.measure.i())")
      a.scatter(Vi, meas, color="green")
      canvas.draw()
      x.append(Vi)             
      y.append(float(meas))
      Vi += Vstep      
      keithley.write("smua.source.levelv = " + str(Vi))
   save_setup(x, y)
   keithley_off()
   
def meas_V():   
   x = []
   y = []
   sV = edVconst.get()
   V = float(sV)
   st_step = edtime.get()
   ti = 0
   t_step = float(st_step)
   st_range = edtrange.get()
   t_range = float(edtrange.get())
   keithley_setup()      
   keithley.write("smua.source.levelv = " + sV)
   keithley.write("smua.source.output = smua.OUTPUT_ON")
   plot_setup()     
   while (ti <= t_range):
      if keyboard.is_pressed("Escape"):
            break
      meas = keithley.query("print(smua.measure.i())")
      a.scatter(ti, meas, color="green")
      canvas.draw()
      x.append(ti)
      y.append(float(meas))
      ti += t_step      
      time.sleep(t_step)         
   save_setup(x, y)
   keithley_off()   

def close():
   arduino_comm("100")
   keithley_reset()   
   plt.close()
   janela.destroy()

janela = Tk()
janela.title("Stability chamber")
janela.geometry("750x920+300+20")

f = plt.figure(figsize=(4, 4), dpi=100)
f.subplots_adjust(left=0.2, bottom=0.125)
a = f.add_subplot(111)
canvas = FigureCanvasTkAgg(f, janela)
canvas.get_tk_widget().pack(side=BOTTOM, fill=X, expand=0)
rm = visa.ResourceManager()
keithley = rm.open_resource("GPIB0::26")
arduino = rm.open_resource("COM3")
arduino.baud_rate = 9600
arduino.port = "COM3"

bt11 = Button(janela, width=16, text="Sample 1 - Device 1", fg="red", font=("Arial", 13, "bold"))
bt11["command"] = partial(arduino_comm, "1") 
bt11.place(x=20, y=50)
bt12 = Button(janela, width=16, text="Sample 1 - Device 2", fg="red", font=("Arial", 13, "bold"))
bt12["command"] = partial(arduino_comm, "2")
bt12.place(x=200, y=50)
bt13 = Button(janela, width=16, text="Sample 1 - Device 3", fg="red", font=("Arial", 13, "bold"))
bt13["command"] = partial(arduino_comm, "3")
bt13.place(x=380, y=50)
bt14 = Button(janela, width=16, text="Sample 1 - Device 4", fg="red", font=("Arial", 13, "bold"))
bt14["command"] = partial(arduino_comm, "4")
bt14.place(x=560, y=50)
bt21 = Button(janela, width=16, text="Sample 2 - Device 1", fg="green", font=("Arial", 13, "bold"))
bt21["command"] = partial(arduino_comm, "5")
bt21.place(x=20, y=100)
bt22 = Button(janela, width=16, text="Sample 2 - Device 2", fg="green", font=("Arial", 13, "bold"))
bt22["command"] = partial(arduino_comm, "6")
bt22.place(x=200, y=100)
bt23 = Button(janela, width=16, text="Sample 2 - Device 3", fg="green", font=("Arial", 13, "bold"))
bt23["command"] = partial(arduino_comm, "7")
bt23.place(x=380, y=100)
bt24 = Button(janela, width=16, text="Sample 2 - Device 4", fg="green", font=("Arial", 13, "bold"))
bt24["command"] = partial(arduino_comm, "8")
bt24.place(x=560, y=100)
bt31 = Button(janela, width=16, text="Sample 3 - Device 1", fg="blue", font=("Arial", 13, "bold"))
bt31["command"] = partial(arduino_comm, "9")
bt31.place(x=20, y=150)
bt32 = Button(janela, width=16, text="Sample 3 - Device 2", fg="blue", font=("Arial", 13, "bold"))
bt32["command"] = partial(arduino_comm, "10")
bt32.place(x=200, y=150)
bt33 = Button(janela, width=16, text="Sample 3 - Device 3", fg="blue", font=("Arial", 13, "bold"))
bt33["command"] = partial(arduino_comm, "11")
bt33.place(x=380, y=150)
bt34 = Button(janela, width=16, text="Sample 3 - Device 4", fg="blue", font=("Arial", 13, "bold"))
bt34["command"] = partial(arduino_comm, "12")
bt34.place(x=560, y=150)
bt41 = Button(janela, width=16, text="Sample 4 - Device 1", fg="black", font=("Arial", 13, "bold"))
bt41["command"] = partial(arduino_comm, "13")
bt41.place(x=20, y=200)
bt42 = Button(janela, width=16, text="Sample 4 - Device 2", fg="black", font=("Arial", 13, "bold"))
bt42["command"] = partial(arduino_comm, "14")
bt42.place(x=200, y=200)
bt43 = Button(janela, width=16, text="Sample 4 - Device 3", fg="black", font=("Arial", 13, "bold"))
bt43["command"] = partial(arduino_comm, "15")
bt43.place(x=380, y=200)
bt44 = Button(janela, width=16, text="Sample 4 - Device 4", fg="black", font=("Arial", 13, "bold"))
bt44["command"] = partial(arduino_comm, "16")
bt44.place(x=560, y=200)
btOFF = Button(janela, width=16, text="Devices OFF", fg="black", font=("Arial", 13, "bold"))
btOFF["command"] = partial(arduino_comm, "100")
btOFF.place(x=380, y=10)
btquit = Button(janela, width=16, text="CLOSE", fg="black", font=("Arial", 13, "bold"), command = close)
btquit.place(x=560, y=10)
btreset = Button(janela, width=16, text="Reset Keithley", fg="black", font=("Arial", 13, "bold"), command =keithley_reset)
btreset.place(x=200, y=10)
btIxV = Button(janela, width=16, text="Measure IxV", fg="black", font=("Arial", 15, "bold"), command=meas_IV)
btIxV.place(x=30, y=400)
btctV = Button(janela, width=16, text="Measure const. V", fg="black", font=("Arial", 15, "bold"), command=meas_V)
btctV.place(x=300, y=400)
btsetV = Button(janela, width=15, text="Set Keithley Voltage", fg="black", font=("Arial", 12), command=keithley_setV)
btsetV.place(x=540, y=305)
edsetV = Entry(janela, width=20)
edsetV.place(x=540, y=340)
lbIV = Label(janela, text = "I x V", font=("Arial", 15, "bold"))
lbIV.place(x=100, y=250)
lbV = Label(janela, text = "Constant V", font=("Arial", 15, "bold"))
lbV.place(x=320, y=250)
lbVstart = Label(janela, text = "V start", font=("Arial", 13, "bold"))
lbVstart.place(x=20, y=275)
edVstart = Entry(janela, width=20)
edVstart.place(x=110, y=280)
lbVstop = Label(janela, text = "V stop", font=("Arial", 13, "bold"))
lbVstop.place(x=20, y=305)
edVstop = Entry(janela, width=20)
edVstop.place(x=110, y=310)
lbVstep = Label(janela, text = "V step", font=("Arial", 13, "bold"))
lbVstep.place(x=20, y=335)
edVstep = Entry(janela, width=20)
edVstep.place(x=110, y=340)
lbtdelay = Label(janela, text = "Time delay", font=("Arial", 13, "bold"))
lbtdelay.place(x=20, y=365)
edtdelay = Entry(janela, width=20)
edtdelay.place(x=110, y=370)
lbIlimit = Label(janela, text = "Current limit", font=("Arial", 13, "bold"))
lbIlimit.place(x=540, y=250)
edIlimit = Entry(janela, width=20)
edIlimit.place(x=540, y=280)
lbVconst = Label(janela, text = "V", font=("Arial", 13, "bold"))
lbVconst.place(x=330, y=275)
edVconst = Entry(janela, width=20)
edVconst.place(x=370, y=280)
lbtime = Label(janela, text = "Time step", font=("Arial", 13, "bold"))
lbtime.place(x=270, y=335)
edtime = Entry(janela, width=20)
edtime.place(x=370, y=340)
lbtrange = Label(janela, text = "Time range", font=("Arial", 13, "bold"))
lbtrange.place(x=270, y=305)
edtrange = Entry(janela, width=20)
edtrange.place(x=370, y=310)
lbgraph = Label(janela, text = "Plot title", font=("Arial", 13, "bold"))
lbgraph.place(x=20, y=450)
edgraph = Entry(janela, width=40)
edgraph.place(x=100, y=455)
lbesc = Label(janela, text="(Press ESC to stop measuring, data will be saved)", font=("Arial", 12))
lbesc.place(x=100, y=480)

janela.mainloop()
