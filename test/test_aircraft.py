from datetime import datetime
import unittest
from flask import current_app
from app import create_app, db
import os
from app.models import Aircraft
from app.repositories import AircraftRepository

repository = AircraftRepository()

class AircraftTestCase(unittest.TestCase):

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
    
    def test_aircraft(self):
        aircraft = self.__new_aircraft()
        self.assertIsNotNone(aircraft)
        self.assertEqual(aircraft.aircraft_identification, "ABC123")
        self.assertEqual(aircraft.aircraft_type, "B737")
        self.assertEqual(aircraft.wake_turbulence_category, "M")
        self.assertEqual(aircraft.equipment, "Standard")
        self.assertEqual(aircraft.endurance, datetime(2024, 11, 1, 12, 0))
        self.assertEqual(aircraft.passenger_capacity, "180")
        self.assertEqual(aircraft.crew_capacity, 6)
        self.assertEqual(aircraft.max_speed, 850)
        self.assertEqual(aircraft.aircraft_colour_and_marking, "White with blue stripes")
    
    def test_compare_aircraft(self):
        aircraft = self.__new_aircraft()
        aircraft2 = self.__new_aircraft()
        self.assertEqual(aircraft, aircraft2)
    
    def test_save(self):
        aircraft = self.__new_aircraft()
        aircraft_save = repository.save(aircraft)
        self.assertIsNotNone(aircraft_save)
        self.assertIsNotNone(aircraft_save.id)
        self.assertGreater(aircraft_save.id, 0)
    
    def test_find(self):
        aircraft = self.__new_aircraft()
        aircraft_save = repository.save(aircraft)
        self.assertIsNotNone(aircraft_save)
        self.assertIsNotNone(aircraft_save.id)
        self.assertGreater(aircraft_save.id, 0)
        aircraft = repository.find(aircraft_save.id)
        self.assertIsNotNone(aircraft)
        self.assertEqual(aircraft.id, aircraft_save.id)
    
    def test_find_all(self):
        aircraft = self.__new_aircraft()
        aircraft2 = self.__new_aircraft()
        aircraft2.aircraft_identification = "XYZ789"
        aircraft_save = repository.save(aircraft)
        aircraft2_save = repository.save(aircraft2)
        self.assertIsNotNone(aircraft_save)
        self.assertIsNotNone(aircraft_save.id)
        self.assertIsNotNone(aircraft2_save)
        self.assertIsNotNone(aircraft2_save.id)
        aircrafts = repository.find_all()
        self.assertIsNotNone(aircrafts)
        self.assertGreater(len(aircrafts), 1)
    
    def test_find_by(self):
        aircraft = self.__new_aircraft()
        aircraft_save = repository.save(aircraft)
        self.assertIsNotNone(aircraft_save)
        self.assertIsNotNone(aircraft_save.id)
        self.assertGreater(aircraft_save.id, 0)
        aircrafts = repository.find_by(aircraft_identification='ABC123')
        self.assertIsNotNone(aircrafts)
        self.assertGreater(len(aircrafts), 0)
    
    def test_update(self):
        aircraft = self.__new_aircraft()
        aircraft_save = repository.save(aircraft)
        aircraft_save.aircraft_identification = "XYZ789"
        aircraft_update = repository.update(aircraft_save)
        self.assertIsNotNone(aircraft_update)
        self.assertEqual(aircraft_update.aircraft_identification, "XYZ789")
    
    def test_delete(self):
        aircraft = self.__new_aircraft()
        aircraft_save = repository.save(aircraft)
        self.assertIsNotNone(aircraft_save)
        self.assertIsNotNone(aircraft_save.id)
        self.assertGreater(aircraft_save.id, 0)
        repository.delete(aircraft_save)
        aircraft_delete = repository.find(aircraft_save.id)
        self.assertIsNone(aircraft_delete)
    
    def __new_aircraft(self):
        return Aircraft(
            aircraft_identification="ABC123",
            aircraft_type="B737",
            wake_turbulence_category="M",
            equipment="Standard",
            endurance=datetime(2024, 11, 1, 12, 0),
            passenger_capacity="180",
            crew_capacity=6,
            max_speed=850,
            aircraft_colour_and_marking="White with blue stripes"
        )

if __name__ == '__main__':
    unittest.main()