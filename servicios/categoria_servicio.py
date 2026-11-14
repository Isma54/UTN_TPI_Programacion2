from entidades.categoria import Categoria
from entidades.producto import Producto
from entidades.usuario import Usuario
from enums.enumerados import Rol
from excepciones.food_store_error import EntidadNoEncontradaError,DuplicadoError,OperacionNoPermitidaError, DatoInvalidoError

class CategoriaServicio:
    def __init__(self)->None:
        self.__categorias:list[Categoria] = []

    def _validar_admin(self,usuario_sesion: Usuario|None) -> None:
        if usuario_sesion is not None:
            if not isinstance(usuario_sesion,Usuario) and (usuario_sesion.eliminado or usuario_sesion.rol != Rol.ADMIN):
                raise OperacionNoPermitidaError("Solo un administrador puede realizar esta operacion")
        else:
            raise OperacionNoPermitidaError("Solo un administrador puede realizar esta operacion")         

    def listar(self)->list[Categoria]:
        return [cat for cat in self.__categorias if not cat.eliminado]

    def buscar_por_id(self,id_categoria:int)->Categoria:
        for c in self.__categorias:
            if id_categoria == c.id and not c.eliminado:
                return c
        raise EntidadNoEncontradaError(f"No se encontro la categoria con id: {id_categoria}")

    def crear_categoria(self,nombre:str,descripcion:str, usuario_sesion: Usuario|None = None)->Categoria:
        self._validar_admin(usuario_sesion)
        if not isinstance(nombre,str):
            raise DatoInvalidoError("El nombre de la categoria debe ser una cadena de texto")
        nombre_limpio = nombre.strip().capitalize()
        for c in self.__categorias:
            if nombre_limpio.lower() == c.nombre.lower() and not c.eliminado:
                raise DuplicadoError(f"Ya existe una categoria con nombre {nombre_limpio}")
        nueva_cat = Categoria(nombre_limpio,descripcion)
        self.__categorias.append(nueva_cat)
        return nueva_cat

    def asociar_producto_a_categoria(self,id_categoria:int,producto:Producto, usuario_sesion: Usuario| None = None)->None:
        self._validar_admin(usuario_sesion)
        if not isinstance(producto,Producto):
            raise DatoInvalidoError("El producto debe ser una instancia de la clase Producto")
        if producto.eliminado:
            raise DatoInvalidoError("No se puede asociar ni desasociar un producto eliminado")
        categoria= self.buscar_por_id(id_categoria)
        categoria.agregar_producto(producto)
        for c in self.__categorias:
            if c.id != categoria.id:
                c.remover_producto(producto)

    def desasociar_producto_de_categoria(self, id_categoria:int,producto:Producto,usuario_sesion: Usuario|None = None):
        self._validar_admin(usuario_sesion)
        if not isinstance(producto,Producto):
            raise DatoInvalidoError("El producto debe ser una instancia de la clase Producto")
        if producto.eliminado:
            raise DatoInvalidoError("No se puede asociar ni desasociar un producto eliminado")
        categoria = self.buscar_por_id(id_categoria)
        if producto not in categoria.productos:
            raise EntidadNoEncontradaError(f"El producto con id {producto.id} no pertenece a la categoria {categoria.nombre}")
        categoria.remover_producto(producto)

    def buscar_categoria_de_producto(self,producto:Producto)->Categoria|None:
        for c in self.__categorias:
            if not c.eliminado and producto in c.productos:
                return c
        return None

    def contar_activos_por_categoria(self,id_categoria:int)->int:
        categoria = self.buscar_por_id(id_categoria)
        return sum(1 for p in categoria.productos if not p.eliminado)

    def editar(self,id_categoria:int,nombre:str|None = None,descripcion:str|None = None,usuario_sesion: Usuario|None = None)->Categoria:
        self._validar_admin(usuario_sesion)
        categoria = self.buscar_por_id(id_categoria)
        if nombre is not None:
            if not isinstance(nombre,str):
                raise DatoInvalidoError("El nombre de la categoria debe ser una cadena de texto")
            if nombre.strip() == "":
                raise DatoInvalidoError("El nombre de la categoria no puede quedar vacia")
            nombre_limpio = nombre.strip().capitalize()
            for c in self.__categorias:
                if id_categoria != c.id and nombre_limpio.lower() == c.nombre.lower() and not c.eliminado:
                    raise DuplicadoError(f"Ya existe una categoria con nombre {nombre_limpio}")
            categoria.nombre = nombre_limpio
        if descripcion is not None:
            categoria.descripcion = descripcion.strip()
        return categoria

    def eliminar(self,id_categoria:int,usuario_sesion: Usuario|None = None)->None:
        self._validar_admin(usuario_sesion)
        categoria = self.buscar_por_id(id_categoria)
        product_asociados = self.contar_activos_por_categoria(id_categoria)
        if product_asociados > 0:
            raise OperacionNoPermitidaError(f"No se puede dar de baja la categoria {categoria.nombre} ya que posee productos activos asociados")
        categoria.eliminar()