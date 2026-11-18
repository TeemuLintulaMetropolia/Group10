from machine import Pin, I2C, ADC
from fifo import Fifo
from led import Led
import time
from piotimer import Piotimer
import micropython
from ssd1306 import SSD1306_I2C
micropython.alloc_emergency_exception_buf(200)

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

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

class Button_handler:
    def __init__(self):
        self.past_click = 0
        self.delay = 200
        self.fifo = Fifo(30, typecode = 'i')
        
    def handler(self, pin):
        now = time.ticks_ms()
        if time.ticks_diff(now, self.past_click) > self.delay:
            if pin.value()== 0:
                self.past_click = now
                self.fifo.put(1)
                
class HR_sensor:
    def __init__(self, adc_pin):
        self.adc = ADC(Pin(adc_pin, Pin.IN))
        self.fifo = Fifo(size=100, typecode='i')
        self.tmr = Piotimer(freq=250, callback=self.adc_callback)
        self.active = True

    def adc_callback(self, tmr):
        if self.active:
            self.fifo.put(self.adc.read_u16())