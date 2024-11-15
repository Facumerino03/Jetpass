from abc import ABC, abstractmethod
from typing import List
from app import db
from flask_sqlalchemy import model # type: ignore

class CreateAbstractRepository(ABC):
    @abstractmethod
    def save(self, model:db.Model) -> db.Model: # type: ignore
        pass
    
class ReadAbstractRepository(ABC):
    @abstractmethod
    def find_all(self) -> List[db.Model]: # type: ignore
        pass
    
    @abstractmethod
    def find_by(self, **kargs) -> List[db.Model]: # type: ignore
        pass
    
    @abstractmethod
    def find(self, id:int) -> db.Model: # type: ignore
        pass

class UpdateAbstractRepository(ABC):
    @abstractmethod
    def update(self, model:db.Model) -> db.Model: # type: ignore
        pass

class DeleteAbstractRepository(ABC):
    @abstractmethod
    def delete(self, model:db.Model) -> db.Model: # type: ignore
        pass

