import logging
from typing import List
from app.models import EmergencyEquipmentData
from app import db
from app.repositories.base_repository import CreateAbstractRepository, ReadAbstractRepository

class EmergencyEquipmentDataRepository(CreateAbstractRepository, ReadAbstractRepository):
    '''
    Class representing the emergency equipment data repository (interacts with the database)
    '''
    def save(self, equipment_data: EmergencyEquipmentData) -> EmergencyEquipmentData:
        '''
        Saves an emergency equipment data to the database
        param:
            equipment_data: EmergencyEquipmentData
        return:
            EmergencyEquipmentData: The saved emergency equipment data
        '''
        db.session.add(equipment_data)
        db.session.commit()
        return equipment_data
      
    def find(self, id: int) -> EmergencyEquipmentData:
        '''
        Finds an emergency equipment data by its id
        param:
            id: int
        return:
            EmergencyEquipmentData: The emergency equipment data found
        '''
        result = None
        if id is not None:
            try:
                result = EmergencyEquipmentData.query.get(id)
            except Exception as e:
                logging.error(f'error getting emergency equipment data by id: {id}, {e}') 
        return result
    
    def find_all(self) -> List[EmergencyEquipmentData]:
        pass

    def find_by(self, **kargs) -> List[EmergencyEquipmentData]:
        pass