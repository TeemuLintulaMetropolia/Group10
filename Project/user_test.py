from user import Users

def run():
    manager = Users()

    print("Saved users:", manager.userlist)
    print("Currently selected:", manager.current_user)

    choice = input("Type [1] Select existing user, [2] Add new user, or [Enter] to continue: ")

    if choice == "1":
        name = input("Enter existing username: ")
        if manager.select_user(name):
            print(f"Switched to {manager.current_user} (Age: {manager.age})")

    elif choice == "2":
        name = input("New user's name: ")
        age = int(input("New user's age: "))
        gender = str(input("Gender: "))
        manager.add_user(name, age=age, gender=gender)
        print(f"Created and selected {manager.current_user}!")

    # From here on, your heartbeat sensor loop just reads manager.name and manager.high_bpm_alertma
    print(f"Ready to measure heartbeat for {manager.current_user}")
