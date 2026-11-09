from machine import Pin
from fifo import Fifo
from led import Led
import time
import micropython
micropython.alloc_emergency_exception_buf(200)

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
    def __init__(self, indicator_led):
        self.led = Led(indicator_led)
        self.past_click = 0
        self.delay = 200
        self.fifo = Fifo(30, typecode = 'i')
        
    def handler(self, pin):
        now = time.ticks_ms()
        if time.ticks_diff(now, self.past_click) > self.delay:
            if pin.value()== 0:
                self.past_click = now
                self.fifo.put(1)
        

button = Pin(12, mode = Pin.IN, pull = Pin.PULL_UP)
my_button = Button_handler(22)
button.irq(handler = my_button.handler, trigger = Pin.IRQ_FALLING, hard = True)
old = 0
rot = Encoder(10, 11)            
led_on = False
brightness = 0
while True:
    if my_button.fifo.has_data():
        my_button.fifo.get()
        my_button.led.toggle()
        led_on = not led_on
    if rot.fifo.has_data():
        step = rot.fifo.get()
        print(step)
        if led_on:
            brightness += step * 5
            if brightness < 0:
                brightness = 0
            if brightness > 100:
                brightness = 100
            my_button.led.brightness(brightness)
