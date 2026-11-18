from hardware import Encoder, Button_handler, oled
from machine import Pin, I2C
from led import Led
import heart_rate_monitor, user_test, test5
import Snake
import time

class Menu_Item:
    def __init__ (self, text, program):
        self.text = text
        self.program = program

def run():
    def print_screen(selected, anim_frame):
        oled.fill(0)
        for i, item in enumerate(Menu):
            x = "   "
            if selected == i:
                if anim_frame == 0:
                    x = "-> "
                else:
                    x = " ->"
            oled.text(f"{x} {item.text}", 0, i + i*8 + 4, 1)
        oled.show()
        
    #Every section in menu is created here and the function it starts is assigned
    Menu = [
    Menu_Item("Heart rate", heart_rate_monitor),
    Menu_Item("HRV analysis", test5),
    Menu_Item("Kubios", test5),
    Menu_Item("History", test5),
    Menu_Item("Change user", user_test),
    Menu_Item("Snake", Snake)
    ]
    
    #button setup
    button = Pin(12, mode = Pin.IN, pull = Pin.PULL_UP)
    my_button = Button_handler()
    button.irq(handler = my_button.handler, trigger = Pin.IRQ_FALLING, hard = True)
    
    #Rot encoder setup
    rot = Encoder(10, 11)
    selected = 0
    steps = 0
    
    #Animation setup
    anim_frame = 0
    current_time = time.ticks_ms()
    last_time = time.ticks_ms()
    
    print_screen(selected, 0)
    
    #Operating the menu using rot encoder and animating the arrow selector
    while True:
        current_time = time.ticks_ms()
        if time.ticks_diff(current_time, last_time) >= 500:
            anim_frame = 1 - anim_frame  # frame changes from 0 to 1 or the other way
            last_time = current_time     
            print_screen(selected, anim_frame) # Päivitetään näyttö animoituna
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
            print_screen(selected, anim_frame)
        #Button pressing logic runs the function assigned to the menu section
        if my_button.fifo.has_data():
            my_button.fifo.get()
            Menu[selected].program.run()
            print_screen(selected, anim_frame)

run()

















