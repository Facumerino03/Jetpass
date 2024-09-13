from datetime import date, datetime
import unittest
from flask import current_app
from flask.cli import F
from app import create_app
from app import db
import os
from app.models import FlightPlan, flightplan
from app.repositories import FlightPlanRepository

repository = FlightPlanRepository()

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
    
    def test_flightplan(self):
        flight_plan = self.__new_flightplan()
        self.assertIsNotNone(flight_plan)
        self.assertEqual(flight_plan.pilot, "Pilot")
        self.assertEqual(flight_plan.requested_aerodrome, "Requested Aerodrome")
        self.assertEqual(flight_plan.departure_aerodrome, "Departure Aerodrome")
        self.assertEqual(flight_plan.first_alternative_aerodrome, "First Alternative Aerodrome")
        self.assertEqual(flight_plan.second_alternative_aerodrome, "Second Alternative Aerodrome")
        self.assertEqual(flight_plan.destination_aerodrome, "Destination Aerodrome")
        self.assertEqual(flight_plan.aircraft_registration, "Aircraft Registration")
        self.assertEqual(flight_plan.aircraft_type, "Aircraft Type")
        self.assertEqual(flight_plan.reason, "Reason")
        self.assertEqual(flight_plan.observations, "Observations")
        self.assertEqual(flight_plan.start_date, datetime.now())
        self.assertEqual(flight_plan.start_time_utc, datetime.now())
        self.assertEqual(flight_plan.end_date, datetime.now())
        self.assertEqual(flight_plan.end_time_utc, datetime.now())
        self.assertEqual(flight_plan.document_submission_date, datetime.now())
        self.assertEqual(flight_plan.document_submission_time, datetime.now())
        
    def test_compare_flightplan(self):
        flightplan = self.__new_flightplan()
        flightplan2 = self.__new_flightplan()
        self.assertEqual(flightplan, flightplan2)
    
    def test_save(self):
        flightplan = self.__new_flightplan()
        flightplan_save = repository.save(flightplan)
        self.assertIsNotNone(flightplan_save)
        self.assertIsNotNone(flightplan_save.id)
        self.assertGreater(flightplan_save.id, 0)
    
    def test_delete(self):
        flightplan = self.__new_flightplan()
        flightplan_save = repository.save(flightplan)
        self.assertIsNotNone(flightplan_save)
        self.assertIsNotNone(flightplan_save.id)
        self.assertGreater(flightplan_save.id, 0)
        flightplan_delete = repository.delete(flightplan_save)
        self.assertIsNone(flightplan_delete)
    
    def test_find(self):
        flightplan = self.__new_flightplan()
        flightplan_save = repository.save(flightplan)
        self.assertIsNotNone(flightplan_save)
        self.assertIsNotNone(flightplan_save.id)
        self.assertGreater(flightplan_save.id, 0)
        flightplan = repository.find(1)
        self.assertIsNotNone(flightplan)
        self.assertIsNotNone(flightplan_save.id)
        self.assertGreater(flightplan_save.id, 0)
    
    def test_find_all(self):
        flightplan = self.__new_flightplan()
        flightplan2 = self.__new_flightplan()
        flightplan2.pilot = "Pilot 2"
        flightplan2.requested_aerodrome = "Requested Aerodrome 2"
        flightplan2.departure_aerodrome = "Departure Aerodrome 2"
        flightplan2.first_alternative_aerodrome = "First Alternative Aerodrome 2"
        flightplan2.second_alternative_aerodrome = "Second Alternative Aerodrome 2"
        flightplan2.destination_aerodrome = "Destination Aerodrome 2"
        flightplan2.aircraft_registration = "Aircraft Registration 2"
        flightplan2.aircraft_type = "Aircraft Type 2"
        flightplan2.reason = "Reason 2"
        flightplan2.observations = "Observations 2"
        flightplan2.start_date = datetime.now()
        flightplan2.start_time_utc = datetime.now()
        flightplan2.end_date = datetime.now()
        flightplan2.end_time_utc = datetime.now()
        flightplan2.document_submission_date = datetime.now()
        flightplan2.document_submission_time = datetime.now()
        flightplan_save = repository.save(flightplan)
        flightplan2_save = repository.save(flightplan2)
        self.assertIsNotNone(flightplan_save)
        self.assertIsNotNone(flightplan_save.id)
        self.assertIsNotNone(flightplan2_save)
        self.assertIsNotNone(flightplan2_save.id)
        flightplans = repository.find_all()
        self.assertIsNotNone(flightplans)
        self.assertGreater(len(flightplans), 1)
    
    def test_find_by(self):
        flightplan = self.__new_flightplan()
        flightplan_save = repository.save(flightplan)
        self.assertIsNotNone(flightplan_save)
        self.assertIsNotNone(flightplan_save.id)
        self.assertGreater(flightplan_save.id, 0)
        flightplan = repository.find_by(pilot='Pilot')
        self.assertIsNotNone(flightplan)
        self.assertGreater(len(flightplan), 0)
    
    def test_update(self):
        flightplan = self.__new_flightplan()
        flightplan_save = repository.save(flightplan)
        flightplan_save.pilot = "Pilot 2"
        flightplan_update = repository.save(flightplan_save)
        self.assertIsNotNone(flightplan_update)
        self.assertEqual(flightplan_save.pilot, "Pilot 2")
        
    def __new_flightplan(self):
        flight_plan = FlightPlan()
        flight_plan.pilot = "Pilot"
        flight_plan.requested_aerodrome = "Requested Aerodrome"
        flight_plan.departure_aerodrome = "Departure Aerodrome"
        flight_plan.first_alternative_aerodrome = "First Alternative Aerodrome"
        flight_plan.second_alternative_aerodrome = "Second Alternative Aerodrome"
        flight_plan.destination_aerodrome = "Destination Aerodrome"
        flight_plan.aircraft_registration = "Aircraft Registration"
        flight_plan.aircraft_type = "Aircraft Type"
        flight_plan.start_date = datetime.now()
        flight_plan.start_time_utc = datetime.now()
        flight_plan.end_date = datetime.now()
        flight_plan.end_time_utc = datetime.now()
        flight_plan.reason = "Reason"
        flight_plan.observations = "Observations"
        flight_plan.document_submission_date = datetime.now()
        flight_plan.document_submission_time = datetime.now()
        return flight_plan
        

        
    

if __name__ == '__main__':
    unittest.main()