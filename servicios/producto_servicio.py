from entidades.producto import Producto
from entidades.usuario import Usuario
from enums.enumerados import Rol
from excepciones.food_store_error import EntidadNoEncontradaError, OperacionNoPermitidaError, DatoInvalidoError, PrecioInvalidoError, StockInvalidoError

class ProductoServicio:
    def __init__(self)-> None:
        self.__productos : list[Producto] = []

    def _validar_admin(self,usuario_sesion: Usuario|None) -> None:
        if usuario_sesion is not None:
            if not isinstance(usuario_sesion,Usuario) and (usuario_sesion.eliminado or usuario_sesion.rol != Rol.ADMIN):
                raise OperacionNoPermitidaError("Solo un administrador puede realizar esta operacion")
        else:
            raise OperacionNoPermitidaError("Solo un administrador puede realizar esta operacion")        

    def crear_producto(self,nombre:str,precio:float,descripcion:str,stock:int,imagen:str,disponible:bool,usuario_sesion: Usuario|None = None)->Producto:
        self._validar_admin(usuario_sesion)
        nuevo_product= Producto(nombre,precio,descripcion,stock,imagen,disponible)
        self.__productos.append(nuevo_product)
        return nuevo_product

    def listar(self,usuario_sesion : Usuario)->list[Producto]:
        self._validar_admin(usuario_sesion)
        return [p for p in self.__productos if not p.eliminado]

    def listar_disponibles_clientes(self)->list[Producto]:
        return [p for p in self.__productos if not p.eliminado and p.disponible and p.stock > 0]

    def buscar_por_id(self,id_producto:int)->Producto:
        for p in self.__productos:
            if p.id == id_producto and not p.eliminado:
                return p
        raise EntidadNoEncontradaError(f"No se encontro el producto con id: {id_producto}")

    def editar(self,id_producto:int,nombre:str|None=None,precio:float|None=None,descripcion:str|None=None,stock:int|None=None,imagen:str|None=None,disponible:bool|None=None,usuario_sesion : Usuario|None = None):
        self._validar_admin(usuario_sesion)
        producto = self.buscar_por_id(id_producto)
        if nombre is not None:
            if not isinstance(nombre, str):
                raise DatoInvalidoError("El nombre del producto debe ser una cadena de texto") 
            if not nombre.strip():
                raise DatoInvalidoError("El nombre del producto no puede quedar vacío")
        if precio is not None:
            if not isinstance(precio, (int, float)) or isinstance(precio, bool):
                raise DatoInvalidoError("El precio del producto debe ser un número")
            if precio < 0:
                raise PrecioInvalidoError("El precio del producto no puede ser negativo")
        if descripcion is not None: 
            if not isinstance(descripcion, str):
                raise DatoInvalidoError("La descripcion del producto debe ser una cadena de texto")
            if not descripcion.strip():
                raise DatoInvalidoError("La descripción del producto no puede quedar vacía")
        if stock is not None:
            if not isinstance(stock, int) or isinstance(stock, bool):
                raise DatoInvalidoError("El stock del producto debe ser un numero entero")
            if stock < 0:
                raise StockInvalidoError("El stock del producto no puede ser negativo")
        if imagen is not None and not isinstance(imagen, str):
            raise DatoInvalidoError("La imagen debe ser una cadena de texto")
        if disponible is not None and not isinstance(disponible, bool):
            raise DatoInvalidoError("La disponibilidad debe ser un booleano")        
        if nombre is not None:
            producto.nombre = nombre
        if precio is not None:
            producto.precio = precio
        if descripcion is not None:
            producto.descripcion = descripcion
        if stock is not None:
            producto.stock = stock
        if imagen is not None:
            producto.imagen = imagen
        if disponible is not None:
            producto.disponible = disponible
        return producto

    def eliminar(self,id_producto:int,usuario_sesion: Usuario|None = None)->None:
        self._validar_admin(usuario_sesion)
        producto = self.buscar_por_id(id_producto)
        if producto:
            producto.eliminar()