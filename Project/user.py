import json
import os

class Users:
    def __init__(self, save_file="profiles.json"):
        self.save_file = save_file
        self.gender = "binary"
        self.age = 30
        self.userlist = {}
        
        self.load()
        
    def add_user(self, name, age, gender):
        self.userlist[name] = {
            "age" : age,
            "gender" : gender
            }
        self.set_current_user(name)
        self.save()
        
    def set_current_user(self, name):
        user_data = self.userlist[name]
        self.current_user = name
        self.age = user_data.get("age")
        self.gender = user_data.get("gender")

    def save(self):
        data_to_save = {
            "recent": self.current_user,
            "profiles": self.userlist
            }
        
        with open(self.save_file, "w") as file:
            json.dump(data_to_save, file)
            file.flush()
                    
    def load(self):
        if self.save_file in os.listdir():
            try:
                with open(self.save_file, "r") as data:
                    saved = json.load(data)

                self.userlist = saved.get("profiles", {})
                self.current_user = saved.get("recent")
                if self.current_user in self.userlist:
                    self.set_current_user(self.current_user)
                    return
            except(ValueError, OSError):
                print("Error")
        self.save()
    
    def select_user(self,name):
        if name not in self.userlist:
            print(f"Username {name} not found")
            return False
        self.set_current_user(name)
        self.save()
        return True
    
        

        
        
    
        
        
        
        