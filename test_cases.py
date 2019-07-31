import unittest
from user import User
import os
from entry import is_registration_allowed


class TestUser(unittest.TestCase):

    def test_username_exists(self):
        self.assertTrue(
            User.is_user_exists('pawan'))

    def test_username_available(self):
        self.assertFalse(
            User.is_user_exists('arora'))

    def test_registration_limit_exhausted(self):
        for i in range(10):
            with open(f'./assests/testusers/{i}.json', "w+", encoding='utf-8') as file:
                file.writelines(f'{i} \n')

        self.assertFalse(is_registration_allowed('./assests/testusers'))

    def test_registration_limit_exists(self):
        self.assertTrue(is_registration_allowed('./assests/testusers'))

    def test_successful_login(self):
        self.assertDictEqual(User.login('pawan', '123'), {
                             'username': 'pawan', 'password': '123'})

    def test_unsuccessful_login(self):
        self.assertFalse(User.login('pawan', '1233'))

    def tearDown(self):
        for the_file in os.listdir('./assests/testusers/'):
            file_path = os.path.join('./assests/testusers/', the_file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception:
            pass


if __name__ == '__main__':
    unittest.main()
