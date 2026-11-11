from entidades.categoria import Categoria
from entidades.producto import Producto
from excepciones.food_store_error import EntidadNoEncontradaError,DuplicadoError,OperacionNoPermitidaError

class CategoriaServicio:
    def __init__(self)->None:
        self.__categorias:list[Categoria] = []

    def listar(self)->list[Categoria]:
        return [cat for cat in self.__categorias if not cat.eliminado]

    def buscar_por_id(self,id_categoria:int)->Categoria:
        for c in self.__categorias:
            if id_categoria == c.id and not c.eliminado:
                return c
        raise EntidadNoEncontradaError(f"No se encontro la categoria con id: {id_categoria}")

    def crear_categoria(self,nombre:str,descripcion:str)->Categoria:
        nombre_limpio = nombre.strip().capitalize()
        for c in self.__categorias:
            if nombre_limpio.lower() == c.nombre.lower() and not c.eliminado:
                raise DuplicadoError(f"Ya existe una categoria con nombre {nombre_limpio}")
        nueva_cat = Categoria(nombre_limpio,descripcion)
        self.__categorias.append(nueva_cat)
        return nueva_cat

    def asociar_producto_a_categoria(self,id_categoria:int,producto:Producto)->None:
        categoria= self.buscar_por_id(id_categoria)
        categoria.agregar_producto(producto)

    def contar_activos_por_categoria(self,id_categoria:int)->int:
        categoria = self.buscar_por_id(id_categoria)
        return sum(1 for p in categoria.productos if not p.eliminado)

    def editar(self,id_categoria:int,nombre:str=None,descripcion:str=None)->Categoria:
        categoria = self.buscar_por_id(id_categoria)
        if nombre is not None and nombre.strip():
            nombre_limpio = nombre.strip().capitalize()
            for c in self.__categorias:
                if id_categoria != c.id and nombre_limpio.lower() == c.nombre.lower() and not c.eliminado:
                    raise DuplicadoError(f"Ya existe una categoria con nombre {nombre_limpio}")
            categoria.nombre = nombre_limpio
        if descripcion is not None:
            categoria.descripcion = descripcion.strip()
        return categoria

    def eliminar(self,id_categoria:int)->None:
        categoria = self.buscar_por_id(id_categoria)
        product_asociados = self.contar_activos_por_categoria(id_categoria)
        if product_asociados > 0:
            raise OperacionNoPermitidaError(f"No se puede dar de baja la categoria {categoria.nombre} ya que posee productos activos asociados")
        categoria.eliminar()