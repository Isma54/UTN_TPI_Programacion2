from entidades.pedido import Pedido
from entidades.usuario import Usuario
from entidades.producto import Producto
from enums.enumerados import FormaPago,Estado,Rol
from excepciones.food_store_error import EntidadNoEncontradaError,OperacionNoPermitidaError,StockInsuficienteError,DatoInvalidoError

class PedidoServicio:
    def __init__(self):
        self.__pedidos : list[Pedido] = []

    def _validar_admin(self,usuario_sesion: Usuario|None) -> None:
        if usuario_sesion is not None:
            if not isinstance(usuario_sesion,Usuario) and (usuario_sesion.eliminado or usuario_sesion.rol != Rol.ADMIN):
                raise OperacionNoPermitidaError("Solo un administrador puede realizar esta operacion")
        else:
            raise OperacionNoPermitidaError("Solo un administrador puede realizar esta operacion")     
    
    def listar(self,usuario_sesion:Usuario)->list[Pedido]:
        self._validar_admin(usuario_sesion)
        return [ped for ped in self.__pedidos if not ped.eliminado]

    def listar_por_usuario(self,usuario:Usuario)->list[Pedido]:
        return [ped for ped in self.__pedidos if not ped.eliminado and ped.usuario.id == usuario.id]

    def buscar_por_id(self,id_pedido:int)->Pedido:
        for p in self.__pedidos:
            if id_pedido == p.id and not p.eliminado:
                return p
        raise EntidadNoEncontradaError(f"No se encontro el pedido con id: {id_pedido}")

    def buscar_por_id_usuario(self,id_pedido:int,usuario:Usuario)->Pedido:
        for p in self.__pedidos:
            if id_pedido == p.id and not p.eliminado and p.usuario.id == usuario.id:
                return p
        raise EntidadNoEncontradaError(f"No se encontro el pedido con id: {id_pedido}")

    def crear_pedido_con_detalles(self,forma_pago:FormaPago,usuario:Usuario,items:list[tuple[int,Producto]], usuario_sesion: Usuario|None = None)->Pedido:
        self._validar_admin(usuario_sesion)
        if not isinstance(usuario,Usuario) or usuario.eliminado:
            raise OperacionNoPermitidaError("No se puede crear un pedido con un usuario inexistente o eliminado")
        if not isinstance(items,list) or not items:
            raise DatoInvalidoError("El pedido debe contener al menos un producto")
        
        nuevo_pedido = Pedido(forma_pago,usuario)         
        for item in items:
            if not isinstance(item,tuple) or len(item) != 2:
                raise DatoInvalidoError("Cada articulo debe contener una cantidad y un producto")
            cant, product = item
            if not isinstance(cant,int) or isinstance(cant,bool) or cant <= 0:
                raise DatoInvalidoError("La cantidad debe ser mayor a 0")
            if not isinstance(product,Producto) or product.eliminado or not product.disponible:
                raise DatoInvalidoError("El producto seleccionado debe estar disponible, no eliminado y ser instancia de Producto")
            nuevo_pedido.agregar_detalle(cant,product)        

        nuevo_pedido.calcular_total()
        stock_anterior = {detalle.producto.id: (detalle.producto, detalle.producto.stock, detalle.producto.disponible) for detalle in nuevo_pedido.detalles_pedidos}
        try:
            for detalle in nuevo_pedido.detalles_pedidos:
                detalle.producto.stock -= detalle.cantidad
            self.__pedidos.append(nuevo_pedido)
        except Exception:
            for producto, stock, disponible in stock_anterior.values():
                producto.stock = stock
                producto.disponible = disponible
            if nuevo_pedido in self.__pedidos:
                self.__pedidos.remove(nuevo_pedido)
            raise

        return nuevo_pedido

    def cambiar_estado(self,id_pedido:int,nuevo_estado:Estado,usuario_sesion: Usuario|None = None)->Pedido:
        self._validar_admin(usuario_sesion)
        if not isinstance(nuevo_estado,Estado):
            raise DatoInvalidoError("El estado del pedido es invalido")
        pedido = self.buscar_por_id(id_pedido)
        estado_actual = pedido.estado
        if estado_actual == nuevo_estado:
            return pedido
        valido = False
        if estado_actual == Estado.PENDIENTE and nuevo_estado in [Estado.CONFIRMADO, Estado.CANCELADO]:
            valido = True
        elif estado_actual == Estado.CONFIRMADO and nuevo_estado in [Estado.TERMINADO, Estado.CANCELADO]:
            valido = True

        if not valido and estado_actual != nuevo_estado:
            raise OperacionNoPermitidaError(f"Transaccion de estado invalida de {estado_actual.name} a {nuevo_estado.name}")

        if nuevo_estado == Estado.CANCELADO and estado_actual not in [Estado.TERMINADO,Estado.CANCELADO]:
            for detalle in pedido.detalles_pedidos:
                detalle.producto.stock += detalle.cantidad
        pedido.estado = nuevo_estado
        return pedido

    def cambiar_forma_pago(self,id_pedido:int,nueva_forma:FormaPago,usuario_sesion: Usuario|None = None)->Pedido:
        self._validar_admin(usuario_sesion)
        pedido = self.buscar_por_id(id_pedido)
        if pedido.estado in [Estado.TERMINADO,Estado.CANCELADO]:
            raise OperacionNoPermitidaError("No se puede modificar la forma de pago de un pedido ya terminado o cancelado")
        pedido.forma_pago = nueva_forma
        return pedido

    def eliminar(self,id_pedido:int,usuario_sesion: Usuario|None = None)->None:
        self._validar_admin(usuario_sesion)
        pedido = self.buscar_por_id(id_pedido)
        if pedido.estado not in [Estado.TERMINADO,Estado.CANCELADO]:
            for detalle in pedido.detalles_pedidos:
                detalle.producto.stock += detalle.cantidad
        pedido.eliminar()
        for detalle in pedido.detalles_pedidos:
            detalle.eliminar()