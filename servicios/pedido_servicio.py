from entidades.pedido import Pedido
from entidades.usuario import Usuario
from entidades.producto import Producto
from enums.enumerados import FormaPago,Estado
from excepciones.food_store_error import EntidadNoEncontradaError,OperacionNoPermitidaError,StockInsuficienteError

class PedidoServicio:
    def __init__(self):
        self.__pedidos : list[Pedido] = []

    def listar(self)->list[Pedido]:
        return [ped for ped in self.__pedidos if not ped.eliminado]

    def listar_por_usuario(self,usuario:Usuario)->list[Pedido]:
        return [ped for ped in self.__pedidos if not ped.eliminado and ped.usuario.id == usuario.id]

    def buscar_por_id(self,id_pedido:int)->Pedido:
        for p in self.__pedidos:
            if id_pedido == p.id and not p.eliminado:
                return p
        raise EntidadNoEncontradaError(f"No se encontro el pedido con id: {id_pedido}")

    def crear_pedido_con_detalles(self,forma_pago:FormaPago,usuario:Usuario,items:list[tuple[int,Producto]])->Pedido:
        if usuario.eliminado:
            raise OperacionNoPermitidaError("No se puede crear un pedido con un usuario eliminado")
        nuevo_pedido = Pedido(forma_pago,usuario)
        for cant,product in items:
            existente = nuevo_pedido.buscar_detalle_por_producto(product)
            stock_necesario = cant + (existente.cantidad if existente else 0)
            if stock_necesario > product.stock:
                raise StockInsuficienteError(f"Stock insuficiente para {product.nombre}. Disponible: {product.stock}")
        for cant, product in items:
            nuevo_pedido.agregar_detalle(cant,product)
            product.stock -= cant
        self.__pedidos.append(nuevo_pedido)
        return nuevo_pedido

    def cambiar_estado(self,id_pedido:int,nuevo_estado:Estado)->Pedido:
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

    def cambiar_forma_pago(self,id_pedido:int,nueva_forma:FormaPago)->Pedido:
        pedido = self.buscar_por_id(id_pedido)
        if pedido.estado in [Estado.TERMINADO,Estado.CANCELADO]:
            raise OperacionNoPermitidaError("No se puede modificar la forma de pago de un pedido ya terminado o cancelado")
        pedido.forma_pago = nueva_forma
        return pedido

    def eliminar(self,id_pedido:int)->None:
        pedido = self.buscar_por_id(id_pedido)
        if pedido.estado not in [Estado.TERMINADO,Estado.CANCELADO]:
            for detalle in pedido.detalles_pedidos:
                detalle.producto.stock += detalle.cantidad
        pedido.eliminar()
        for detalle in pedido.detalles_pedidos:
            detalle.eliminar()