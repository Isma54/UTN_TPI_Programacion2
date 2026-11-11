from abc import ABC, abstractmethod

class Calculable(ABC):
    @abstractmethod
    def calcular_total(self)->None:
        pass