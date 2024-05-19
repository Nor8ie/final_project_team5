# Python "Personal Assistant" final_project TEAM 5 (members: Bogdan Munteanu, Victoria Dumitrescu, Norbert Lang)

The present Personal Assistant application serves as a tool for storing and managing contacts along with a series of notes associated to them. The assistant is designed for easy access to a contacts’ details such as: phone number, birthday, email address, or other information through notes. Notes can store information such as, for example, interests, hobbies, or food tastes.
Here is an overview of the features and usage of this application:

• Contact Management:
Add Contacts: Store contacts with details such as names, emails, phone numbers, addresses, and birthdays.
Search Contacts: Find contacts by name, phone number, email, or address.
Edit and Delete Contacts: Modify existing contact details or remove contacts from the database.
Validate Contact Information: Ensure correct formatting of phone numbers and emails during entry.

• Notes Management:
Add Notes: Attach text-based notes to individual contacts, categorized by certain tags for easy identification.
Search, Edit, and Delete Notes: Perform operations on notes associated with contacts.
• Birthday Reminders:
Upcoming Birthdays: Display a list of contacts whose birthdays are within a specified number of days from the current date. The user specifies this number of days for his own preference.

• Storage and later access to the information:
Data Storage: All contacts and notes are stored persistently on the hard disk using Python's pickle library.
Automatic Saving: Changes to the contact book and notes are automatically saved to ensure data integrity.

Short guide on how to use the application:
==> Adding a Contact:
Use the add [name] [phone-number] command to create a new contact.
Optionally, add details such as address or email using the following commands:
add-address [name] [address]
add-email [name] [email]

==> Searching for Contacts:
Locate contacts by name, phone number, email, or address using the search-by [name] or [email] or [phone] or [address] or [birthday] and [search value] command.
For showing all the contacts saved use command all
If the user wants to delete the contact from the database can use the delete [name] command.

==> Managing contacts:
The user can edit an existing contact using command edit-by [phone] or [birthday] or [email] or [address], followed by [name] and [new value]

==> Managing Notes:
Attach notes to contacts using add-note [name] [tag] [note].
Attention! [tag] is one single word that describes the category of the subject introduced in the [note] field.
Perform operations like search, edit, or delete notes associated with contacts using the following commands:
edit-note [name] [tag] [new note]
search-note [keyword as text input]
delete-note [name] [tag]

==> Birthday Notifications:
Users can add birthdays to existing contacts with the command: add-birthday [name] [DD.MM.YYYY]
View upcoming birthdays by specifying the number of days ahead with the birthdays [days-ahead] command.
If the user wants a specific person’s birthday they can use show-birthday [name]

==> Exiting the Application:
Use the close or exit command to save changes and close the Personal Assistant.

Disclaimer:
This Personal Assistant application is the subject of a homework assignment.
