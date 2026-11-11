from entidades.base import Base
from entidades.producto import Producto
from excepciones.food_store_error import DatoInvalidoError

class Categoria(Base):
    def  __init__(self,nombre:str,descripcion:str)->None:
        super().__init__()
        self.nombre = nombre
        self.descripcion = descripcion
        self.__productos : list[Producto] = []

    @property
    def nombre(self)->str:
        return self.__nombre
    @property
    def descripcion(self)->str:
        return self.__descripcion
    @property
    def productos(self)->tuple[Producto]:
        return tuple(self.__productos)

    @nombre.setter
    def nombre(self,nombre:str)->None:
        if not isinstance(nombre,str):
            raise DatoInvalidoError("El nombre de la categoria debe ser una cadena de texto")
        if nombre.strip() == "":
            raise DatoInvalidoError("El nombre de la categoria no puede quedar vacia")
        self.__nombre = nombre.strip()

    @descripcion.setter
    def descripcion(self,descripcion:str)->None:
        if not isinstance(descripcion,str):
            raise DatoInvalidoError("La descripcion de la categoria debe ser una cadena de texto")
        if descripcion.strip() == "":
            raise DatoInvalidoError("La descripcion de la categoria no puede quedar vacia")
        self.__descripcion = descripcion.strip()

    def agregar_producto(self,producto:Producto)->None:
        if not isinstance(producto,Producto):
            raise DatoInvalidoError("Solo se pueden agregar instancias de la clase Producto")
        if producto not in self.__productos:
            self.__productos.append(producto)

    def remover_producto(self,producto:Producto)->None:
        if producto in self.__productos:
            self.__productos.remove(producto)

    def __str__(self)->str:
        return f"ID:{self.id} | {self.nombre} | {self.descripcion}"
