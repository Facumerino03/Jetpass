import unittest
from flask import current_app
from app import create_app
from app.services import Security
import os

class AppTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.PASSWORD = '123456'

    def tearDown(self):
        self.app_context.pop()

    def test_app(self):
        self.assertIsNotNone(current_app)
        
    def test_security_standard(self):
        encrypted_password = Security.encrypt_password(self.PASSWORD)
        self.assertTrue(Security.password_check(encrypted_password, self.PASSWORD))
        
    def test_security_passlib(self):
        encrypted_password = Security.encrypt_password_passlib(self.PASSWORD)
        self.assertTrue(Security.password_check_passlib(encrypted_password, self.PASSWORD))

if __name__ == '__main__':
    unittest.main()