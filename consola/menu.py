from abc import ABC, abstractmethod
import os
from entidades.usuario import Usuario
from servicios.categoria_servicio import CategoriaServicio
from servicios.pedido_servicio import PedidoServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio

class Menu(ABC):
    def __init__(self,usuario:Usuario,cat_servicio:CategoriaServicio,ped_servicio:PedidoServicio,prod_servicio:ProductoServicio,usu_servicio:UsuarioServicio)->None:
        self._usuario = usuario
        self._cat_servicio = cat_servicio
        self._ped_servicio = ped_servicio
        self._prod_servicio = prod_servicio
        self._usu_servicio = usu_servicio

    @abstractmethod
    def mostrar(self)->bool:
        pass

def crear_menu(usuario:Usuario,cat_servicio:CategoriaServicio,ped_servicio:PedidoServicio,prod_servicio:ProductoServicio,usu_servicio:UsuarioServicio)->Menu:
    from consola.menu_administrador import MenuAdministrador
    from consola.menu_cliente import MenuCliente
    from enums.enumerados import Rol
    if usuario.rol == Rol.ADMIN:
        return MenuAdministrador(usuario,cat_servicio,ped_servicio,prod_servicio,usu_servicio)
    else:
        return MenuCliente(usuario,cat_servicio,ped_servicio,prod_servicio,usu_servicio)

def limpiar_consola():
    os.system("cls" if os.name == "nt" else "clear")
def continuar():
    input("Presione cualquier tecla para continuar ")