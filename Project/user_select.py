#from hardware import Encoder, Button_handler, oled
#from machine import Pin, I2C
from user_manager import Users
#from led import Led
#import time

class Start_Item:
    def __init__ (self, text, program):
        self.text = text
        self.program = program

manager = Users()

Start_Menu = [
    Start_Item("Selected Existing User", manager.show_user())
    ]
print(Start_Menu[0].program) 

