from user import User
import os.path
import json
import calendar
import time
from CustomEncryption import encrypt_file, decrypt_file


class Notes:
    encryption_key = b'\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18'

    def __init__(self, username):
        self.username = username

    def read_notes(self):
        '''
        * returns all notes of the user
        *
        * @return mixed (dict if data exists else False)
        '''
        user_notes_file = self.create_file_name(self.username)
        try:
            os.path.isfile(user_notes_file+'.enc')
            decrypt_file(user_notes_file+'.enc', Notes.encryption_key)

        except FileNotFoundError:
            return False

        # decrypt_file(user_notes_file+'.enc', Notes.encryption_key)
        user_data_dict = dict()
        with open(user_notes_file, 'r', encoding='utf-8') as fin:
            for line in fin:
                key_val = line.split(':', 2)
                user_data_dict[key_val[0]] = key_val[1]

        os.remove(user_notes_file)
        return user_data_dict

    def create_file_name(self, filename, ecryption_ext_required=False):
        file_name = f'./assests/notes/{filename}.txt'
        if ecryption_ext_required:
            file_name = file_name + '.enc'
        return file_name

    def delete_old_note(self, notes):
        i = True
        user_notes_file = self.create_file_name(self.username)
        decrypt_file(user_notes_file+'.enc', Notes.encryption_key)

        f = open(user_notes_file, 'w+', encoding='utf-8')
        for k, v in notes.items():
            if i:
                i = False
                continue
            txt = '{}:{}'.format(k, v)
            f.writelines(txt)
        f.close()

        os.remove(user_notes_file+'.enc')
        encrypt_file(user_notes_file, Notes.encryption_key)
        os.remove(user_notes_file)

    def create_note(self, new_note):
        user_notes_file = self.create_file_name(self.username)
        try:
            os.path.isfile(user_notes_file+'.enc')
            decrypt_file(user_notes_file+'.enc', Notes.encryption_key)
            os.remove(user_notes_file + '.enc')
            f = open(user_notes_file, 'a+', encoding='utf-8')

        except FileNotFoundError:
            f = open(user_notes_file, 'w+', encoding='utf-8')

        epoch_curr = calendar.timegm(time.gmtime())
        txt = '{}:{}\n'.format(epoch_curr, new_note)
        f.writelines(txt)

        f.close()

        encrypt_file(user_notes_file, Notes.encryption_key)
        os.remove(user_notes_file)
        return True
