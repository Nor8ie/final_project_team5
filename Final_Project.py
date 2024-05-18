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
                raise NameError("Name must contain only alphabetic characters.\n")
        except ValueError as e:
            raise e


class Phone(Field):
    def __init__(self, value):
        if len(value) == 10 and value.isdigit():
            super().__init__(value)
        else:
            raise NumberError("Number must be of 10 digits.\n")


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Birthday must be in DD.MM.YYYY format.\n")


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
            raise ValueError(
                "Email is not correct. It must include the @ sign and at least one '.' after it.\n"
            )


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
        return f"Email added for {str(self.name).title()}\n"

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        return f"Birthday added for {str(self.name).title()}\n"

    def add_note(self, tag="General", note="None"):
        if tag not in self.notes:
            self.notes[tag] = note
            return f"Note added for {str(self.name).title()} with tag '{tag}'\n"
        return f"Note with tag '{tag}' already exists. Try another tag\n"

    def edit_note(self, tag, new_note):
        if tag in self.notes:
            self.notes[tag] = new_note
            return f"Note edited successfully for {str(self.name).title()} with tag '{tag}'\n"
        return f"Note with tag '{tag}' was not found for {str(self.name).title()}\n"

    def delete_note(self, tag):
        if tag in self.notes:
            self.notes.pop(tag, None)
            return f"All notes with tag '{tag}' deleted successfully for {str(self.name).title()}\n"
        return f"No notes found with tag '{tag}' for {str(self.name).title()}\n"

    def __str__(self):
        birthday_str = (
            f", Birthday: {self.birthday.value:%d.%m.%Y}" if self.birthday else ""
        )
        notes_str = "\n".join([f"- {tag}: {note}" for tag, note in self.notes.items()])
        return f"Contact name: {str(self.name.value).title()}, Phone: {self.phone}{birthday_str}\nAddress: {self.address}\nEmail: {self.email}\nNotes:\n{notes_str}\n"


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
        return f"Contact '{name.title()}' deleted successfully.\n"


################################# EXCEPTIONS HANDLERS #################################


def input_error(func):
    def inner(args, kwargs):
        try:
            return func(args, kwargs)
        except ValueError as e:
            return e
        except Exception:
            return "Give me name and phone please.\n"

    return inner


def indexOutOfRange(func):
    def inner(args, kwargs):
        try:
            return func(args, kwargs)
        except IndexError as e:
            return "index out of bounds, maybe the value does not exist.\n"
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
            return "The name does not exist.\n"

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
    if criterion in ["name", "phone", "birthday", "address", "email"]:
        for name, record in book.items():
            if criterion == "phone":
                try:
                    search_value = Phone(search_value).value
                    if record.phone.value == search_value:
                        birthday_str = (
                            f"{record.birthday.value:%d.%m.%Y}"
                            if record.birthday
                            else "N/A"
                        )
                        result += f"Contact: {name.title()}, Phone: {record.phone}, Birthday: {birthday_str}, Address: {record.address}, Email: {record.email}\n"
                except NumberError as e:
                    return str(e)
            elif criterion == "name":
                if not search_value.isalpha():
                    return "The name must be entered with characters only.\n"
                elif (
                    search_value.isalpha() and record.name.value == search_value.lower()
                ):
                    birthday_str = (
                        f"{record.birthday.value:%d.%m.%Y}"
                        if record.birthday
                        else "N/A"
                    )
                    result += f"Contact: {name.title()}, Phone: {record.phone}, Birthday: {birthday_str}, Address: {record.address}, Email: {record.email}\n"

            elif criterion == "birthday":
                try:
                    search_value_date = datetime.strptime(
                        search_value, "%d.%m.%Y"
                    ).date()
                    if record.birthday and record.birthday.value == search_value_date:
                        birthday_str = (
                            f"{record.birthday.value:%d.%m.%Y}"
                            if record.birthday
                            else "N/A"
                        )
                        result += f"Contact: {name.title()}, Phone: {record.phone}, Birthday: {birthday_str}, Address: {record.address}, Email: {record.email}\n"
                except ValueError as e:
                    return str(e)
            elif (
                criterion == "address"
                and str(record.address).lower() == search_value.strip().lower()
            ):
                birthday_str = (
                    f"{record.birthday.value:%d.%m.%Y}" if record.birthday else "N/A"
                )
                result += f"Contact: {name.title()}, Phone: {record.phone}, Birthday: {birthday_str}, Address: {record.address}, Email: {record.email}\n"
            elif criterion == "email":
                try:
                    search_value = Email(search_value).value
                    if (
                        str(record.email) == str(search_value).lower()
                    ):  # str(record.email).lower() == search_value.lower()
                        birthday_str = (
                            f"{record.birthday.value:%d.%m.%Y}"
                            if record.birthday
                            else "N/A"
                        )
                        result += f"Contact: {name.title()}, Phone: {record.phone}, Birthday: {birthday_str}, Address: {record.address}, Email: {record.email}\n"
                except ValueError as e:
                    return str(e)
        if result:
            return result
        else:
            return "No records found for the given criteria.\n"
    else:
        return "Please provide a valid format: search-by [name] or [email] or [phone] or [address] or [birthday] and [value].\n"


@general_error
@valid_name
def editBy(args, book):
    criterion, name, *new_value = args
    new_value = " ".join(new_value)
    name = name.strip().lower()

    try:
        name = Name(name).value
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
    except NameError as e:
        return str(e)


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
    name = name.strip().lower()
    email = email.strip().lower()
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
def addNote(args, book):
    name, tag, *note = args
    note = " ".join(note)
    try:
        name = Name(name).value
        if name in book:
            return book[name].add_note(tag, note)
        else:
            raise KeyError
    except NameError as e:
        return str(e)


@general_error
@valid_name
def editNote(args, book):
    name, tag, *newNote = args
    newNote = " ".join(newNote)
    try:
        name = Name(name).value
        if name in book:
            return book[name].edit_note(tag, newNote)
        else:
            raise KeyError
    except NameError as e:
        return str(e)


@general_error
def searchNote(args, book):
    keywords = args
    keywords = " ".join(keywords)
    result = ""
    found_notes = {}
    for name, record in book.items():
        for tag, note in record.notes.items():
            if keywords.lower() in note.lower():
                result += (
                    f"{str(record.name).title()} has tag: {tag} with note: {note}\n"
                )
    if result:
        return result
    else:
        return "The keyword you are searching for does not exist.\n"


@general_error
@valid_name
def deleteNote(args, book):
    name, tag = args
    try:
        name = Name(name).value
        if name in book:
            return book[name].delete_note(tag)
        else:
            raise KeyError
    except NameError as e:
        return str(e)


@valid_name
@indexOutOfRange
def showBirthday(args, book):
    name = args[0].strip().lower()
    try:
        name = Name(name).value
        if name in book and book[name].birthday:
            return f"{name.title()}'s birthday is on {book[name].birthday.value.strftime('%d.%m.%Y')}\n"
        else:
            raise KeyError
    except NameError as e:
        return str(e)


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
        result += f"No birthdays {days_ahead} days from today.\n"
    return result


def deleteContact(args, book):
    name = args[0].strip().lower()
    try:
        # Validate name input for alphabetic characters
        name = Name(name).value
        if name in book:
            return book.delete_contact(name)
    except (NameError, KeyError) as e:
        return str(e)


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
            print('Please type Hello to see the menu options or "exit" to close.\n')
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
            ** Add email to a contact                     >>> add-email [name] [email]
            ** Add note to a contact                      >>> add-note [name] [tag: one keyword] [note: text]
            ** Edit Note                                  >>> edit-note [name] [tag] [new note]
            ** Search notes from all contacts             >>> search-note [keyword]
            ** Delete note from a contact                 >>> delete-note [name] [tag]
            ** Edit an existing contact                   >>> edit-by [phone] or [birthday] or [email] or [address], followed by [name] and [new value]
            ** Search for an existing contact             >>> search-by [name] or [email] or [phone] or [address] or [birthday] and [value]
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
            if len(args) < 3:
                print(
                    "Please type the edit-by, option from [phone] or [birthday] or [email] or [address], followed by [name] and [new value].\n"
                )
            else:
                print(editBy(args, book))
        elif command == "edit-note":
            if len(args) < 3:
                print(
                    "Please provide the contact name, the tag and the note as text.\n"
                )
            else:
                print(editNote(args, book))
        elif command == "search-note":
            if len(args) < 1:
                print("Please provide the keyword for your search.\n")
            else:
                print(searchNote(args, book))
        elif command == "delete-note":
            if len(args) == 2:
                print(deleteNote(args, book))
            else:
                print(
                    "Please provide the contact name and tag for the note to delete.\n"
                )
        elif command == "add-birthday":
            if len(args) == 2:
                print(addBirthday(args, book))
            else:
                print(
                    "Please provide a contact name and a birthday in format DD.MM.YYYY \n"
                )
        elif command == "add-address":
            if len(args) < 2:
                print("Please provide the contact name and address.\n")
            else:
                print(addAddress(args, book))
        elif command == "add-email":
            if len(args) == 2:
                print(addEmail(args, book))
            else:
                print("Please provide the contact name and email address.\n")
        elif command == "add-note":
            if len(args) < 3:
                print(
                    "Please provide the contact name, a keyword for tag and the note as text.\n"
                )
            else:
                print(addNote(args, book))
        elif command == "show-birthday":
            if len(args) == 1:
                print(showBirthday(args, book))
            else:
                print("Please provide the contact name to retrieve the birthday.\n")
        elif command == "birthdays":
            if args:
                days_input = args[0]
                if days_input.isdigit():  # Check if input contains digits only
                    days_ahead = int(days_input)
                    if 1 <= days_ahead <= 30:  # Check if days_ahead is within range
                        print(showBirthdaysInDays(book, days_ahead))
                    else:
                        print("Please enter a number of days between 1 and 30.\n")
                else:
                    print("Please enter a valid number of days.\n")
            else:
                print("Please specify the number of days ahead.\n")
        elif command == "search-by":
            if len(args) >= 2:
                print(searchBy(args, book))
            else:
                print(
                    "Please provide the search option [name] or [email] or [phone] or [address] or [birthday] and [value].\n"
                )

        elif command == "all":
            print("\n")
            for name, record in book.items():
                print(record)
            print("\n")
        elif command == "delete":
            if args:
                print(deleteContact(args, book))  # Command for deleting contact
            else:
                print("Please provide the contact name you want to discard.\n")
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
