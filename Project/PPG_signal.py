from fifo import Fifo
from piotimer import Piotimer
from machine import ADC, Pin
import hardware
import micropython

micropython.alloc_emergency_exception_buf(200)


def run(value, previous_value, maxval, minval, HR):
    i2c = hardware.i2c
    oled = hardware.oled
    
    previous = int(55 - ((previous_value - minval) / (maxval - minval) * 55))
    current = int(55 - ((value - minval) / (maxval - minval) * 55))
    if current == 0:
        current = 1
    x = 127
    
    oled.scroll(-1, 0)
    oled.fill_rect(127, 0, 1, 64, 0)
    oled.line(x, previous, x, current, 1)
    oled.fill_rect(0, 55, 128, 9, 0)
    oled.text(f"HR: {HR}", 0, 56, 1)
    
    oled.show()
