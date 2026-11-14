from consola.menu import Menu, limpiar_consola, continuar
import questionary
from colorama import Fore,init
from excepciones.food_store_error import FoodStoreError
init(autoreset=True)

class MenuCliente(Menu):
    def mostrar(self):
        while True:
            limpiar_consola()
            opcion = questionary.select(
                message= f"=== FOOD STORE - CLIENTE ({self._usuario.nombre} {self._usuario.apellido}) ===",
                choices= ["1. Ver categorias","2. Ver productos disponibles","3. Mis pedidos","4. Mis datos","9. Cerrar Sesion","0. Salir"]
            ).ask()
            try:
                match opcion:
                    case "1. Ver categorias":
                        limpiar_consola()
                        print(Fore.LIGHTBLUE_EX + "--- LISTA DE CATEGORIAS ---")
                        categorias = self._cat_servicio.listar()
                        if not categorias:
                            print(Fore.YELLOW + "! No hay categorias existentes")
                            continuar()

                        else:
                            for cat in categorias:
                                print(cat)
                            continuar()

                    case "2. Ver productos disponibles":
                        limpiar_consola()
                        print(Fore.LIGHTBLUE_EX + "--- LISTA DE PRODUCTOS ---")
                        productos = self._prod_servicio.listar_disponibles_clientes()
                        if not productos:
                            print(Fore.YELLOW + "! No hay productos disponibles con stock")
                            continuar()

                        else:
                            for product in productos:
                                print(product)
                            continuar()

                    case "3. Mis pedidos":
                        limpiar_consola()
                        print(Fore.LIGHTBLUE_EX + "--- MIS PEDIDOS ---")
                        pedidos = self._ped_servicio.listar_por_usuario(self._usuario)
                        if not pedidos:
                            print(Fore.YELLOW + "! No tienes pedidos registrados")
                            continuar()
                          
                        else:
                            for ped in pedidos:
                                print(ped)
                            id_ped = int(input("Ingrese el ID del pedido para ver sus detalles (0 para volver): "))
                            if id_ped != 0:
                                pedido = self._ped_servicio.buscar_por_id_usuario(id_ped, self._usuario)
                                print(Fore.LIGHTBLUE_EX + f"--- DETALLE DEL PEDIDO ({pedido.id}) ---")
                                for det in pedido.detalles_pedidos:
                                    print(f"  ->{det}")
                                print(Fore.LIGHTGREEN_EX + f"Total: ${pedido.total:2f}")
                                continuar()
                            else:
                                continuar()
                            

                    case "4. Mis datos":
                        limpiar_consola()
                        print(Fore.LIGHTBLUE_EX + "=== MIS DATOS ===")
                        print(f"Nombre: {self._usuario.nombre}")
                        print(f"Apellido: {self._usuario.apellido}")
                        print(f"Mail: {self._usuario.mail}")
                        print(f"Celular: {self._usuario.celular}")
                        print(f"Rol: {self._usuario.rol.name}")
                        continuar()                      

                    case "9. Cerrar Sesion":
                        return True
                    
                    case "0. Salir":
                        return False
                    
            except FoodStoreError as e:
                print(Fore.RED + f"X Error: {e}")
                continuar()

            except ValueError:
                print(Fore.RED + "X Ingrese un numero valido")
                continuar()