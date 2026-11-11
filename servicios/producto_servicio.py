from entidades.producto import Producto
from excepciones.food_store_error import EntidadNoEncontradaError

class ProductoServicio:
    def __init__(self)-> None:
        self.__productos : list[Producto] = []

    def crear_producto(self,nombre:str,precio:float,descripcion:str,stock:int,imagen:str,disponible:bool)->Producto:
        nuevo_product= Producto(nombre,precio,descripcion,stock,imagen,disponible)
        self.__productos.append(nuevo_product)
        return nuevo_product

    def listar(self)->list[Producto]:
        return [p for p in self.__productos if not p.eliminado]

    def listar_disponibles_clientes(self)->list[Producto]:
        return [p for p in self.__productos if not p.eliminado and p.disponible and p.stock > 0]

    def buscar_por_id(self,id_producto:int)->Producto:
        for p in self.__productos:
            if p.id == id_producto and not p.eliminado:
                return p
        raise EntidadNoEncontradaError(f"No se encontro el producto con id: {id_producto}")

    def editar(self,id_producto:int,nombre:str=None,precio:float=None,descripcion:str=None,stock:int=None,imagen:str=None,disponible:bool=None):
        producto = self.buscar_por_id(id_producto)
        if nombre is not None and nombre.strip():
            producto.nombre = nombre
        if precio is not None:
            producto.precio = precio
        if descripcion is not None and descripcion.strip():
            producto.descripcion = descripcion
        if stock is not None:
            producto.stock = stock
        if imagen is not None and imagen.strip():
            producto.imagen = imagen
        if disponible is not None:
            producto.disponible = disponible
        return producto

    def eliminar(self,id_producto:int)->None:
        producto = self.buscar_por_id(id_producto)
        if producto:
            producto.eliminar()