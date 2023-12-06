contacts = {}

def exception_handling(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TypeError as str_error:
            if "positional argument" in str_error.args[0]:
                return str_error
    return wrapper

@exception_handling
def add_new_contact(name, phone):
    if not phone.isnumeric():
        raise TypeError("Oops. Wrong number.")
    if name in contacts:
        raise ValueError(f"Oops. I already have a contact named \"{name.capitalize()}\"")
    
    contacts[name] = phone
    return f"It's all good.\nI have added a new contact with the name \"{name.capitalize()}\" and the phone number \"{phone}\""


def change_phone(name, phone):
    if not name in contacts:
        raise Exception(f"Oops. I couldn't find {name}.")
    if not phone.isnumeric():
        raise ValueError("Oops. Wrong number.")

    contacts[name] = phone
    return f"That's great.\nThe phone number for contact \"{name}\" has been changed to \"{phone}\""


def show_phone(name):
    if not name in contacts:
        raise Exception(f"Oops. I couldn't find {name.capitalize()}.")

    return f"Name: {name.capitalize()} Phone: {contacts[name]}"


def show_all():
    text = " ".join(f"{name} {phone}\n" for name, phone in contacts.items())
    return text


def main():
    commands = {
        
    }


    while True:
        user_string = input(">>> ").lower()
        
        if user_string == "test":
            print(test(1))
        
        if user_string in ["good bye", "close", "exit"]:
            print("Good bye!")
            exit()
        
        elif user_string == "hello":
            print("How can I help you?")
        
        elif user_string.startswith("add"):
            
            func, *args = user_string.split(" ")
            
            print(add_new_contact(*args))
        
        elif user_string.startswith("change"):
            _, name, phone = user_string.split(" ")
            print(change_phone(name, phone))
        
        elif user_string.startswith("phone"):
            _, phone = user_string.split(" ")
            print(show_phone(phone))
        
        elif user_string.startswith("show all"):
            print(show_all())
        
        else:
            print("I don't understand you")
        


if __name__ == "__main__":
    main()