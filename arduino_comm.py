# encoding: utf-8

from tkinter import *
import serial
import time

def clockwise():
    ser.write(b'230')
      
def close_serial():
    ser.close()

def open_serial():   
    ser.open()
    time.sleep(1)

janela = Tk()
janela.title("Janela")

ser = serial.Serial(timeout=5)
ser.port = 'COM8'
ser.baudrate = 9600

ope = Button(janela, width=15, text="Open", command=open_serial)
ope.place(x=10, y=70)

go = Button(janela, width=15, text="Move", command=clockwise)
go.place(x=10, y=120)

clos = Button(janela, width=15, text="Close", command=close_serial)
clos.place(x=10, y=170)

ed1 = Entry(janela, width=12)
ed1.place(x=10, y=20)

janela.geometry("430x220+350+150")
janela.mainloop()



