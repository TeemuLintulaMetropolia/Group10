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
    

def print_screen():
    oled.fill(0)
    
    oled.show()

#Defining things
micropython.alloc_emergency_exception_buf(200)
fifo = Filefifo(10, name = 'sinewave_250Hz_03.txt', repeat = False)
samples = []

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

rot = Encoder(10, 11)

print_screen()

while True:
    while True #We add everything to a list
        try:
            data = fifo.get()
        except:
            break
        samples.append(data)
















