import unittest
from flask import current_app
from app import create_app, db
import os
from app.models import EmergencyEquipmentData
from app.repositories import EmergencyEquipmentDataRepository

repository = EmergencyEquipmentDataRepository()

class EmergencyEquipmentDataTestCase(unittest.TestCase):

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
    
    def test_emergency_equipment_data(self):
        equipment_data = self.__new_emergency_equipment_data()
        self.assertIsNotNone(equipment_data)
        self.assertEqual(equipment_data.radio_uhf, True)
        self.assertEqual(equipment_data.radio_vhf, False)
        self.assertEqual(equipment_data.radio_elt, True)
        self.assertEqual(equipment_data.survival_equipment, True)
        self.assertEqual(equipment_data.survival_polar, False)
        self.assertEqual(equipment_data.survival_desert, True)
        self.assertEqual(equipment_data.survival_maritime, False)
        self.assertEqual(equipment_data.survival_jungle, True)
        self.assertEqual(equipment_data.jackets, True)
        self.assertEqual(equipment_data.jackets_lights, False)
        self.assertEqual(equipment_data.jackets_fluorescein, True)
        self.assertEqual(equipment_data.jackets_radio_uhf, False)
        self.assertEqual(equipment_data.jackets_radio_vhf, True)
        self.assertEqual(equipment_data.dinghies, True)
        self.assertEqual(equipment_data.dinghies_number, 2)
        self.assertEqual(equipment_data.dinghies_capacity, 10)
        self.assertEqual(equipment_data.dinghies_cover, True)
        self.assertEqual(equipment_data.dinghies_cover_colour, "Yellow")
    
    def test_save(self):
        equipment_data = self.__new_emergency_equipment_data()
        equipment_data_save = repository.save(equipment_data)
        self.assertIsNotNone(equipment_data_save)
        self.assertIsNotNone(equipment_data_save.id)
        self.assertGreater(equipment_data_save.id, 0)
    
    def test_find(self):
        equipment_data = self.__new_emergency_equipment_data()
        equipment_data_save = repository.save(equipment_data)
        self.assertIsNotNone(equipment_data_save)
        self.assertIsNotNone(equipment_data_save.id)
        self.assertGreater(equipment_data_save.id, 0)
        equipment_data = repository.find(equipment_data_save.id)
        self.assertIsNotNone(equipment_data)
        self.assertEqual(equipment_data.id, equipment_data_save.id)
    
    def __new_emergency_equipment_data(self):
        return EmergencyEquipmentData(
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

if __name__ == '__main__':
    unittest.main()