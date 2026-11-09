from machine import Pin, I2C
from fifo import Fifo
from led import Led
import time
import micropython
from ssd1306 import SSD1306_I2C
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

def toggle_selected_led(pin, value):
    led = Led(pin)
    led.value(value) 
    
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

def print_screen(selected, leds):
    oled.fill(0)
    for i in range(3):
        x = " "
        y = "OFF"
        if selected == i:
            x = "*"
        if leds[i] == 1:
            y = "ON"
        oled.text(f"{x} Led{i+1} {y}", 36, 8*((i+1)*2), 1)
    oled.show()

button = Pin(12, mode = Pin.IN, pull = Pin.PULL_UP)
my_button = Button_handler()
button.irq(handler = my_button.handler, trigger = Pin.IRQ_FALLING, hard = True)
rot = Encoder(10, 11)
leds = [0, 0, 0]
selected = 0
print_screen(selected , leds)
while True:
    if rot.fifo.has_data():
        step = rot.fifo.get()
        selected = (selected + step) % 3
        if selected < 0:
            selected = 2
        if selected > 2:
            selected = 0
        print_screen(selected , leds)
    if my_button.fifo.has_data():
        my_button.fifo.get()
        print(selected)
        if leds[selected] == 0:
            leds[selected] = 1
        else:
            leds[selected] = 0
        print(leds)
        print_screen(selected , leds)
        toggle_selected_led(22-selected, leds[selected])


















