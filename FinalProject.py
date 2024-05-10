from datetime import datetime
from collections import UserDict
import pickle

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Phone(Field):
    def __init__(self, value):
        if len(value) == 10 and value.isdigit():
            super().__init__(value)
        else:
            raise ValueError("Number must be of 10 digits")
        
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Birthday must be in DD.MM.YYYY format")

class Record:
    def __init__(self, name):
        self.name = name
        self.phone='not yet initieted'
        self.birthday = None  # New field for birthday

    def add_phone(self, phone):
        self.phone=Phone(phone)

    def edit_phone(self, givenName, newPhoneNo):
        if givenName == self.name:
            self.phone= Phone(newPhoneNo)
        else:
            print(f'Numele dat: {givenName} nu exista!')

    def find_phone(self, phoneNumber):
        if phoneNumber in self.phones:
            return phoneNumber
        else:
            print("this phone does not exist in the list")

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        return(f"birthday added for {self.name}")

    def __str__(self):
        birthday_str = f", Birthday: {str(self.birthday)}" if self.birthday else ""
        return f"Contact name: {self.name.value}, Phone: {self.phone}: {birthday_str}"
    
class AddressBook(UserDict):
    def add_record(self, name, phone):
        record = Record(name)
        record.add_phone(phone)
        self.data[record.name] = record

        
    def get_birthdays_per_week(self):
        today= datetime.now().date()  #2024-03-18
        result={}
        peopleDict={}
        for name1, record in self.data.items():
            name= name1
            birthday=record.birthday.value
            peopleDict[name]=birthday

        for name,birthday in peopleDict.items():
            days_until_birthday = (birthday.replace(year=today.year) - today).days
            if days_until_birthday<=7 and days_until_birthday >=0:
                if birthday.replace(year=today.year).strftime('%A') == "Saturday" or birthday.replace(year=today.year).strftime('%A') == "Sunday":
                    if "Monday" in result:
                        result["Monday"]+= ", " + name
                        continue
                    else:
                        result["Monday"]= name
                        continue
                dayOfBirthday_this_wekk=birthday.replace(year=today.year).strftime('%A')
                if dayOfBirthday_this_wekk in result:
                    result[dayOfBirthday_this_wekk]+= ", " + name
                else:
                    result[dayOfBirthday_this_wekk]=name

        return(result)
    




################################# EXCEPTIONS HANDLERS #################################

def input_error(func):
    def inner(args, kwargs):
        try:
            return func(args, kwargs)
        except ValueError as e:
            return e
        except Exception:
            return "Give me name and phone please."

    return inner

def name_exists(func):
    def inner(args, kwargs):
        try:
            return func(args,kwargs)
        except IndexError:
            return "The name does not exist"

    return inner

def general_error(func):
    def inner(args, kwargs):
        try:
            return func(args,kwargs)
        except Exception as e:
            return e
    return inner


def valid_name(func):
     def inner(args, kwargs):
        try:
            return func(args,kwargs)
        except KeyError:
            return "The name does not exist"

     return inner

################################# END OF EXCEPTIONS HANDLERS #################################





def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@general_error
@input_error
def add_contact(args, book):
    name, phone = args
    if name in book:
        return f"Username {name} already exists"
    book.add_record(name, phone)  
    return "Contact added."


@name_exists
@general_error
def change_contact(args, book):
    if len(args)!=2:
        return f"ValueError: not enough values to unpack (expected 2, got {len(args)}). Ex: change Name oldNumber NewNumber"
    name, newPhone = args

    if name in book:
        book[name].edit_phone(name, newPhone)
        return "Contact updated."
    else:
        return f"Can`t find this name {name} "
    

@general_error
@valid_name
def phone(args,book):
    name=args[0]
    if name in book:
        return book[name].phone
    else:
        raise KeyError

@general_error
@name_exists
def addBirthday(args,book):
    name, birthDate = args
    if name in book:
        return book[name].add_birthday(birthDate)
    else:
        raise IndexError

@valid_name
def showBirthday(args,book):
    name = args[0]
    if name in book and book[name].birthday:
        return(f"{name}'s birthday is on {book[name].birthday.value.strftime('%d.%m.%Y')}")
    else:
        raise IndexError

def save_to_pickle(data, filename='data.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

def load_from_pickle(filename='data.pkl'):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Return an empty dictionary if the file doesn't exist


def showAllBirthdays(book):
    birthdays = book.get_birthdays_per_week()
    result=''
    if birthdays:
        print("Birthdays in the next week:")
        for day, names in birthdays.items():
            result += f"{day}: {names}\n"
        return result
    else:
        return "No birthdays in the next week."

    

def main():
    book = load_from_pickle()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            save_to_pickle(book)  
            break
        elif command.lower() == "hello":
            print("How can I help you?")
        elif command.lower() == "add":
            print(add_contact(args, book))
        elif command.lower() == "change":
            print(change_contact(args, book))
        elif command.lower() == "phone":
            print(phone(args, book))
        elif command.lower() == "add-birthday":
            print(addBirthday(args,book))
        elif command.lower() == "show-birthday":
            print(showBirthday(args, book))
        elif command.lower() == "birthdays":
            print(showAllBirthdays(book))
        elif command.lower() == "all":
            for name, record in book.items():
               print(f"{name}: {record.phone}")

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()