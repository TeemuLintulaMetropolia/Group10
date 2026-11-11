from hardware import Encoder, Button_handler, oled
from machine import Pin, I2C
from led import Led
import task3_2

class Menu_Item:
    def __init__ (self, text, program):
        self.text = text
        self.program = program

def run():
    def print_screen(selected):
        oled.fill(0)
        for i, item in enumerate(Menu):
            x = " "
            if selected == i:
                x = "*"
            oled.text(f"{x} {item.text}", 8, 8*(i+1), 1)
            print(item.text)
        oled.show()
    
    Menu = [
    Menu_Item("Heart rate monitor", task3_2),
    Menu_Item("HRV analysis", task3_2),
    Menu_Item("Kubios", task3_2),
    Menu_Item("History", task3_2),
    Menu_Item("Change user", task3_2)
    ]

    button = Pin(12, mode = Pin.IN, pull = Pin.PULL_UP)
    my_button = Button_handler()
    button.irq(handler = my_button.handler, trigger = Pin.IRQ_FALLING, hard = True)
    rot = Encoder(10, 11)
    selected = 0
    print_screen(selected)
    

run()
















