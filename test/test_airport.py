import unittest
from flask import current_app
from app import create_app, db
import os
from app.models import Airport
from app.repositories import AirportRepository
from app.models.enums import TrafficTypeAllowedEnum

repository = AirportRepository()

class AirportTestCase(unittest.TestCase):

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
    
    def test_airport(self):
        airport = self.__new_airport()
        self.assertIsNotNone(airport)
        self.assertEqual(airport.name, "John F. Kennedy International Airport")
        self.assertEqual(airport.airport_code, "JFK")
        self.assertEqual(airport.city, "New York")
        self.assertEqual(airport.country, "USA")
        self.assertEqual(airport.south_coordinates, 40.6413)
        self.assertEqual(airport.west_coordinates, -73.7781)
        self.assertEqual(airport.latitude, 40.6413)
        self.assertEqual(airport.elevation, 13)
        self.assertEqual(airport.runway_length, 4000)
        self.assertEqual(airport.traffic_type_allowed, TrafficTypeAllowedEnum.INTERNATIONAL)
    
    def test_compare_airport(self):
        airport = self.__new_airport()
        airport2 = self.__new_airport()
        self.assertEqual(airport, airport2)
    
    def test_save(self):
        airport = self.__new_airport()
        airport_save = repository.save(airport)
        self.assertIsNotNone(airport_save)
        self.assertIsNotNone(airport_save.id)
        self.assertGreater(airport_save.id, 0)
    
    def test_find(self):
        airport = self.__new_airport()
        airport_save = repository.save(airport)
        self.assertIsNotNone(airport_save)
        self.assertIsNotNone(airport_save.id)
        self.assertGreater(airport_save.id, 0)
        airport = repository.find(airport_save.id)
        self.assertIsNotNone(airport)
        self.assertEqual(airport.id, airport_save.id)
    
    def test_find_all(self):
        airport = self.__new_airport()
        airport2 = self.__new_airport()
        airport2.airport_code = "LAX"
        airport2.traffic_type_allowed = TrafficTypeAllowedEnum.INTERNATIONAL
        airport_save = repository.save(airport)
        airport2_save = repository.save(airport2)
        self.assertIsNotNone(airport_save)
        self.assertIsNotNone(airport_save.id)
        self.assertIsNotNone(airport2_save)
        self.assertIsNotNone(airport2_save.id)
        airports = repository.find_all()
        self.assertIsNotNone(airports)
        self.assertGreater(len(airports), 1)
    
    def test_find_by(self):
        airport = self.__new_airport()
        airport_save = repository.save(airport)
        self.assertIsNotNone(airport_save)
        self.assertIsNotNone(airport_save.id)
        self.assertGreater(airport_save.id, 0)
        airports = repository.find_by(airport_code='JFK')
        self.assertIsNotNone(airports)
        self.assertGreater(len(airports), 0)
    
    def test_update(self):
        airport = self.__new_airport()
        airport_save = repository.save(airport)
        airport_save.name = "Los Angeles International Airport"
        airport_update = repository.update(airport_save, airport_save.id)
        self.assertIsNotNone(airport_update)
        self.assertEqual(airport_update.name, "Los Angeles International Airport")
    
    def test_delete(self):
        airport = self.__new_airport()
        airport_save = repository.save(airport)
        self.assertIsNotNone(airport_save)
        self.assertIsNotNone(airport_save.id)
        self.assertGreater(airport_save.id, 0)
        repository.delete(airport_save)
        airport_delete = repository.find(airport_save.id)
        self.assertIsNone(airport_delete)
    
    def __new_airport(self):
        return Airport(
            name="John F. Kennedy International Airport",
            airport_code="JFK",
            city="New York",
            country="USA",
            south_coordinates=40.6413,
            west_coordinates=-73.7781,
            latitude=40.6413,
            elevation=13,
            runway_length=4000,
            traffic_type_allowed=TrafficTypeAllowedEnum.INTERNATIONAL
        )

if __name__ == '__main__':
    unittest.main()