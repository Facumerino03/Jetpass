import unittest
from flask import current_app
from app import create_app, db
import os
from app.models import Pilot
from app.repositories import PilotRepository

repository = PilotRepository()

class PilotTestCase(unittest.TestCase):

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
    
    def test_pilot(self):
        pilot = self.__new_pilot()
        self.assertIsNotNone(pilot)
        self.assertEqual(pilot.first_name, "John")
        self.assertEqual(pilot.last_name, "Doe")
        self.assertEqual(pilot.license_number, "ABC123")
    
    def test_compare_pilot(self):
        pilot = self.__new_pilot()
        pilot2 = self.__new_pilot()
        self.assertEqual(pilot, pilot2)
    
    def test_save(self):
        pilot = self.__new_pilot()
        pilot_save = repository.save(pilot)
        self.assertIsNotNone(pilot_save)
        self.assertIsNotNone(pilot_save.id)
        self.assertGreater(pilot_save.id, 0)
    
    def test_find(self):
        pilot = self.__new_pilot()
        pilot_save = repository.save(pilot)
        self.assertIsNotNone(pilot_save)
        self.assertIsNotNone(pilot_save.id)
        self.assertGreater(pilot_save.id, 0)
        pilot = repository.find(pilot_save.id)
        self.assertIsNotNone(pilot)
        self.assertEqual(pilot.id, pilot_save.id)
    
    def test_find_all(self):
        pilot = self.__new_pilot()
        pilot2 = self.__new_pilot()
        pilot2.license_number = "XYZ789"
        pilot_save = repository.save(pilot)
        pilot2_save = repository.save(pilot2)
        self.assertIsNotNone(pilot_save)
        self.assertIsNotNone(pilot_save.id)
        self.assertIsNotNone(pilot2_save)
        self.assertIsNotNone(pilot2_save.id)
        pilots = repository.find_all()
        self.assertIsNotNone(pilots)
        self.assertGreater(len(pilots), 1)
    
    def test_find_by(self):
        pilot = self.__new_pilot()
        pilot_save = repository.save(pilot)
        self.assertIsNotNone(pilot_save)
        self.assertIsNotNone(pilot_save.id)
        self.assertGreater(pilot_save.id, 0)
        pilots = repository.find_by(first_name='John')
        self.assertIsNotNone(pilots)
        self.assertGreater(len(pilots), 0)
    
    def test_update(self):
        pilot = self.__new_pilot()
        pilot_save = repository.save(pilot)
        pilot_save.first_name = "Jane"
        pilot_update = repository.save(pilot_save)
        self.assertIsNotNone(pilot_update)
        self.assertEqual(pilot_save.first_name, "Jane")
        
    def test_update(self):
        pilot = self.__new_pilot()
        pilot_save = repository.save(pilot)
        pilot_save.first_name = "Jane"
        pilot_update = repository.update(pilot_save)
        self.assertIsNotNone(pilot_update)
        self.assertEqual(pilot_update.first_name, "Jane")
    
    def __new_pilot(self):
        return Pilot(
            first_name="John",
            last_name="Doe",
            license_number="ABC123"
        )

if __name__ == '__main__':
    unittest.main()