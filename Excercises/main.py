#main.py for task 2.1
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from ButtonClass import Button
import task2_1
import task2_2
import task2_3

import time

sw0 = Button(7)
sw1 = Button(8)
sw2 = Button(9)
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SSD1306_I2C(128,64, i2c)





selectedprogram = 1
def printoled(selectedprogram):
    oled.fill(0)
    oled.text(f"Task 2.{selectedprogram}", 32, 16, 8)
    oled.text("Press SW1 to run", 0, 32, 8)
    oled.text("Press SW2 or SW0", 0, 42, 8)
    oled.text("to cycle", 34, 52, 8)
    oled.show()

printoled(1)
while True:
    sw1.checkRelease()
    if sw1.checkRelease():
        if selectedprogram == 1:
            task2_1.run_program()
        elif selectedprogram == 2:
            task2_2.run_program()
        elif selectedprogram == 3:
            task2_3.run_program()
    if sw0.checkRelease():
        selectedprogram += 1
        if selectedprogram > 3:
            selectedprogram = 1
        printoled(selectedprogram)
    if sw2.checkRelease():
        selectedprogram -= 1
        if selectedprogram < 1:
            selectedprogram = 3
        printoled(selectedprogram)

    time.sleep(0.5)