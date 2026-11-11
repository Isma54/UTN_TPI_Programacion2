from abc import ABC,abstractmethod
from datetime import datetime

class Base(ABC):
    CONTADOR_ID = 0
    def __init__(self)->None:
        Base.CONTADOR_ID += 1
        self.__id = Base.CONTADOR_ID
        self.__eliminado = False
        self.__creado_en : datetime = datetime.now()

    @property
    def id(self)->int:
        return self.__id
    @property
    def eliminado(self)->bool:
        return self.__eliminado
    @property
    def creado_en(self)->datetime:
        return self.__creado_en

    def eliminar(self)->None:
        self.__eliminado = True

    def __eq__(self, otro:Base)->bool:
        if not isinstance(otro,Base):
            return False
        return self.id == otro.id

    def __hash__(self)->int:
        return hash(self.id)

    @abstractmethod
    def __str__(self)->str:
        pass