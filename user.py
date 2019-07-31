import json
import os.path
from CustomEncryption import encrypt_file, decrypt_file


class User:
    encryption_key = b'\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18'

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def login(username, password):
        user_file = User.create_file_name(User, username)
        try:
            # check if file exists else throw execption automaticaly
            os.path.isfile(user_file)
            # decrypt file to authenticate
            decrypt_file(user_file+'.enc', User.encryption_key)
            connection_file = open(user_file, 'r', encoding='utf-8')
            user_data_dict = json.load(connection_file)
            connection_file.close()

            os.remove(user_file)
            if user_data_dict and username == user_data_dict.get('username') and password == user_data_dict.get('password'):
                return user_data_dict
            return False
        except FileNotFoundError:
            return False

    def register(self):
        user_file = self.create_file_name(self.username)
        try:
            with open(user_file, "x", encoding='utf-8') as file:
                json.dump({"username": self.username,
                           "password": self.password}, file)
            encrypt_file(user_file, User.encryption_key)
            os.remove(user_file)
            return True
        except Exception:
            os.remove(user_file)
            return False

    @staticmethod
    def is_user_exists(username):
        user_file = User.create_file_name(User, username, True)
        try:
            return True if os.path.isfile(user_file) else False
        except FileNotFoundError:
            return False

    def create_file_name(self, filename, ecryption_ext_required=False):
        file_name = f'./assests/users/{filename}.json'
        if ecryption_ext_required:
            file_name = file_name + '.enc'
        return file_name
