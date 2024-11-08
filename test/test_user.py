import unittest
from flask import current_app
from app import create_app, db
import os
from app.models import User
from app.repositories import UserRepository

repository = UserRepository()

class UserTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user(self):
        user = self.__new_user()
        self.assertIsNotNone(user)
        self.assertEqual(user.firstname, "Facundo")
        self.assertEqual(user.lastname, "Merino")
        self.assertEqual(user.dni, "26134242")
        self.assertEqual(user.email, "test@gmail.com")
        self.assertEqual(user.phone, "26134242")
        self.assertEqual(user.address, "Suite 951 312 Mark Summit, Shondamouth, UT 89664")
        self.assertEqual(user.state, "Utah")
        self.assertEqual(user.city, "Shondamouth")
        self.assertEqual(user.zipcode, "89664")

    def test_compare_user(self):
        user = self.__new_user()
        user2 = self.__new_user()
        self.assertEqual(user, user2)

    def test_save(self):
        user = self.__new_user()
        user_save = repository.save(user)
        self.assertIsNotNone(user_save)
        self.assertIsNotNone(user_save.id)
        self.assertGreater(user_save.id, 0)

    def test_find(self):
        user = self.__new_user()
        user_save = repository.save(user)
        self.assertIsNotNone(user_save)
        self.assertIsNotNone(user_save.id)
        self.assertGreater(user_save.id, 0)
        user = repository.find(user_save.id)
        self.assertIsNotNone(user)
        self.assertEqual(user.id, user_save.id)

    def test_find_all(self):
        user = self.__new_user()
        user2 = self.__new_user()
        user2.dni = "123456789"
        user2.email = "test2@gmail.com"
        user_save = repository.save(user)
        user2_save = repository.save(user2)
        self.assertIsNotNone(user_save)
        self.assertIsNotNone(user_save.id)
        self.assertGreater(user_save.id, 0)
        users = repository.find_all()
        self.assertIsNotNone(users)
        self.assertGreater(len(users), 1)

    def test_find_by(self):
        user = self.__new_user()
        user_save = repository.save(user)
        self.assertIsNotNone(user_save)
        self.assertIsNotNone(user_save.id)
        self.assertGreater(user_save.id, 0)
        users = repository.find_by(dni='26134242')
        self.assertIsNotNone(users)
        self.assertGreater(len(users), 0)

    def test_update(self):
        user = self.__new_user()
        user_save = repository.save(user)
        user_save.email = 'nuevo@gmail.com'
        user_save_update = repository.update(user_save, user_save.id)
        self.assertIsNotNone(user_save_update)
        self.assertEqual(user_save_update.email, 'nuevo@gmail.com')

    def test_delete(self):
        user = self.__new_user()
        user_save = repository.save(user)
        self.assertIsNotNone(user_save)
        self.assertIsNotNone(user_save.id)
        self.assertGreater(user_save.id, 0)
        repository.delete(user_save)
        user_delete = repository.find(user_save.id)
        self.assertIsNone(user_delete)

    def __new_user(self):
        user = User(
            firstname="Facundo",
            lastname="Merino",
            dni="26134242",
            email="test@gmail.com",
            phone="26134242",
            address="Suite 951 312 Mark Summit, Shondamouth, UT 89664",
            state="Utah",
            city="Shondamouth",
            zipcode="89664",
            password="f@dKhfi3h%Ym43r$3jM2"
        )
        return user

if __name__ == '__main__':
    unittest.main()