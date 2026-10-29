from machine import Pin, I2C
import time

class Button:
    __init__ (self, pin):
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)
    
    def checkRelease(self):
        if self.pin == False:
            while self.pin == False:
                #Waiting for release
                None
            return True
        else:
            return False