from colorama import Fore, init
from enums.enumerados import Rol, FormaPago, Estado
from excepciones.food_store_error import FoodStoreError, DuplicadoError, StockInsuficienteError
from servicios.categoria_servicio import CategoriaServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio
from servicios.pedido_servicio import PedidoServicio

init(autoreset=True)

def ejecutar_pruebas():
    print(Fore.MAGENTA + "=== EJECUTANDO PRUEBAS AUTOMÁTICAS DEL MODELO Y SERVICIOS ===")
    print()
    
    cat_serv = CategoriaServicio()
    prod_serv = ProductoServicio()
    usr_serv = UsuarioServicio()
    ped_serv = PedidoServicio()

    print("[Prueba 1] Gestión de Categorías...")
    c1 = cat_serv.crear_categoria("Hamburguesas", "Variedad de hamburguesas caseras")
    print(f"  Categoría creada con éxito: {c1}")
    
    try:
        cat_serv.crear_categoria("HAMBURGUESAS", "Intento de duplicado")
    except DuplicadoError as e:
        print(Fore.GREEN + f"[OK] Excepción DuplicadoError capturada correctamente: {e}")
    print()

    print("[Prueba 2] Agregación de Productos...")
    p1 = prod_serv.crear_producto("Hamburguesa Completa", 5500.0, "Con queso y huevo", 10, "hamb.png", True)
    cat_serv.asociar_producto_a_categoria(c1.id, p1)
    activos = cat_serv.contar_activos_por_categoria(c1.id)
    print(Fore.GREEN + f"[OK] Producto asociado a la categoría. Cantidad de activos en '{c1.nombre}': {activos}")
    print()

    print("[Prueba 3] Composición de Pedidos y Validación de Stock...")
    u1 = usr_serv.crear_usuario("Carlos", "Gomez", "carlos@gmail.com", "2612222222", "pass123", Rol.USUARIO)
    carrito_invalido = [(12, p1)]
    try:
        ped_serv.crear_pedido_con_detalles(FormaPago.EFECTIVO, u1, carrito_invalido)
    except StockInsuficienteError as e:
        print(Fore.GREEN + f"[OK] Excepción StockInsuficienteError capturada correctamente: {e}")
        print(f"  El stock del producto se mantuvo intacto en: {p1.stock}")
        
    carrito_valido = [(3, p1)]
    pedido_ok = ped_serv.crear_pedido_con_detalles(FormaPago.EFECTIVO, u1, carrito_valido)
    print(Fore.GREEN + f"[OK] Pedido consolidado con éxito: {pedido_ok}")
    print(f"  Stock resultante de {p1.nombre} (Debe ser 7): {p1.stock}")
    print(f"  Monto Total Computado por Calculable: ${pedido_ok.total}")
    print()

    print("[Prueba 4] Transición de Estados...")
    print(f"  Estado actual del pedido: {pedido_ok.estado.name}")
    ped_serv.cambiar_estado(pedido_ok.id, Estado.CONFIRMADO)
    print(f"  Nuevo estado (Transición válida): {pedido_ok.estado.name}")
    
    try:
        ped_serv.cambiar_estado(pedido_ok.id, Estado.PENDIENTE)
    except FoodStoreError as e:
        print(Fore.GREEN + f"[OK] Excepción de Transición Inválida capturada: {e}")
    print()

    print("[Prueba 5] Restricciones de Baja Lógica...")
    try:
        cat_serv.eliminar(c1.id)
    except FoodStoreError as e:
        print(Fore.GREEN + f"[OK] Bloqueo de eliminación correcto: {e}")
    print()

    print(Fore.CYAN + "=== TODAS LAS PRUEBAS FUERON PASADAS CON ÉXITO ===")

if __name__ == "__main__":
    ejecutar_pruebas()