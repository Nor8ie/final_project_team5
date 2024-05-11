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

class Address(Field):
    def __init__(self, value):
        super().__init__(value)

class Email(Field):
    def __init__(self, email):
        contains_at = False
        contains_dot = False
        for char in email:
             if char == "@":
                contains_at = True
        afterAt= email.split("@")
        if len(afterAt) > 1 and "." in afterAt[1]:
                contains_dot = True

        if contains_at and contains_dot:
            super().__init__(email)
        else:
            raise ValueError("Email is not correct. Must have @ and .")   

class Record:
    def __init__(self, name):
        self.name = name
        self.phone='not yet initieted'
        self.birthday = None  # New field for birthday
        self.address= "Not yet added"  # New field for address
        self.email= "No email added"

    def add_phone(self, phone):
        self.phone=Phone(phone)

    def add_address(self, address:str ):
        self.address= Address(address)
        return (f"address added for {self.name}")
    
    def add_email(self, email:str):
        self.email= Email(email)
        return (f"email added for {self.name}")

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


def indexOutOfRange(func):
    def inner(args, kwargs):
        try:
            return func(args, kwargs)
        except IndexError as e:
            return "index out of bounds, maybe the value does not exist"
        except Exception as ee:
            return ee

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
    

@general_error
@general_error
def searchBy(args, book):
    field, *argument = args
    argument=' '.join(argument)
    result = ""
    for name, record in book.items():
        if field.lower() == "phone" and record.phone.value == argument:
            result += f"Name: {name}, Phone: {record.phone}, Birthday: {record.birthday}, Address: {record.address}, Email: {record.email}\n"
        elif field.lower() == "name" and name == argument:
            result += f"Name: {name}, Phone: {record.phone}, Birthday: {record.birthday}, Address: {record.address}, Email: {record.email}\n"
        elif field.lower() == "birthday" and record.birthday and record.birthday.value == datetime.strptime(argument, "%d.%m.%Y").date():  
            result += f"Name: {name}, Phone: {record.phone}, Birthday: {record.birthday}, Address: {record.address}, Email: {record.email}\n"
        elif field.lower() == "address" and record.address.value == argument:
            result += f"Name: {name}, Phone: {record.phone}, Birthday: {record.birthday}, Address: {record.address}, Email: {record.email}\n"
        elif field.lower() == "email" and record.email.value == argument:
            result += f"Name: {name}, Phone: {record.phone}, Birthday: {record.birthday}, Address: {record.address}, Email: {record.email}\n"
    if result:
        return result
    else:
        return "No records found for the given criteria."

    
@general_error
@valid_name
def changeBy(args, book):
    field, name, *new_value = args
    new_value = ' '.join(new_value)
    if name in book:
        if field.lower() == "phone":
            book[name].phone = Phone(new_value)
            return f"Phone updated for {name}"
        elif field.lower() == "birthday":
            book[name].birthday = Birthday(new_value)
            return f"Birthday updated for {name}"
        elif field.lower() == "address":
            book[name].address = Address(new_value)
            return f"Address updated for {name}"
        elif field.lower() == "email":
            book[name].email = Email(new_value)
            return f"Email updated for {name}"
        else:
            return f"Field '{field}' cannot be changed."
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

@general_error
@name_exists
def addAddress(args,book):
    name = args[0]
    address = ' '.join(args[1:])
    if name in book:
        return book[name].add_address(address)
    else:
        raise IndexError

@general_error
@name_exists
def addEmail(args,book):
    name,email = args
    if name in book:
        return book[name].add_email(email)
    else:
        raise IndexError


@valid_name
@indexOutOfRange
def showBirthday(args,book):
    name = args[0]
    if name in book and book[name].birthday:
        return(f"{name}'s birthday is on {book[name].birthday.value.strftime('%d.%m.%Y')}")
    else:
        raise IndexError


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



############ SAVE FILE AS A DATABASE

def save_to_pickle(data, filename='data.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

def load_from_pickle(filename='data.pkl'):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Return an empty dictionary if the file doesn't exist

########### 
    

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
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change-by":
            print(changeBy(args, book))
        elif command == "add-birthday":
            print(addBirthday(args,book))
        elif command == "add-address":
            print(addAddress(args,book))
        elif command == "add-email":
            print(addEmail(args,book))
        elif command == "show-birthday":
            print(showBirthday(args, book))
        elif command == "birthdays":
            print(showAllBirthdays(book))
        elif command == "search-by":
            print(searchBy(args, book))
        elif command == "all":
            for name, record in book.items():
               print(f"{name}: phone: {record.phone} / address: {record.address} / email: {record.email}")

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()