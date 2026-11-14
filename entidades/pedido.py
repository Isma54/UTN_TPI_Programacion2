from entidades.base import Base
from entidades.calculable import Calculable
from enums.enumerados import Estado,FormaPago
from entidades.detalle_pedido import DetallePedido
from entidades.producto import Producto
from entidades.usuario import Usuario
from excepciones.food_store_error import DatoInvalidoError, StockInsuficienteError
from datetime import date

class Pedido(Base,Calculable):
    def __init__(self,forma_pago:FormaPago,usuario:Usuario):
        super().__init__()
        self.__fecha : date = date.today()
        self.__estado = Estado.PENDIENTE
        self.__total : float = 0.0
        self.forma_pago = forma_pago
        self.usuario = usuario
        self.__detalles_pedidos : list[DetallePedido] = []

    @property
    def fecha(self)->date:
        return self.__fecha
    @property
    def estado(self)->Estado:
        return self.__estado
    @property
    def total(self)->float:
        return self.__total
    @property
    def forma_pago(self)->FormaPago:
        return self.__forma_pago
    @property
    def usuario(self)->Usuario:
        return self.__usuario
    @property
    def detalles_pedidos(self)->tuple[DetallePedido]:
        return tuple(self.__detalles_pedidos)

    @forma_pago.setter
    def forma_pago(self,metodo:FormaPago)->None:
        if not isinstance(metodo,FormaPago):
            raise DatoInvalidoError("Forma de pago invalida")
        self.__forma_pago = metodo

    @estado.setter
    def estado(self,estado:Estado)->None:
        if not isinstance(estado,Estado):
            raise DatoInvalidoError("El estado del pedido es invalido")
        self.__estado = estado

    @usuario.setter
    def usuario(self,usuario:Usuario):
        if not isinstance(usuario,Usuario):
            raise DatoInvalidoError("El usuario no es valido")
        if usuario.eliminado:
            raise DatoInvalidoError("El usuario se encuentra eliminado")
        self.__usuario = usuario

    def calcular_total(self)->None:
        total=0.0
        for detalle in self.__detalles_pedidos:
            detalle.actualizar_subtotal()
            total += detalle.subtotal
        self.__total = total

    def agregar_detalle(self,cantidad:int,producto:Producto)->None:
        if not isinstance(cantidad,int) or isinstance(cantidad,bool):
            raise DatoInvalidoError("La cantidad debe ser un numero entero")
        if cantidad <= 0:
            raise DatoInvalidoError("La cantidad debe ser mayor a cero")
        if not isinstance(producto,Producto):
            raise DatoInvalidoError("El producto no es valido")
        if producto.eliminado or not producto.disponible:
            raise DatoInvalidoError(f"El producto {producto.nombre} no esta disponible")

        existente = self.buscar_detalle_por_producto(producto)
        stock_necesario = cantidad + (existente.cantidad if existente else 0)

        if stock_necesario > producto.stock:
            raise StockInsuficienteError(f"Stock insuficiente para {producto.nombre}, stock disponible: {producto.stock}")

        if existente:
            existente.cantidad = stock_necesario
            existente.actualizar_subtotal()
        else:
            detalle = DetallePedido(cantidad,producto)
            self.__detalles_pedidos.append(detalle)
        self.calcular_total()

    def eliminar_detalle_por_producto(self,producto:Producto)->None:
        detalle = self.buscar_detalle_por_producto(producto)
        if detalle:
            detalle.eliminar()
            self.__detalles_pedidos.remove(detalle)
            self.calcular_total()

    def buscar_detalle_por_producto(self,producto:Producto)->DetallePedido | None:
        if not isinstance(producto,Producto):
            raise DatoInvalidoError("El producto no es valido")
        for detalle in self.__detalles_pedidos:
            if detalle.producto.id == producto.id and not producto.eliminado:
                return detalle
        return None

    def __str__(self)->str:
        fecha_formateada = self.fecha.strftime("%d/%m/%Y")
        return f"ID: {self.id} | Fecha: {fecha_formateada} | Usuario: {self.usuario.nombre} {self.usuario.apellido} ({self.usuario.mail}) | Estado: {self.estado.name} | Pago: {self.forma_pago.name} | Total: ${self.total:.2f}"