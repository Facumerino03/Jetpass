import os
import unittest
from flask import current_app
from app import create_app, db

class UserTestCase(unittest.TestCase):
    """
    Test User model
    Necesitamos aplicar principios como DRY (Don't Repeat Yourself) y KISS (Keep It Simple, Stupid).
    YAGNI (You Aren't Gonna Need It) y SOLID (Single Responsibility Principle).
    """
    def setUp(self):

        self.USERNAME_PRUEBA = 'pabloprats'
        self.EMAIL_PRUEBA = 'test@test.com'
        self.PASSWORD_PRUEBA = '123456'
        self.ADDRESS_PRUEBA = 'Address 1234'
        self.FIRSTNAME_PRUEBA = 'Pablo'
        self.LASTNAME_PRUEBA = 'Prats'
        self.PHONE_PRUEBA = '54260123456789'
        self.CITY_PRUEBA = 'San Rafael'
        self.COUNTRY_PRUEBA = 'Argentina'
        
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app(self):
        self.assertIsNotNone(current_app)
    
    def test_user(self):
        
        user = self.__get_user()
        
        self.assertEqual(user.email, self.EMAIL_PRUEBA)
        self.assertEqual(user.username, self.USERNAME_PRUEBA)
        self.assertEqual(user.password, self.PASSWORD_PRUEBA)
        self.assertIsNotNone(user.data)
        self.assertEqual(user.data.address, self.ADDRESS_PRUEBA)
        self.assertEqual(user.data.firstname, self.FIRSTNAME_PRUEBA)
        self.assertEqual(user.data.lastname, self.LASTNAME_PRUEBA)
        self.assertEqual(user.data.phone, self.PHONE_PRUEBA)

if __name__ == '__main__':
    unittest.main()