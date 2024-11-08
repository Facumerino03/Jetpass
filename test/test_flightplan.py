from datetime import datetime
import unittest
from flask import current_app
from app import create_app, db
import os
from app.models import FlightPlan, User, Pilot, Aircraft, Airport, EmergencyEquipmentData
from app.repositories import FlightPlanRepository, UserRepository, PilotRepository, AircraftRepository, AirportRepository, EmergencyEquipmentDataRepository

flightplan_repository = FlightPlanRepository()
user_repository = UserRepository()
pilot_repository = PilotRepository()
aircraft_repository = AircraftRepository()
airport_repository = AirportRepository()
equipment_repository = EmergencyEquipmentDataRepository()

class FlightPlanTestCase(unittest.TestCase):

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
        self.assertEqual(flight_plan.submission_date.date(), datetime.now().date())
        self.assertEqual(flight_plan.priority, "FF")
        self.assertEqual(flight_plan.address_to, "ATC")
        self.assertEqual(flight_plan.filing_time.date(), datetime.now().date())
        self.assertEqual(flight_plan.originator, "ORIG")
        self.assertEqual(flight_plan.message_type, "FPL")
        self.assertEqual(flight_plan.aircraft_id, 1)
        self.assertEqual(flight_plan.flight_rules, "I")
        self.assertEqual(flight_plan.flight_type, "S")
        self.assertEqual(flight_plan.number_of_aircraft, 1)
        self.assertEqual(flight_plan.pilot_id, 1)
        self.assertEqual(flight_plan.departure_aerodrome_id, 1)
        self.assertEqual(flight_plan.departure_time.date(), datetime.now().date())
        self.assertEqual(flight_plan.cruising_speed, "N0450")
        self.assertEqual(flight_plan.cruising_level, "FL350")
        self.assertEqual(flight_plan.route, "DCT JFK DCT LAX")
        self.assertEqual(flight_plan.destination_aerodrome_id, 2)
        self.assertEqual(flight_plan.total_estimated_elapsed_time, "0500")
        self.assertEqual(flight_plan.first_alternative_aerodrome_id, 3)
        self.assertEqual(flight_plan.second_alternative_aerodrome_id, 4)
        self.assertEqual(flight_plan.other_information, "NIL")
        self.assertEqual(flight_plan.persons_on_board, 180)
        self.assertEqual(flight_plan.emergency_equipment_data_id, 1)
        self.assertEqual(flight_plan.remarks, False)
        self.assertEqual(flight_plan.remarks_details, "NIL")
        self.assertEqual(flight_plan.filled_by_user_id, 1)
        self.assertEqual(flight_plan.document_signature_filename, "sign.png")
    
    def test_save(self):
        flight_plan = self.__new_flightplan()
        flight_plan_save = flightplan_repository.save(flight_plan)
        self.assertIsNotNone(flight_plan_save)
        self.assertIsNotNone(flight_plan_save.id)
        self.assertGreater(flight_plan_save.id, 0)
    
    def test_find(self):
        flight_plan = self.__new_flightplan()
        flight_plan_save = flightplan_repository.save(flight_plan)
        self.assertIsNotNone(flight_plan_save)
        self.assertIsNotNone(flight_plan_save.id)
        self.assertGreater(flight_plan_save.id, 0)
        flight_plan = flightplan_repository.find(flight_plan_save.id)
        self.assertIsNotNone(flight_plan)
        self.assertEqual(flight_plan.id, flight_plan_save.id)
    
    def test_find_all(self):
        flight_plan = self.__new_flightplan()
        flight_plan2 = self.__new_flightplan(unique=True)
        flight_plan_save = flightplan_repository.save(flight_plan)
        flight_plan2_save = flightplan_repository.save(flight_plan2)
        self.assertIsNotNone(flight_plan_save)
        self.assertIsNotNone(flight_plan_save.id)
        self.assertIsNotNone(flight_plan2_save)
        self.assertIsNotNone(flight_plan2_save.id)
        flight_plans = flightplan_repository.find_all()
        self.assertIsNotNone(flight_plans)
        self.assertGreater(len(flight_plans), 1)
    
    def test_find_by(self):
        flight_plan = self.__new_flightplan()
        flight_plan_save = flightplan_repository.save(flight_plan)
        self.assertIsNotNone(flight_plan_save)
        self.assertIsNotNone(flight_plan_save.id)
        self.assertGreater(flight_plan_save.id, 0)
        flight_plans = flightplan_repository.find_by(pilot_id=1)
        self.assertIsNotNone(flight_plans)
        self.assertGreater(len(flight_plans), 0)
    
    def test_update(self):
        flight_plan = self.__new_flightplan()
        flight_plan_save = flightplan_repository.save(flight_plan)
        
        # Crear un nuevo piloto para la actualización
        new_pilot = Pilot(first_name="Jane", last_name="Doe", license_number="XYZ789")
        new_pilot_save = pilot_repository.save(new_pilot)
        
        flight_plan_save.pilot_id = new_pilot_save.id
        flight_plan_update = flightplan_repository.update(flight_plan_save)
        self.assertIsNotNone(flight_plan_update)
        self.assertEqual(flight_plan_update.pilot_id, new_pilot_save.id)
    
    def test_delete(self):
        flight_plan = self.__new_flightplan()
        flight_plan_save = flightplan_repository.save(flight_plan)
        self.assertIsNotNone(flight_plan_save)
        self.assertIsNotNone(flight_plan_save.id)
        self.assertGreater(flight_plan_save.id, 0)
        flightplan_repository.delete(flight_plan_save)
        flight_plan_delete = flightplan_repository.find(flight_plan_save.id)
        self.assertIsNone(flight_plan_delete)
    
    def __new_flightplan(self, unique=False):
        user = User(
            firstname="John" if not unique else "Jane",
            lastname="Doe",
            dni="12345678" if not unique else "87654321",
            email="john.doe@example.com" if not unique else "jane.doe@example.com",
            phone="123456789",
            address="123 Main St",
            state="NY",
            city="New York",
            zipcode="10001",
            password="password"
        )
        user_save = user_repository.save(user)
        
        pilot = Pilot(first_name="John", last_name="Doe", license_number="ABC123" if not unique else "XYZ789")
        pilot_save = pilot_repository.save(pilot)
        
        aircraft = Aircraft(
            aircraft_identification="N12345" if not unique else "N54321",
            aircraft_type="B737",
            wake_turbulence_category="M",
            equipment="Standard",
            endurance=datetime(2024, 11, 1, 12, 0),
            passenger_capacity="180",
            crew_capacity=6,
            max_speed=850,
            aircraft_colour_and_marking="White with blue stripes"
        )
        aircraft_save = aircraft_repository.save(aircraft)
        
        departure_aerodrome = Airport(
            name="JFK" if not unique else "EWR",
            airport_code="JFK" if not unique else "EWR",
            city="New York" if not unique else "Newark",
            country="USA",
            south_coordinates=40.6413 if not unique else 40.6895,
            west_coordinates=-73.7781 if not unique else -74.1745,
            latitude=40.6413 if not unique else 40.6895,
            elevation=13 if not unique else 18,
            runway_length=4000 if not unique else 3000,
            traffic_type_allowed="Commercial"
        )
        departure_aerodrome_save = airport_repository.save(departure_aerodrome)
        
        destination_aerodrome = Airport(
            name="LAX" if not unique else "SFO",
            airport_code="LAX" if not unique else "SFO",
            city="Los Angeles" if not unique else "San Francisco",
            country="USA",
            south_coordinates=33.9416 if not unique else 37.6213,
            west_coordinates=-118.4085 if not unique else -122.3790,
            latitude=33.9416 if not unique else 37.6213,
            elevation=125 if not unique else 13,
            runway_length=3500 if not unique else 4000,
            traffic_type_allowed="Commercial"
        )
        destination_aerodrome_save = airport_repository.save(destination_aerodrome)
        
        first_alternative_aerodrome = Airport(
            name="ORD" if not unique else "ATL",
            airport_code="ORD" if not unique else "ATL",
            city="Chicago" if not unique else "Atlanta",
            country="USA",
            south_coordinates=41.9742 if not unique else 33.6407,
            west_coordinates=-87.9073 if not unique else -84.4277,
            latitude=41.9742 if not unique else 33.6407,
            elevation=204 if not unique else 313,
            runway_length=3200 if not unique else 3500,
            traffic_type_allowed="Commercial"
        )
        first_alternative_aerodrome_save = airport_repository.save(first_alternative_aerodrome)
        
        second_alternative_aerodrome = Airport(
            name="DFW" if not unique else "MIA",
            airport_code="DFW" if not unique else "MIA",
            city="Dallas" if not unique else "Miami",
            country="USA",
            south_coordinates=32.8998 if not unique else 25.7959,
            west_coordinates=-97.0403 if not unique else -80.2870,
            latitude=32.8998 if not unique else 25.7959,
            elevation=185 if not unique else 8,
            runway_length=3900 if not unique else 3200,
            traffic_type_allowed="Commercial"
        )
        second_alternative_aerodrome_save = airport_repository.save(second_alternative_aerodrome)
        
        equipment_data = EmergencyEquipmentData(
            radio_uhf=True,
            radio_vhf=False,
            radio_elt=True,
            survival_equipment=True,
            survival_polar=False,
            survival_desert=True,
            survival_maritime=False,
            survival_jungle=True,
            jackets=True,
            jackets_lights=False,
            jackets_fluorescein=True,
            jackets_radio_uhf=False,
            jackets_radio_vhf=True,
            dinghies=True,
            dinghies_number=2,
            dinghies_capacity=10,
            dinghies_cover=True,
            dinghies_cover_colour="Yellow"
        )
        equipment_data_save = equipment_repository.save(equipment_data)
        
        return FlightPlan(
            submission_date=datetime.now(),
            priority="FF",
            address_to="ATC",
            filing_time=datetime.now(),
            originator="ORIG",
            message_type="FPL",
            aircraft_id=aircraft_save.id,
            flight_rules="I",
            flight_type="S",
            number_of_aircraft=1,
            pilot_id=pilot_save.id,
            departure_aerodrome_id=departure_aerodrome_save.id,
            departure_time=datetime.now(),
            cruising_speed="N0450",
            cruising_level="FL350",
            route="DCT JFK DCT LAX",
            destination_aerodrome_id=destination_aerodrome_save.id,
            total_estimated_elapsed_time="0500",
            first_alternative_aerodrome_id=first_alternative_aerodrome_save.id,
            second_alternative_aerodrome_id=second_alternative_aerodrome_save.id,
            other_information="NIL",
            persons_on_board=180,
            emergency_equipment_data_id=equipment_data_save.id,
            remarks=False,
            remarks_details="NIL",
            filled_by_user_id=user_save.id,
            document_signature_filename="sign.png"
        )

if __name__ == '__main__':
    unittest.main()