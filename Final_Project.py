from datetime import datetime, timedelta
from collections import UserDict
import pickle


class NumberError(Exception):
    pass


class NameError(Exception):
    pass


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        try:
            if value.isalpha():
                super().__init__(value)
            else:
                raise NameError("Name must contain only alphabetic characters")
        except ValueError as e:
            raise e


class Phone(Field):
    def __init__(self, value):
        if len(value) == 10 and value.isdigit():
            super().__init__(value)
        else:
            raise NumberError("Number must be of 10 digits")


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
        afterAt = email.split("@")
        if len(afterAt) > 1 and "." in afterAt[1]:
            contains_dot = True

        if contains_at and contains_dot:
            super().__init__(email)
        else:
            raise ValueError("Email is not correct. Must have @ and .")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phone = "not yet initieted"
        self.birthday = None  # New field for birthday
        self.address = "Not yet added"  # New field for address
        self.email = "No email added"
        self.notes = {}

    def add_phone(self, phone):
        self.phone = Phone(phone)

    def add_address(self, address: str):
        self.address = Address(address)
        return f"Address added for {str(self.name).title()}\n"

    def add_email(self, email: str):
        self.email = Email(email)
        return f"\nEmail added for {str(self.name).title()}\n"

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        return f"\nBirthday added for {str(self.name).title()}\n"

    def add_note(self, tag="General", note="None"):
        if tag not in self.notes:
            self.notes[tag] = note
            return f"Note added for {str(self.name).title()} with tag '{tag}'"
        return f"Note with tag '{tag}' already exists. Try another tag"
        

    def edit_note(self, tag, new_note):
        if tag in self.notes:
                self.notes[tag] = new_note
                return f"Note edited successfully for {str(self.name).title()} with tag '{tag}'"
        return f"Note with tag '{tag}' not found for {str(self.name).title()}'"


    def delete_note(self, tag):
     if tag in self.notes:
        self.notes.pop(tag, None)
        return f"All notes with tag '{tag}' deleted successfully for {str(self.name).title()}"
     return f"No notes found with tag '{tag}' for {str(self.name).title()}"



    def __str__(self):
        birthday_str = f", Birthday: {str(self.birthday)}" if self.birthday else ""
        notes_str = "\n".join([f"- {tag}: {note}" for tag, note in self.notes.items()])
        return f"\nContact name: {self.name.value}, Phone: {self.phone}: {birthday_str}\nAddress: {self.address}\nEmail: {self.email}\nNotes:\n{notes_str}"


class AddressBook(UserDict):
    def add_record(self, name, phone):
        record = Record(name)
        record.add_phone(phone)
        self.data[record.name.value] = record

    def get_birthdays_in_days(self, days_ahead):
        today = datetime.now().date()
        future_date = today + timedelta(days=days_ahead)
        birthdays = {}
        for name, record in self.data.items():
            if record.birthday:
                birthday_date = record.birthday.value.replace(year=today.year)
                days_until_birthday = (birthday_date - today).days
                if days_until_birthday == days_ahead:
                    birthdays[name] = birthday_date
        return birthdays

    def delete_contact(self, name):
        del self.data[name]
        return f"Contact '{name.title()}' deleted successfully."


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


def general_error(func):
    def inner(args, kwargs):
        try:
            return func(args, kwargs)
        except Exception as e:
            return e

    return inner


def valid_name(func):
    def inner(args, kwargs):
        try:
            return func(args, kwargs)
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
    name = args[0].strip().lower()
    phone = args[1].strip()
    if name in book:
        return f"\nUsername {name.title()} already exists"
    else:
        try:
            name = Name(name).value
            phone = Phone(phone).value
            book.add_record(name, phone)
            return f"Contact '{name.title()}' added successfully."
        except (NameError, NumberError) as e:
            return str(e)


@general_error
@general_error
def searchBy(args, book):
    criterion, *search_value = args
    search_value = " ".join(search_value)
    criterion = args[0].strip().lower()
    result = ""
    for name, record in book.items():
        if criterion == "phone" and record.phone.value == search_value:
            result += f"Name: {name.title()}, Phone: {record.phone}, Birthday: {record.birthday}, Address: {record.address}, Email: {record.email}\n"
        elif criterion == "name" and record.name.value == search_value.lower():
            result += f"Name: {name.title()}, Phone: {record.phone}, Birthday: {record.birthday}, Address: {record.address}, Email: {record.email}\n"
        elif (
            criterion == "birthday"
            and record.birthday
            and record.birthday.value
            == datetime.strptime(search_value, "%d.%m.%Y").date()
        ):
            result += f"Name: {name.title()}, Phone: {record.phone}, Birthday: {record.birthday}, Address: {record.address}, Email: {record.email}\n"
        elif (
            criterion == "address"
            and str(record.address).lower() == search_value.lower()
        ):
            result += f"Name: {name.title()}, Phone: {record.phone}, Birthday: {record.birthday}, Address: {record.address}, Email: {record.email}\n"
        elif criterion == "email" and str(record.email).lower() == search_value.lower():
            result += f"Name: {name.title()}, Phone: {record.phone}, Birthday: {record.birthday}, Address: {record.address}, Email: {record.email}\n"
    if result:
        return result
    else:
        return "No records found for the given criteria."


@general_error
@valid_name
def editBy(args, book):
    criterion, name, *new_value = args
    new_value = " ".join(new_value)
    name = name.strip().lower()

    if name in book:
        if criterion == "phone":
            book[name].phone = Phone(new_value)
            return f"Phone updated for {name.title()}\n"
        elif criterion == "birthday":
            book[name].birthday = Birthday(new_value)
            return f"Birthday updated for {name.title()}\n"
        elif criterion == "address":
            book[name].address = Address(new_value)
            return f"Address updated for {name.title()}\n"
        elif criterion == "email":
            book[name].email = Email(new_value)
            return f"Email updated for {name.title()}\n"
        else:
            return f"Field '{criterion}' cannot be changed.\n"
    else:
        raise KeyError


@general_error
@valid_name
def addBirthday(args, book):
    name = args[0].strip().lower()
    birthDate = args[1].strip()
    try:
        name = Name(name).value
        if name in book:
            return book[name].add_birthday(birthDate)
        else:
            raise KeyError
    except NameError as e:
        return str(e)


@general_error
@valid_name
def addAddress(args, book):
    name = args[0].strip().lower()
    address = " ".join(args[1:]).strip()
    try:
        name = Name(name).value
        if name in book:
            return book[name].add_address(address)
        else:
            raise KeyError
    except NameError as e:
        return str(e)


@general_error
@valid_name
def addEmail(args, book):
    name, email = args
    name = name.strip()
    try:
        name = Name(name).value
        if name in book:
            return book[name].add_email(email)
        else:
            raise KeyError
    except NameError as e:
        return str(e)
    
@general_error   
@valid_name
def addNote(args,book):
    name, tag, *note= args
    note = " ".join(note)
    if name in book:
        return book[name].add_note(tag,note)
    else:
        raise KeyError
    
@general_error   
@valid_name
def editNote(args,book):
    name, tag, *newNote=args
    newNote=" ".join(newNote)
    if name in book:
        return book[name].edit_note(tag, newNote)
    else:
        raise KeyError

@general_error
def searchNote(args,book):
    keywords=args
    keywords=" ".join(keywords)
    result= ""
    found_notes = {}
    for name, record in book.items():
         for tag, note in record.notes.items():
            if keywords.lower() in note.lower():
                result+= f"{record.name.value} has tag: {tag} with note: {note} \n"
    if found_notes is not "":
        return result
    else:
        return "No keyword found"

@general_error
@valid_name
def deleteNote(args,book):
    name, tag= args
    if name in book:
        return book[name].delete_note(tag)
    else:
        raise KeyError


@valid_name
@indexOutOfRange
def showBirthday(args, book):
    name = args[0].strip().lower()
    if name in book and book[name].birthday:
        return f"{name.title()}'s birthday is on {book[name].birthday.value.strftime('%d.%m.%Y')}\n"
    else:
        raise KeyError


def showBirthdaysInDays(book, days_ahead):
    birthdays = book.get_birthdays_in_days(days_ahead)
    result = ""
    if birthdays:
        result += f"\nBirthdays {days_ahead} days from now:\n"
        # Group contacts by birthday
        grouped_birthdays = {}
        for name, birthday_date in birthdays.items():
            day_month = birthday_date.strftime("%d.%m")
            weekday = birthday_date.strftime("%A")
            key = (weekday, day_month)
            if key not in grouped_birthdays:
                grouped_birthdays[key] = [name]
            else:
                grouped_birthdays[key].append(name)

        # Format output
        for (weekday, day_month), contacts in grouped_birthdays.items():
            result += f"\n[{day_month}] - {weekday} : "
            result += ", ".join(contacts).title()
            result += "\n"
    else:
        result += f"\nNo birthdays {days_ahead} days from now.\n"
    return result


def deleteContact(args, book):
    name = args[0].strip().lower()
    try:
        # Validate name input for alphabetic characters
        name = Name(name).value
        if name in book:
            return book.delete_contact(name)
    except (NameError, KeyError) as e:
        print(str(e))


############ SAVE FILE AS A DATABASE


def save_to_pickle(data, filename="data.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(data, f)


def load_from_pickle(filename="data.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Return an empty dictionary if the file doesn't exist


###########


def main():
    book = load_from_pickle()
    print(
        "\n\t\t#######################################\n\n\t\tWelcome to your Personal Assistant app!\n\n\t\t#######################################\n\n\t\tType Hello to start!\n\n"
    )
    while True:
        user_input = input("Enter a command: ")
        if not user_input:
            print('Please type Hello to see the menu options or "exit" to close.')
            continue
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print(
                "\n\n\t****** Thank you for using the Personal Assistant! ******\n\t\t\tSee you next time!\n\n"
            )
            save_to_pickle(book)
            break
        elif command == "hello":
            print(
                """
            \nTo continue, please choose one of the following options:\n
            ** Add a new contact                          >>> add [name] [phone-number]  
            ** Add address to a contact                   >>> add-address [name] [address]
            ** Add email to contact                       >>> add-email [name] [email]
            ** Add note to contact                        >>> add-note [name] [tag:in one word] [note:str]
            ** Edit Note                                  >>> edit-note [name] [tag] [new note]
            ** Search notes from all contact notes        >>> search-note [note]
            ** Delete note from a contact                 >>> delete-note [name] [tag]
            ** Edit an existing contact                   >>> edit-by [phone/email/address] [name] [phone-number/email-address/]
            ** Search for an existing contact             >>> search-by [name/email/phone] [contact-name/email-address/phone-number]
            ** Display all contacts from the phonebook    >>> all
            ** Add birthday for a contact                 >>> add-birthday [name] [DD.MM.YYYY]
            ** Show birthday for a contact                >>> show-birthday [name]
            ** Show birthdays in specified no days        >>> birthdays [number] *Number should be in the range 1-30
            ** Delete a contact from the address book     >>> delete [name]          
            ** Exit the application                       >>> close or exit
            """
            )
        elif command == "add":
            print(add_contact(args, book))
        elif command == "edit-by":
            print(editBy(args, book))
        elif command == "edit-note":
            print(editNote(args,book))
        elif command == "search-note":
            print(searchNote(args,book))
        elif command == "delete-note":
            print(deleteNote(args,book))
        elif command == "add-birthday":
            print(addBirthday(args, book))
        elif command == "add-address":
            print(addAddress(args, book))
        elif command == "add-email":
            print(addEmail(args, book))
        elif command == "add-note":
            print(addNote(args,book))
        elif command == "show-birthday":
            print(showBirthday(args, book))
        elif command == "birthdays":
            if args:
                days_input = args[0]
                if days_input.isdigit():  # Check if input contains digits only
                    days_ahead = int(days_input)
                    if 1 <= days_ahead <= 30:  # Check if days_ahead is within range
                        print(showBirthdaysInDays(book, days_ahead))
                    else:
                        print("\nPlease enter a number of days between 1 and 30.")
                else:
                    print("\nPlease enter a valid number of days.")
            else:
                print("\nPlease specify the number of days ahead.")
        elif command == "search-by":
            print(searchBy(args, book))
        elif command == "all":
            print("\n")
            for name, record in book.items():
                print(record)
        elif command == "delete":
            print(deleteContact(args, book))  # Command for deleting contact
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
