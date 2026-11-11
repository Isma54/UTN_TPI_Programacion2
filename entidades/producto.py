from entidades.base import Base
from excepciones.food_store_error import DatoInvalidoError,PrecioInvalidoError,StockInvalidoError
class Producto(Base):
    def __init__(self,nombre:str,precio:float,descripcion:str,stock:int,imagen:str,disponible:bool)->None:
        super().__init__()
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.stock = stock
        self.imagen = imagen
        self.__disponible = disponible

    @property
    def nombre(self)->str:
        return self.__nombre
    @property
    def precio(self)->float:
        return self.__precio
    @property
    def descripcion(self)->str:
        return self.__descripcion
    @property
    def imagen(self)->str:
        return self.__imagen
    @property
    def stock(self)->int:
        return self.__stock
    @property
    def imagen(self)->str:
        return self.__imagen
    @property
    def disponible(self)->bool:
        return self.__disponible

    @nombre.setter
    def nombre(self,nombre:str)->None:
        if not isinstance(nombre,str):
            raise DatoInvalidoError("El nombre del producto debe ser una cadena de texto")
        if nombre.strip() == "":
            raise DatoInvalidoError("El nombre del produdcto no puede quedar vacio")
        self.__nombre = nombre.strip()

    @imagen.setter
    def imagen(self,imagen:str)->None:
        if not isinstance(imagen, str):
            raise DatoInvalidoError("La imagen debe ser una ruta de texto")
        self.__imagen = imagen.strip()   

    @descripcion.setter
    def descripcion(self,descripcion:str)->None:
        if not isinstance(descripcion,str):
            raise DatoInvalidoError("La descripcion del producto debe ser una cadena de texto")
        if descripcion.strip() == "":
            raise DatoInvalidoError("La descripcion del producto no puede quedar vacio")
        self.__descripcion = descripcion.strip()

    @precio.setter
    def precio(self,precio:float)->None:
        if not isinstance(precio,(int,float)) or isinstance(precio,bool):
            raise DatoInvalidoError("El precio del producto debe ser un numero")
        if precio < 0:
            raise PrecioInvalidoError("El precio del producto no puede ser negativo")
        self.__precio = precio

    @stock.setter
    def stock(self,cantidad:int)->None:
        if not isinstance(cantidad,int) or isinstance(cantidad,bool):
            raise DatoInvalidoError("El stock del producto debe ser un numero")
        if cantidad < 0:
            raise StockInvalidoError("El stock del producto no puede ser negativo")
        self.__stock = cantidad
        if self.__stock == 0:
            self.__disponible = False

    @disponible.setter
    def disponible(self, disponible: bool) -> None:
        if not isinstance(disponible, bool):
            raise DatoInvalidoError("La disponibilidad debe ser un booleano")
        self.__disponible = disponible

    def __str__(self)->str:
        disp = "Disponible" if self.__disponible else "No disponible"
        return f"ID: {self.id} | {self.nombre} | ${self.precio} | {self.descripcion} | Stock: {self.stock} | {disp}"