import json
import os

class User_Profiles:
    def __init__(self, save_file="profiles.json"):
        self.save_file = save_file
        self.temp_file = save_file + ".tmp"
        self.current_user = "admin"
        self.name = "admin"
        self.age = 30
        self.mean_ppi = 250
        self.mean_hr = 60
        self.rmssd = 2
        self.sdnn = -1
        self.current_user_info = {}
        
        self.load()
        
    def add_user(self, name, age, gender):
        self.write_to_info()
        self.current_user_info[name] = {
            "age" : age,
            "gender" : gender,
            "mean_ppi" : None,
            "mean_hr" : None,
            "rmssd" : None,
            "sdnn" : None
            }
        self.becomming_current_user(name)
        self.save()
        
    def becomming_current_user(self, name):
        user_data = self.current_user_info[name]
        self.current_user = name
        self.name = name
        self.age = user_data.get("age")
        self.mean_ppi = user_data.get("mean_ppi")
        self.mean_hr = user_data.get("mean_hr")
        self.rmssd = user_data.get("rmssd")
        self.sdnn = user_data.get("sdnn")
        
    def write_to_info(self):
        self.current_user_info[self.current_user] = {
            "age": self.age,
            "mean_ppi": self.mean_ppi,
            "mean_hr": self.mean_hr,
            "rmssd": self.rmssd,
            "sdnn": self.sdnn
        }

    def save(self):
        self.write_to_info()
        data_to_save = {
            "recent": self.current_user,
            "profiles": self.current_user_info
            }
        
        with open(self.temp_file, "w") as file:
            json.dump(data_to_save, file)
            file.flush()
            
        os.rename(self.temp_file, self.save_file)
        
    def load(self):
        if self.save_file in os.listdir():
            try:
                with open(self.save_file, "r") as data:
                    saved = json.load(data)

                self.current_user_info = saved.get("profiles", {})
                self.current_user = saved.get("recent")
                if self.current_user in self.current_user_info:
                    self.becomming_current_user(self.current_user)
                    return
            except(ValueError, OSError):
                print("Error")
        self.save()
                

    def list_users(self):
        return self.current_user_info
    
    def select_user(self,name):
        if name not in self.current_user_info:
            print(f"Username {name} not found")
            return False
        self.write_to_info()
        self.becomming_current_user(name)
        self.save()
        return True
    
        

        
        
    
        
        
        
        