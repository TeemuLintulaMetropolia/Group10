# oled_refresh_rate_1_of_3
# Shows why calling show() for every pixel is slow (~30 ms each).
import time
import random
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

button1 = Pin(9, Pin.IN, Pin.PULL_UP)
button2 = Pin(7, Pin.IN, Pin.PULL_UP)

pressed1 = False
pressed2 = False

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)


class Bodypart:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def move (self, x, y):
        self.x = x
        self.y = y
        

class Head:
    def __init__ (self):
        self.x = 0
        self.y = 0
        self.direction = 1
        self.parts = []
    
    def makelonger (self):
        if len(self.parts) == 0:
            self.parts.append(Bodypart(self.x, self.y))
        else:
            lastpart = self.parts[len(self.parts) - 1]
            self.parts.append(Bodypart(lastpart.x, lastpart.y))

    
    def move (self):
        
        for i in range(len(self.parts) - 1, 0, -1):
            self.parts[i].move(self.parts[i - 1].x, self.parts[i - 1].y)
            if len(self.parts) > 0:
                self.parts[0].move(self.x, self.y)
                
        if self.direction == 1:
            self.x += 1
        elif self.direction == 2:
            self.y -= 1
        elif self.direction == 3:
            self.x -= 1
        elif self.direction == 4:
            self.y += 1
class Fruit:
    def __init__ (self):
        self.x = 0
        self.y = 0
        self.eaten = True
        self.colorFrames = 0
    
    def summon (self, snake):
        while True:
            x = random.randint(0, 127)
            y = random.randint(0, 63)
            possible = True
            if snake.x == x and snake.y == y:
                possible = False
            else:
                for part in snake.parts:
                    if part.x == x and part.y == y:
                        possible = False
                        break
            
            if possible:
                self.x = x
                self.y = y
                break

head = Head()
fruit = Fruit()
alive = True

def collision (snake, fruit):
    if snake.x == fruit.x and snake.y == fruit.y:
        snake.makelonger()
        fruit.eaten = True
    if snake.x > 127 or snake.x < 0 or snake.y < 0 or snake.y > 63:
        return False
    for part in snake.parts:
        if part.x == snake.x and part.y == snake.y:
            return False
    return True

def draw (head, fruit):
    if fruit.colorFrames == 0:
        oled.fill(0)
        oled.pixel(head.x, 63 - head.y, 1)
        for part in head.parts:
            oled.pixel(part.x, 63 - part.y, 1)
        oled.pixel(fruit.x, 63 - fruit.y, 1)
        oled.show()
    else:
        oled.fill(1)
        oled.pixel(head.x, 63 - head.y, 0)
        for part in head.parts:
            oled.pixel(part.x, 63 - part.y, 0)
        oled.pixel(fruit.x, 63 - fruit.y, 0)
        oled.show()
    
    
while alive:
    time.sleep(0.1)
    if len(head.parts) < 10:
        head.makelonger()
    head.move()
    alive = collision(head, fruit)
    draw(head, fruit)

    if button1() == False and pressed1 == False:
        head.direction += 1
        if head.direction > 4:
            head.direction = 1
        pressed1 = True
    elif button1() and pressed1 == True:
        pressed1 = False
    
    if button2() == False and pressed2 == False:
        head.direction -= 1
        if head.direction < 1:
            head.direction = 4
        pressed2 = True
    elif button2() and pressed2 == True:
        pressed2 = False
        
    if fruit.eaten:
        fruit.eaten = False
        fruit.colorFrames += 5
        fruit.summon(head)
    if fruit.colorFrames > 0:
        fruit.colorFrames -= 1
        
oled.fill(1)
oled.text('GAME OVER', 25, 31, 0)
oled.show()
    
        