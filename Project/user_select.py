from hardware import Encoder, Button_handler, oled
from machine import Pin, I2C
from user_manager import Users
from led import Led
import time
class Screen_Item:
    def __init__ (self, text, program):
        self.text = text
        self.program = program

def print_screen(selected, anim_frame, users):
        oled.fill(0)
        for i, item in enumerate(users):
            x = "   "
            if selected == i:
                if anim_frame == 0:
                    x = "-> "
                else:
                    x = " ->"
            oled.text(f"{x} {item.text}", 0, i + i*8 + 4, 1)
        oled.show()

def add_users_to_userlist(userlist):
    userslist = Start_Menu["select_user"].program
    user_menu = []
    if userslist == None:
        return False
    for user in userslist:
        print(f"This is printing: {user}")
        user_menu.append(Screen_Item(f"{user}", print("hello")))
    return user_menu

manager = Users()

Start_Menu = {
    "select_user": Screen_Item("Selected Existing User", manager.list_user()),
    }

added_user_to_list = add_users_to_userlist(Start_Menu)
print(added_user_to_list)
print_screen(0,0,added_user_to_list)
