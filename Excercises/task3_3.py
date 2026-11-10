from machine import Pin, I2C
from fifo import Fifo
from filefifo import Filefifo
from led import Led
import time
import micropython
from ssd1306 import SSD1306_I2C

class Encoder:
    def __init__(self, rot_a, rot_b):
        self.a = Pin(rot_a, mode = Pin.IN)
        self.b = Pin(rot_b, mode = Pin.IN)
        self.fifo = Fifo(30, typecode = 'i')
        self.a.irq(handler = self.handler, trigger = Pin.IRQ_RISING, hard = True)
    def handler(self, pin):
        if self.b():
            self.fifo.put(-1)
        else:
            self.fifo.put(1)
    

def print_screen(values, maxval, minval):
    oled.fill(0)
    for x,value in enumerate(values):
        oled.pixel(x, int(63 - ((value - minval) / (maxval - minval) * 63)), 1)
    oled.show()

#Defining things
micropython.alloc_emergency_exception_buf(200)
fifo = Filefifo(10, name = 'week3_data.txt', repeat = False)
samples = []

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

rot = Encoder(10, 11)

#program starts
for i in range(1000): #We add everything to a list
        try:
            data = fifo.get()
        except:
            break
        samples.append(data)
        
maxval = 0
minval = 0
for sample in samples: #We fing min and max values
    if maxval == 0:
        maxval = sample
        minval = sample
    if maxval < sample:
        maxval = sample
    elif minval > sample:
        minval = sample
x = 0

while True:
    if rot.fifo.has_data():
        step = rot.fifo.get()
        x += step
        if x < 0:
            x = 0
        if x > len(samples) - 128:
            x = len(samples) - 128
        printsamples = []
        for i in range(128):
            printsamples.append(samples[x + i])
        print_screen(printsamples, maxval, minval)
            
            
            
    









