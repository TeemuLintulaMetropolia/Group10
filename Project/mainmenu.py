from hardware import Encoder, Button_handler, oled
from machine import Pin, I2C
from led import Led
import task3_2
import Snake

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
            oled.text(f"{x} {item.text}", 0, i + i*8 + 4, 1)
        oled.show()
    #Every section in menu is created here and the function it starts is assigned
    Menu = [
    Menu_Item("Heart rate", task3_2),
    Menu_Item("HRV analysis", task3_2),
    Menu_Item("Kubios", task3_2),
    Menu_Item("History", task3_2),
    Menu_Item("Change user", task3_2),
    Menu_Item("Snake", Snake)
    ]
    
    #button, rotatory encoder and other variables are set up 
    button = Pin(12, mode = Pin.IN, pull = Pin.PULL_UP)
    my_button = Button_handler()
    button.irq(handler = my_button.handler, trigger = Pin.IRQ_FALLING, hard = True)
    rot = Encoder(10, 11)
    selected = 0
    steps = 0
    print_screen(selected)
    
    #Operating the menu using rot encoder
    while True:
        #Rotating changes the selection every 3 steps
        if rot.fifo.has_data():
            step = rot.fifo.get()
            steps += step
            selected = int(steps / 3)
            if selected < 0:
                selected = len(Menu) -1
                steps = len(Menu) * 3
            if selected > len(Menu) -1:
                selected = 0
                steps = 0
            print_screen(selected)
        #Button pressing logic runs the function assigned to the menu section
        if my_button.fifo.has_data():
            my_button.fifo.get()
            Menu[selected].program.run()
            print_screen(selected)

run()

















