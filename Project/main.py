from hardware import Encoder, Button_handler, oled
from machine import Pin, I2C
from led import Led
import heart_rate_monitor, user_test
from menu import Menu_Item, print_menu
import time
import micropython

micropython.alloc_emergency_exception_buf(200)

def run():
    #Every section in menu is created here and the function it starts is assigned
    Menu = [
    Menu_Item("Heart rate", heart_rate_monitor),
    Menu_Item("HRV analysis", user_test),
    Menu_Item("Kubios", user_test),
    Menu_Item("History", user_test),
    Menu_Item("Change user", user_test),
    ]
    
    #button setup
    button = Pin(12, mode = Pin.IN, pull = Pin.PULL_UP)
    my_button = Button_handler()
    button.irq(handler = my_button.handler, trigger = Pin.IRQ_FALLING, hard = True)
    
    
    #Rot encoder setup
    rot = Encoder(10, 11)
    selected = 0
    steps = 0
    
    def setup_pins(button, rot):
            button = Pin(12, mode = Pin.IN, pull = Pin.PULL_UP)
            my_button = Button_handler()
            button.irq(handler = my_button.handler, trigger = Pin.IRQ_FALLING, hard = True)
            while my_button.fifo.has_data():
                my_button.fifo.get()

                
    #Animation setup
    anim_frame = 0
    current_time = time.ticks_ms()
    last_time = time.ticks_ms()
    
    print_menu(selected, 0, Menu)
    
    #Operating the menu using rot encoder and animating the arrow selector
    while True:
        current_time = time.ticks_ms()
        if time.ticks_diff(current_time, last_time) >= 500:
            anim_frame = 1 - anim_frame  # frame changes from 0 to 1 or the other way
            last_time = current_time     
            print_menu(selected, anim_frame, Menu) # Päivitetään näyttö animoituna
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
            print_menu(selected, anim_frame, Menu)
        #Button pressing logic runs the function assigned to the menu section
        if my_button.fifo.has_data():
            my_button.fifo.get()
            Menu[selected].program.run()
            
            #When the function ends it needs to reassign all of this again
            setup_pins(button, rot)
            print_menu(selected, anim_frame, Menu)

run()

















