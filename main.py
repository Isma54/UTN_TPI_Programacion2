from servicios.categoria_servicio import CategoriaServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio
from servicios.pedido_servicio import PedidoServicio
from enums.enumerados import Rol
from consola.menu import crear_menu
from excepciones.food_store_error import CredencialesInvalidasError
from colorama import Fore,init
from consola.menu import limpiar_consola,continuar
import getpass
init(autoreset=True)

def main()->None:
    cat_servicio = CategoriaServicio()
    producto_servicio = ProductoServicio()
    usuario_servicio = UsuarioServicio()
    pedido_servicio = PedidoServicio()

    administrador = usuario_servicio.crear_administrador_inicial("Ana","Perez","admin@foodstore.com","2615555555", "admin123")
    usuario_servicio.crear_usuario("Juan","Gomez","cliente@foodstore.com","2614444444", "cliente123", Rol.USUARIO, administrador)
    c1 =cat_servicio.crear_categoria("Hamburgesas","Hamburgesas completas", administrador)
    c2 =cat_servicio.crear_categoria("Bedidas","Gaseosas, jugos naturales y aguas", administrador)
    p1 =producto_servicio.crear_producto("Hamburgesa completa",8000,"Medallon de carne, lechuga, tomate, queso y pan de papa",15,"",True, administrador)
    p2 =producto_servicio.crear_producto("Coca-Cola 1.5L", 4300, "Gaseosa fria sabor original",30,"",True, administrador)
    cat_servicio.asociar_producto_a_categoria(c1.id,p1,administrador)
    cat_servicio.asociar_producto_a_categoria(c2.id,p2,administrador)

    
    while True:
        intentos = 3
        usuario_actual = None

        while intentos > 0:
            limpiar_consola()
            print("=== BIENVENIDO A FOOD STORE ===")
            print(f"--- INICIO DE SESION (Intentos restantes {intentos}) ---")
            mail = input("Mail: ")
            contrasenia = getpass.getpass("Contraseña: ")

            try:
                usuario_actual = usuario_servicio.autenticar(mail,contrasenia)
                print(Fore.GREEN + f"¡Bienvenido/a, {usuario_actual.nombre} {usuario_actual.apellido} ({usuario_actual.rol.name})!")
                continuar()
                print()
                break
            except CredencialesInvalidasError as e:
                print(Fore.YELLOW + f"! {e}")
                continuar()
                intentos -= 1
                print()

        if usuario_actual is None:
            print(Fore.RED + "Se ha superado el numero maximo de intentos. El programa ha finalizado")
            continuar()
            break

        menu = crear_menu(usuario_actual,cat_servicio,pedido_servicio,producto_servicio,usuario_servicio)
        cerrar_sesion = menu.mostrar()

        if not cerrar_sesion:
            print("Saliendo de Food Store ¡Hasta luego!")
            continuar()
            break

if __name__ == "__main__":
    main()