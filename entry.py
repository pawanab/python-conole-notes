#!/usr/bin/python3
import time
import getpass
# import traceback
from user import User
from notes import Notes
import os

MAX_USER_REG = 10
MAX_NOTES_PER_USER = 3


def view_notes(username):
    n = Notes(username)
    all_notes = n.read_notes()
    if all_notes is False:
        print('No notes exists for {}'.format(username))
        return False

    for savedtime, note in all_notes.items():
        print(time.strftime("%d %b %Y %I:%M %p",
                            time.localtime(int(savedtime))), note, sep=' : ')


def add_note(username):
    n = Notes(username)
    all_notes = n.read_notes()
    if all_notes and MAX_NOTES_PER_USER == len(all_notes):
        print(
            'You have reached the limit. Your oldest note will be deleted to save new.')
        n.delete_old_note(all_notes)

    new_note = take_input('Enter note to save ', 'note')
    if n.create_note(new_note):
        print('Note saved successfully.')
    else:
        print('something went wrong... please try again')


def logged_in_user_option(username):
    print("Welcome {}".format(username))
    print("Press 1 : see all previous notes",
          "Press 2 : Add new note",
          "Press 3 : Exit", sep="\n")

    while True:
        option = input(f'{username} > ')

        if '3' == option:
            break
        try:
            {
                '1': view_notes,
                '2': add_note
            }[option](username)
        except KeyError:
            print(str(option) + " is invalid! Please try again")


def login():
    username = take_input('username', 'User name')

    while True:
        password = getpass.getpass()
        if password:
            break
        print("Password can't be empty")

    username = username.lower()
    # validate user if it exists or not
    user_data = User.login(username, password)

    if user_data is False:
        print('User not exists or invalid username password')
    else:
        try:
            logged_in_user_option(user_data.get('username'))
        except Exception:
            print('Ooopss, sorry.')
        # log to know what went wrong(NEXT phase of dev.)


def take_input(field, label):
    while True:
        field_input = input(f'> {field}: ')
        if field_input:
            return field_input
        print("{} Can't be Empty.".format(label))


def is_registration_allowed(dir_name):
    users_count = countfiles_in_dir(dir_name)

    return False if users_count >= MAX_USER_REG else True


def register():

    if is_registration_allowed('./assests/users') is False:
        print('Sorry, You can not login, Max user registratin limit reach', end='\n\n')
        return False
    username = take_input('username', 'User Name')
    username = username.lower()

    username_taken = User.is_user_exists(username)
    if username_taken is True:
        print('user name already taken.. please try different')
        register()

    while True:
        password = getpass.getpass()
        if password:
            break
        print("Password can't be empty")

    user = User(username, password)
    is_saved = user.register()
    if is_saved:
        print('Registration successfull. You can Login')
        return True
    return False

# have to modify function to check only user file (json.enc files)


def countfiles_in_dir(dir_name):
    return len([name for name in os.listdir(dir_name)
                if os.path.isfile(os.path.join(dir_name, name))])


def select_option():
    print("Welcome to the system. Please register or login.")
    # print("Options: register | login | exit")

    while True:
        option = input('Options: register | login | exit > ')
        option = option.lower()

        if option == "exit":
            break
        try:
            {
                'login': login,
                'register': register
            }[option]()
        except KeyError:
            # traceback.print_exc()
            print(str(option) + " is invalid! Please try again")

    print('Shuting Down......')


if __name__ == "__main__":
    select_option()
