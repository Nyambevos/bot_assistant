from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.__value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if self.is_valid(value):
            self.__value = value
        else:
            self.__value = None

    def is_valid(self, value):
        return True


class Name(Field):
    def is_valid(self, value):
        if value.isalnum():
            return True
        raise ValueError("Incorrect name")


class Phone(Field):
    def is_valid(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Incorrect phone number")
        return True


class Birthday(Field):
    def is_valid(self, value):
        if value is not None:
            birthday = datetime.strptime(value, "%d-%m-%Y")
            if birthday > datetime.now():
                raise ValueError("Incorrect birthday's date")
            return True


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.birthday = Birthday(birthday)
        self.phones = []

    def __str__(self):
        name = self.name.value
        phones = ', '.join(p.value for p in self.phones)
        birthday = self.birthday.value
        return f"Contact name: {name.capitalize()}. Phones: {phones}. Birthday: {birthday}"

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones.remove(self.find_phone(phone))

    def edit_phone(self, old_phone, new_phone):
        obj_old_phone = self.find_phone(old_phone)

        if obj_old_phone is None:
            raise IndexError(f"Phone number:: {old_phone}, not found")

        index_old_phone = self.phones.index(obj_old_phone)

        self.phones[index_old_phone] = Phone(new_phone)

    def find_phone(self, phone):
        ph = list(filter(lambda ph: ph.value == phone, self.phones))

        if len(ph):
            return ph[0]

        return None

    def days_to_birthday(self):
        if self.birthday is not None:
            birthday = datetime.strptime(
                self.birthday.value, "%d-%m-%Y")

            next_birthday = birthday.replace(
                year=datetime.now().year)

            if next_birthday < datetime.now():
                next_birthday = next_birthday.replace(
                    year=next_birthday.year + 1)

            difference = next_birthday.date() - datetime.now().date()

            return difference.days

        return None


class AddressBook(UserDict):
    def add_record(self, record):
        self.data.update({record.name.value: record})

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        self.data.pop(name, None)

    def iterator(self, amount=1):
        index = 0
        records_list = list(self.data.values())

        while index < len(records_list):
            yield records_list[index:index + amount]
            index += amount

    def find_by_key(self, key):
        match_records = []
        for record in self.data.values():
            if key in record.name.value:
                match_records.append(record)
                continue
            else:
                for phone in record.phones:
                    if key in phone.value:
                        match_records.append(record)
                        break
        return match_records if match_records else None
