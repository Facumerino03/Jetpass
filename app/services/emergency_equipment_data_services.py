from typing import List
from app.models import EmergencyEquipmentData
from app.repositories import EmergencyEquipmentDataRepository

class EmergencyEquipmentDataServices:
    """Clase que se encarga del CRUD de los datos de equipo de emergencia"""
    
    def __init__(self):
        self.repository = EmergencyEquipmentDataRepository()

    def save(self, equipment_data: dict) -> EmergencyEquipmentData:
        emergency_equipment_data = EmergencyEquipmentData(
            radio_uhf=equipment_data['radio_uhf'],
            radio_vhf=equipment_data['radio_vhf'],
            radio_elt=equipment_data['radio_elt'],
            survival_equipment=equipment_data['survival_equipment'],
            survival_polar=equipment_data['survival_polar'],
            survival_desert=equipment_data['survival_desert'],
            survival_maritime=equipment_data['survival_maritime'],
            survival_jungle=equipment_data['survival_jungle'],
            jackets=equipment_data['jackets'],
            jackets_lights=equipment_data['jackets_lights'],
            jackets_fluorescein=equipment_data['jackets_fluorescein'],
            jackets_radio_uhf=equipment_data['jackets_radio_uhf'],
            jackets_radio_vhf=equipment_data['jackets_radio_vhf'],
            dinghies=equipment_data['dinghies'],
            dinghies_number=equipment_data['dinghies_number'],
            dinghies_capacity=equipment_data['dinghies_capacity'],
            dinghies_cover=equipment_data['dinghies_cover'],
            dinghies_cover_colour=equipment_data['dinghies_cover_colour']
        )
        return self.repository.save(emergency_equipment_data)

    def find(self, id: int) -> EmergencyEquipmentData:
        return self.repository.find(id)