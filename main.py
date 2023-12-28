import sys
import pickle
from pathlib import Path

from address_book import AddressBook, Record

contacts = AddressBook()

FILENAME = "contacts.bin"


def help(*_):
    text = ("List of available commands:\n"
            "\n"
            "\tcreate - Adding new contacts command\n"
            "\t\tArguments:\n"
            "\t\t\tname - name without spaces\n"
            "\t\t\tbirthday - optional. In the format dd-mm-yyyy\n"
            "\t\tExample: create Olga 11-05-1983\n"
            "\n"
            "\tadd - Add a phone number to an existing contact\n"
            "\t\tArguments:\n"
            "\t\t\tname - name without spaces\n"
            "\t\t\tphone - phone number, 10 digits.\n"
            "\t\tExample: add Olga 0987654321\n"
            "\n"
            "\tchange - Edit the phone number t\n"
            "\t\tArguments:\n"
            "\t\t\tname - name without spaces\n"
            "\t\t\told phone - the number to be changed, 10 digits.\n"
            "\t\t\tnew phone - new phone number, 10 digits.\n"
            "\t\tExample: change Olga 0987654321 1234567890\n"
            "\n"
            "\tphone - Show phone numbers of the selected contact\n"
            "\t\tArguments:\n"
            "\t\t\tname - name without spaces\n"
            "\t\tExample: phone Olga\n"
            "\n"
            "\tfind - Search for contacts by keyword\n"
            "\t\tArguments:\n"
            "\t\t\tkeyword - Any keyword you want to"
            "find in the name or phone number\n"
            "\t\tExample: find 098\n"
            "\n"
            "\tshow all - Show all contacts \n"
            "\n"
            "\thelp - List of all commands\n"
            "\n"
            "\texit - Уxit from the program\n"
            "\n"
            )

    return text


def save_to_file(address_book: AddressBook(),  filename):
    with open(filename, "wb") as file:
        pickle.dump(address_book.data, file)


def load_from_file(address_book: AddressBook(), filename):
    with open(filename, "rb") as file:
        address_book.data = pickle.load(file)


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
    save_to_file(contacts, FILENAME)
    sys.exit()


@input_error
def create_new_contact(name, birthday=None):
    if name in contacts:
        raise IndexError(f"I already have a contact named: {name}")

    contacts.add_record(Record(name, birthday))

    return f"I have added a new contact with the name \"{name.capitalize()}\""


@input_error
def add_new_phone(name, phone):
    contacts[name].add_phone(phone)

    return f"Phone number {phone} has been added to {name.capitalize()} contact"


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
        "create": create_new_contact,
        "add": add_new_phone,
        "hello": hello,
        "change": change_phone,
        "phone": show_phone,
        "show all": show_all,
        "find": find,
        "help": help,

        "exit": exit,
        "good bye": exit,
        "close": exit
    }

    if Path(FILENAME).is_file():
        load_from_file(contacts, FILENAME)
    else:
        print("Hello. I'll help you save all your contacts.\n"
              "I have commands to save contacts, read contacts,"
              "and search for contacts by keywords.\n"
              "You can always use the 'help' command to learn more.")

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
