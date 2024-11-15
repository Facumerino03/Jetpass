from dataclasses import dataclass
from app import db

@dataclass(init=True,eq=False)
class EmergencyEquipmentData(db.Model):
    '''
    Class representing emergency equipment data in the flight plans
    '''
    __tablename__ = "emergency_equipment_data"
    
    id:int = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    flight_plan:int = db.relationship('FlightPlan', back_populates='emergency_equipment_data', uselist=False)
    
    # Radio Equipment
    radio_uhf:bool = db.Column("radio_uhf", db.Boolean, nullable=False, default=False)  
    radio_vhf:bool = db.Column("radio_vhf", db.Boolean, nullable=False, default=False)  
    radio_elt:bool = db.Column("radio_elt", db.Boolean, nullable=False, default=False)  
    
    # Survival Equipment
    survival_equipment:bool = db.Column("survival_equipment", db.Boolean, nullable=False, default=False)
    survival_polar:bool = db.Column("survival_polar", db.Boolean, nullable=False, default=False)  
    survival_desert:bool = db.Column("survival_desert", db.Boolean, nullable=False, default=False) 
    survival_maritime:bool = db.Column("survival_maritime", db.Boolean, nullable=False, default=False)  
    survival_jungle:bool = db.Column("survival_jungle", db.Boolean, nullable=False, default=False) 
    
    # Jackets
    jackets:bool = db.Column("jackets", db.Boolean, nullable=False, default=False)  
    jackets_lights:bool = db.Column("jackets_lights", db.Boolean, nullable=False, default=False) 
    jackets_fluorescein:bool = db.Column("jackets_fluorescein", db.Boolean, nullable=False, default=False)  
    jackets_radio_uhf:bool = db.Column("jackets_radio_uhf", db.Boolean, nullable=False, default=False) 
    jackets_radio_vhf:bool = db.Column("jackets_radio_vhf", db.Boolean, nullable=False, default=False)
      
    # Dinghies
    dinghies:bool = db.Column("dinghies", db.Boolean, nullable=False, default=False)
    dinghies_number:int = db.Column("dinghies_number", db.Integer, nullable=False) 
    dinghies_capacity:int = db.Column("dinghies_capacity", db.Integer, nullable=False)  
    dinghies_cover:bool = db.Column("dinghies_cover", db.Boolean, nullable=False, default=False) 
    dinghies_cover_colour:str = db.Column("dinghies_cover_colour", db.String(100), nullable=False) 
    
    def __eq__(self, equipment: object) -> bool:
        return (
            self.id == equipment.id and
            self.flight_plan == equipment.flight_plan and
            self.radio_uhf == equipment.radio_uhf and
            self.radio_vhf == equipment.radio_vhf and
            self.radio_elt == equipment.radio_elt and
            self.survival_equipment == equipment.survival_equipment and
            self.survival_polar == equipment.survival_polar and
            self.survival_desert == equipment.survival_desert and
            self.survival_maritime == equipment.survival_maritime and
            self.survival_jungle == equipment.survival_jungle and
            self.jackets == equipment.jackets and
            self.jackets_lights == equipment.jackets_lights and
            self.jackets_fluorescein == equipment.jackets_fluorescein and
            self.jackets_radio_uhf == equipment.jackets_radio_uhf and
            self.jackets_radio_vhf == equipment.jackets_radio_vhf and
            self.dinghies_number == equipment.dinghies_number and
            self.dinghies == equipment.dinghies and
            self.dinghies_capacity == equipment.dinghies_capacity and
            self.dinghies_cover == equipment.dinghies_cover and
            self.dinghies_cover_colour == equipment.dinghies_cover_colour
        )