#main.py for task 2.1
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time

sw1 = Pin(8, Pin.IN, Pin.PULL_UP)
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SSD1306_I2C(128,64, i2c)


oled.fill(0)
oled.text("Task 2.1", 32, 16, 8)
oled.text("Press SW1", 32, 32, 8)

oled.show()

while sw1() == True:
    time.sleep_ms(20)
    


from task2_1 import run_program
run_program()