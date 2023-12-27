import sys
from pathlib import Path

from address_book import AddressBook, Record

contacts = AddressBook()

FILENAME = "contacts.bin"


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError as err:
            return err
        except TypeError:
            return "Incorrect number of arguments"
        except KeyError as err:
            return f"Record {err} not found"
        except ValueError as err:
            return err

    return wrapper


def hello():
    return "How can I help you?"


def exit():
    contacts.save_to_file(FILENAME)
    sys.exit()


@input_error
def add_new_contact(name, phone):
    if name in contacts:
        raise IndexError(f"I already have a contact named: {name}")

    contacts.add_record(Record(name))
    contacts[name].add_phone(phone)

    return f"I have added a new contact with the name \"{name.capitalize()}\""


@input_error
def change_phone(name, old_phone, new_phone):
    contacts[name].edit_phone(old_phone, new_phone)

    return (f"The phone number for contact: {name}" +
            f" has been changed to: {new_phone}")


@input_error
def show_phone(name):
    phones = []
    for phone in contacts[name].phones:
        phones.append(phone.value)

    return f"Name: {name.capitalize()} Phone: {' '.join(phones)}"


@input_error
def show_all():
    iter = contacts.iterator()

    for contact in iter:
        print(contact[0])

    return "Done"


@input_error
def find(keyword):
    found_contacts = contacts.find_by_key(keyword)
    if found_contacts is not None:
        for contact in found_contacts:
            print(contact)
        return "Done"
    else:
        return "No matches found"


def non_exist_command(*_):
    return "Oops. I don't know this command yet."


def main():
    commands = {

        "add": add_new_contact,
        "hello": hello,
        "change": change_phone,
        "phone": show_phone,
        "show all": show_all,
        "find": find,

        "exit": exit,
        "good bye": exit,
        "close": exit
    }
    if Path(FILENAME).is_file():
        contacts.load_from_file(FILENAME)

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
