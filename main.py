contacts = {}

def input_error(func):
    def wrapper(*args, **kwargs):
        if len(args) == 2 and not args[1].isnumeric():
            return "Incorrect number."
        
        try:
            return func(*args, **kwargs)
        except TypeError as str_error:
            if "positional argument" in str_error.args[0]:
                if "2" in str_error.args[0]:
                    return "Give me name and phone please"
                elif "1" in str_error.args[0]:
                    return "Enter user name"
                else:
                    return str_error.args[0]
        
        except IndexError as str_error:
            return str_error.args[0]
    return wrapper


def hello():
    return "How can I help you?"

@input_error
def add_new_contact(name, phone):
    if name in contacts:
        raise IndexError(f"Oops. I already have a contact named \"{name.capitalize()}\"")
    
    contacts[name] = phone
    return f"I have added a new contact with the name \"{name.capitalize()}\""

@input_error
def change_phone(name, phone):
    if not name in contacts:
        raise IndexError(f"Oops. I couldn't find {name.capitalize()}.")

    contacts[name] = phone
    return f"The phone number for contact \"{name.capitalize()}\" has been changed to \"{phone}\""

@input_error
def show_phone(name):
    if not name in contacts:
        raise IndexError(f"Oops. I couldn't find {name.capitalize()}.")

    return f"Name: {name.capitalize()} Phone: {contacts[name]}"

@input_error
def show_all():
    return "\n".join(f"{name} {phone}" for name, phone in contacts.items())


def non_exist_command(*_):
    return "Oops. I don't know this command yet."

def main():
    commands = {
        
        "add": add_new_contact,
        "hello": exit,
        "change": change_phone,
        "phone": show_phone,
        "show all": show_all,

        "exit": exit,
        "good bye": exit,
        "close": exit
    }


    while True:
        user_string = input(">>> ").lower()
        
        if user_string in commands:
            return_string = commands[user_string]()
        else:
            comand, *args = user_string.split(" ")

            func_comand = commands.get(comand, non_exist_command)
            return_string = func_comand(*args)
            
        print(return_string)
                  


if __name__ == "__main__":
    main()