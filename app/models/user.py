from dataclasses import dataclass
from app import db

@dataclass(init=True,eq=False)
class User(db.Model):
    '''
    Class representing a user of the system with different profiles.
    '''
    __tablename__ = "users"
    
    id:int = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    firstname:str = db.Column("first name", db.String(100), nullable=False)
    lastname:str = db.Column("last name", db.String(100), nullable=False)
    dni:str = db.Column("dni", db.String(100), unique=True, nullable=False)
    email:str = db.Column("email", db.String(250), unique=True, nullable=False)
    phone:str = db.Column("phone number", db.String(100), unique=False, nullable=False)
    address:str = db.Column("address", db.String(250), nullable=False)
    state:str = db.Column("state", db.String(100), nullable=False)
    city:str = db.Column("city", db.String(100), nullable=False)
    zipcode:str = db.Column("zipcode", db.String(100), nullable=False)
    password:str = db.Column("password", db.String(254), nullable=False)
    
    def __eq__(self, user: object) -> bool:
        return (
            self.id == user.id and
            self.email == user.email and
            self.dni == user.dni and
            self.firstname == user.firstname and
            self.lastname == user.lastname and
            self.phone == user.phone and
            self.address == user.address and
            self.state == user.state and
            self.city == user.city and
            self.zipcode == user.zipcode
        )
        
    

    
    