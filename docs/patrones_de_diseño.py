from asyncio import selector_events
from dataclasses import dataclass
from datetime import datetime, timezone
from time import sleep

@dataclass(init=False)
class Vuelo:
    def __init__(self):
        self.hr = datetime.now(timezone.utc)
    
    def get_hora_creacion(self):
        return self.hr
    
@dataclass(init=False)
class Hora():
    def __init__(self):
        self.vuelo = Vuelo()

class HoraSingleton():
    FLAG = False
    DATA = None
    def __init__(self):
        #aca iria un bloqueo para evitar concurrencia
        if HoraSingleton.FLAG == False:
           self.vuelo = Vuelo()
           HoraSingleton.DATA = self
           HoraSingleton.FLAG = True
    
    @staticmethod
    def instance():
        if HoraSingleton.FLAG == False:
            return HoraSingleton()
        else:
            return HoraSingleton.DATA
            
    
    def get_hora_vuelo(self):
        return self.vuelo.get_hora_creacion()
    
    

if __name__ == '__main__':
    hora1 = HoraSingleton.instance()
    sleep(2)
    hora2 = HoraSingleton.instance()
    sleep(2)
    hora3 = HoraSingleton.instance()
    if hora1 == hora2 and hora2 == hora3:
        print('Es el mismo objeto')
    else:
        print('No es el mismo objeto')
    