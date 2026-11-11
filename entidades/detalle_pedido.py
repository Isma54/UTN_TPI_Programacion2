from entidades.base import Base
from entidades.producto import Producto
from excepciones.food_store_error import DatoInvalidoError

class DetallePedido(Base):
    def __init__(self,cantidad:int,producto:Producto)->None:
        super().__init__()
        self.cantidad = cantidad
        self.__subtotal = 0.0
        self.__nombre_producto = producto.nombre
        self.__precio_unitario = producto.precio
        self.actualizar_subtotal()

    @property
    def cantidad(self)->int:
        return self.__cantidad
    @property
    def producto(self)->Producto:
        return self.__producto
    @property
    def subtotal(self)->float:
        return self.__subtotal
    @property
    def nombre_producto(self)->str:
        return self.__nombre_producto    
    @property
    def precio_unitario(self)->float:
        return self.__precio_unitario


    @cantidad.setter
    def cantidad(self,cantidad:int)->None:
        if not isinstance(cantidad,int) or isinstance(cantidad,bool):
            raise DatoInvalidoError("La cantidad debe ser un numero entero")
        if cantidad <= 0:
            raise DatoInvalidoError("La cantidad no puede ser negativa")
        self.__cantidad = cantidad

    def actualizar_subtotal(self)->None:
        self.__subtotal = self.cantidad * self.precio_unitario

    def __str__(self)->str:
        return f"ID: {self.id} | {self.nombre_producto} | Cantidad: {self.cantidad} | Precio unitario: ${self.precio_unitario} |Subtotal: ${self.__subtotal}"
    