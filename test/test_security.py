import unittest
from flask import current_app
from app import create_app
from app.services import Security
from app.services.security import WerkzeugSecurity, PasslibSecurity
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
        security = Security(WerkzeugSecurity())
        encrypted_password = security.encrypt_password(self.PASSWORD)
        self.assertTrue(security.check_password(encrypted_password, self.PASSWORD))
        
    def test_security_passlib(self):
        security = Security(PasslibSecurity())
        encrypted_password = security.encrypt_password(self.PASSWORD)
        self.assertTrue(security.check_password(encrypted_password, self.PASSWORD))

if __name__ == '__main__':
    unittest.main()