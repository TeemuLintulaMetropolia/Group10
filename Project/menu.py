from hardware import oled

class Menu_Item:
    def __init__ (self, text, program):
        self.text = text
        self.program = program
        
def print_menu(selected, anim_frame, Menu):
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