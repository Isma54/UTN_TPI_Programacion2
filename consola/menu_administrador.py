from consola.menu import Menu,continuar,limpiar_consola
from enums.enumerados import Rol,Estado,FormaPago
from excepciones.food_store_error import FoodStoreError
import questionary
from colorama import Fore,init
init(autoreset=True)

class MenuAdministrador(Menu):
    def mostrar(self):
        while True:
            limpiar_consola()
            opcion = questionary.select(
                message= f"=== FOOD STORE - ADMINISTRADOR ({self._usuario.nombre} {self._usuario.apellido}) ===",
                choices= ["1. Categorias", "2. Productos", "3. Usuarios", "4. Pedidos", "9. Cerrar sesion", "0. Salir"]
            ).ask()
            try:
                match opcion:
                    case "1. Categorias":
                        self._menu_categorias()
                    case "2. Productos":
                        self._menu_productos()
                    case "3. Usuarios":
                        self._menu_usuarios()
                    case "4. Pedidos":
                        self._menu_pedidos()
                    case "9. Cerrar sesion":
                        print("Cerrando menu...")
                        continuar()
                        limpiar_consola()
                        return True
                    case "0. Salir":
                        return False
    
            except FoodStoreError as e:
                print(Fore.RED + f"X Error: {e}")
                continuar()
            except ValueError:
                print(Fore.RED + "X Ingrese un numero valido")
                continuar()

    def _menu_categorias(self):
        while True:
            limpiar_consola()
            seleccion = questionary.select(
                message= "--- GESTION DE CATEGORIAS (ADMIN) ---",
                choices= ["1. Listar", "2. Crear", "3. Editar", "4. Eliminar", "0. Volver"],
            ).ask()
            try: 
                match seleccion:
                    case "1. Listar":
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

                    case "2. Crear":
                        limpiar_consola()
                        print(Fore.LIGHTBLUE_EX + "--- NUEVA CATEGORIA ---")
                        nombre= input("Nombre: ")
                        descripcion = input("Descripcion: ")
                        c = self._cat_servicio.crear_categoria(nombre,descripcion)
                        print(Fore.GREEN + f"[OK] Categoria creada con exito con id: {c.id}")
                        continuar()

                    case "3. Editar":
                        limpiar_consola()
                        print(Fore.LIGHTBLUE_EX + "--- EDITAR CATEGORIA ---")
                        categorias = self._cat_servicio.listar()
                        if not categorias:
                            print(Fore.YELLOW + "! No hay categorias disponibles para actualizar")
                            continuar()
                            continue
                        for cat in categorias:
                            print(cat)
                        id_cat = int(input("ID de la categoria a editar: "))
                        self._cat_servicio.buscar_por_id(id_cat)
                        nuevo_nombre = input("Nuevo nombre (Enter para conservar): ")
                        nueva_descrip = input("Nueva descripcion (Enter para conservar): ")
                        nombre_param = nuevo_nombre if nuevo_nombre.strip() != "" else None
                        descrip_param = nueva_descrip if nueva_descrip.strip() != "" else None
                        self._cat_servicio.editar(id_cat, nombre_param, descrip_param)
                        print(Fore.GREEN + "[OK] Categoria actualizada con exito")
                        continuar()

                    case "4. Eliminar":
                        limpiar_consola()
                        print(Fore.LIGHTBLUE_EX + "--- ELIMINAR CATEGORIA (BAJA LOGICA) ---")
                        categorias = self._cat_servicio.listar()
                        if not categorias:
                            print(Fore.YELLOW + "! No hay categorias disponibles para dar de baja")
                            continuar()
                            continue

                        for cat in categorias:
                            print(cat)
                        id_cat = int(input("ID de la categoria a eliminar: "))
                        confirmar = questionary.select(
                            message= "¿Eliminar?",
                            choices= ["Si","No"]
                        ).ask()
                        match confirmar:
                            case "Si":
                                self._cat_servicio.eliminar(id_cat)
                                print(Fore.GREEN + "[OK] Categoria eliminada logicamente")
                                continuar()

                            case "No":
                                print(Fore.YELLOW + "Operacion cancelada")
                                print("Volviendo al menu...")
                                continuar()

                    case "0. Volver":
                        print("Volviendo al menu principal...")
                        continuar()
                        break

            except ValueError:
                print(Fore.RED + "X Error: Ingrese un numero entero valido")
                continuar()
            except FoodStoreError as e:
                print(Fore.RED + f"X Error de negocio: {e}")
                continuar()

    def _menu_productos(self):
        while True:
            limpiar_consola()
            seleccion = questionary.select(
                message= "--- GESTION DE PRODUCTOS (ADMIN) ---",
                choices= ["1. Listar", "2. Crear", "3. Editar", "4. Eliminar", "0. Volver"]
            ).ask()
            try:
                match seleccion:
                    case "1. Listar":
                        limpiar_consola()
                        print(Fore.LIGHTBLUE_EX + "--- LISTA DE PRODUCTOS ---")
                        productos = self._prod_servicio.listar()
                        if not productos:
                            print(Fore.YELLOW + "! No hay productos disponibles con stock")
                            continuar()

                        else:
                            for product in productos:
                                print(product)
                            continuar()

                    case "2. Crear":
                        limpiar_consola()
                        print(Fore.LIGHTBLUE_EX + "--- NUEVO PRODUCTO ---")
                        categorias = self._cat_servicio.listar()
                        if not categorias:
                            print(Fore.YELLOW + "! No se pueden crear productos si no existen categorias primero")
                            continuar()
                            continue
                        print("Categoria disponibles:")
                        for cat in categorias:
                            print(cat)
                        id_cat = int(input("ID de la categoria para el producto: "))
                        self._cat_servicio.buscar_por_id(id_cat)
                        nombre = input("Nombre: ")
                        descripcion = input("Descripcion: ")
                        precio = float(input("Precio: "))
                        stock = int(input("Stock inicial: "))
                        imagen = input("Ruta de la imagen: ")

                        disp_input = questionary.select(
                            message= "¿Esta disponible para la venta?",
                            choices= ["Si","No"]
                        ).ask()
                        disponible = True if disp_input == "Si" else False
                        nuevo_product = self._prod_servicio.crear_producto(nombre,precio,descripcion,stock,imagen,disponible)
                        self._cat_servicio.asociar_producto_a_categoria(id_cat,nuevo_product)
                        print(Fore.GREEN + f"[OK] Producto creado con exito con id: {nuevo_product.id}")
                        continuar()

                    case "3. Editar":
                        limpiar_consola()
                        print(Fore.LIGHTBLUE_EX + "--- EDITAR PRODUCTO ---")
                        productos = self._prod_servicio.listar()
                        if not productos:
                            print(Fore.YELLOW + "! No hay productos para editar")
                            continuar()
                            continue
                        for p in productos:
                            print(p)

                        id_prod = int(input("ID del producto a editar: "))
                        self._prod_servicio.buscar_por_id(id_prod)

                        nuevo_nombre = input("Nuevo nombre (Enter para conservar): ")
                        nuevo_precio = input("Nuevo precio (Enter para conservar): ")
                        nueva_descripcion = input("Nueva descripcion (Enter para conservar): ")
                        nuevo_stock = input("Nuevo stock (Enter para conservar): ")
                        nueva_img = input("Nueva imagen (Enter para conservar): ")
                        disp_actualizar = questionary.select(
                            message= "¿El producto a actualizar esta disponible?",
                            choices= ["Si","No","Conservar"]
                        ).ask()
                        if disp_actualizar == "Si":
                            disponible_param = True
                        elif disp_actualizar == "No":
                            disponible_param = False
                        else:
                            disponible_param = None

                        nom_param = nuevo_nombre if nuevo_nombre.strip() != "" else None
                        precio_param = float(nuevo_precio) if nuevo_precio.strip() != "" else None
                        desc_param = nueva_descripcion if nueva_descripcion.strip() != "" else None
                        stock_param = int(nuevo_stock) if nuevo_stock.strip() != "" else None
                        img_param = nueva_img if nueva_img.strip() != "" else None                   

                        self._prod_servicio.editar(id_prod,nom_param,precio_param,desc_param,stock_param,img_param,disponible_param)
                        print(Fore.GREEN + "[OK] Producto actualizado con exito")
                        continuar()

                    case "4. Eliminar":
                        limpiar_consola()
                        print(Fore.LIGHTBLUE_EX + "--- ELIMINAR PRODUCTO (BAJA LOGICA) ---")
                        productos = self._prod_servicio.listar()
                        if not productos:
                            print(Fore.YELLOW + "! No hay productos disponibles para dar de baja")
                            continuar()
                            continue
                        for p in productos:
                            print(p)
                        id_prod = int(input("ID del producto a eliminar: "))
                        confirmar = questionary.select(
                            message= "¿Eliminar?",
                            choices= ["Si","No"]
                        ).ask()
                        match confirmar:
                            case "Si":
                                self._prod_servicio.eliminar(id_prod)
                                print(Fore.GREEN + "[OK] Producto eliminado logicamente")
                                continuar()

                            case "No":
                                print(Fore.YELLOW + "Operacion cancelada")
                                print("Volviendo al menu...")
                                continuar()

                    case "0. Volver":
                        print("Volviendo al menu principal...")
                        continuar()
                        break

            except ValueError:
                print(Fore.RED + "X Error: Ingrese un numero entero valido")
                continuar()
            except FoodStoreError as e:
                print(Fore.RED + f"X Error de negocio: {e}")
                continuar()

    def _menu_usuarios(self):
        while True:
            limpiar_consola()
            seleccion = questionary.select(
                message= "--- GESTION DE USUARIOS (ADMIN) ---",
                choices= ["1. Listar", "2. Crear", "3. Editar", "4. Eliminar", "0. Volver"]
            ).ask()
            try:
                match seleccion:
                    case "1. Listar":
                        limpiar_consola()
                        print(Fore.LIGHTBLUE_EX + "--- LISTA DE USUARIOS REGISTRADOS ---")
                        usuarios = self._usu_servicio.listar()
                        if not usuarios:
                            print(Fore.YELLOW + "! No hay usuarios registrados")
                            continuar()
                        else:
                            for u in usuarios:
                                print(u)
                            continuar()

                    case "2. Crear":
                        limpiar_consola()
                        print(Fore.LIGHTBLUE_EX + "--- REGISTRAR NUEVO USUARIO ---")
                        nombre = input("Nombre: ")
                        apellido = input("Apellido: ")
                        mail = input("Mail: ")
                        celular = input("Celular: ")
                        contrasenia = input("Contraseña: ")

                        rol_elegir = questionary.select(
                            message= "Seleccione el rol:",
                            choices= ["ADMIN","USUARIO"]
                        ).ask()
                        rol_param = Rol.ADMIN if rol_elegir == "ADMIN" else Rol.USUARIO
                        nuevo_usuario = self._usu_servicio.crear_usuario(nombre,apellido,mail,celular,contrasenia,rol_param)
                        print(Fore.GREEN + f"[OK] Usuario creado con exito con id: {nuevo_usuario.id}")
                        continuar()

                    case "3. Editar":
                        limpiar_consola()
                        print(Fore.LIGHTBLUE_EX + "--- EDITAR DATOS DE USUARIO ---")
                        usuarios= self._usu_servicio.listar()
                        for u in usuarios:
                            print(u)
                        id_usu = int(input("ID del usuario a editar: "))
                        self._usu_servicio.buscar_por_id(id_usu)

                        nuevo_nom = input("Nuevo nombre (Enter para conservar): ")
                        nuevo_ape = input("Nuevo apellido (Enter para conservar): ")
                        nuevo_mail = input("Nuevo mail (Enter para conservar): ")
                        nuevo_cel = input("Nuevo celular (Enter para conservar): ")
                        nueva_contra = input("Nueva contraseña (Enter para conservar): ")
                        nuevo_rol = questionary.select(
                            message= "¿Desea cambiar el rol?",
                            choices= ["Cambiar a ADMIN", "Cambiar a USUARIO", "Conservar actual"]
                        ).ask()
                        rol_param = None
                        if nuevo_rol == "Cambiar a ADMIN":
                            rol_param = Rol.ADMIN
                        elif nuevo_rol == "Cambiar a USUARIO":
                            rol_param = Rol.USUARIO

                        nom_param = nuevo_nom if nuevo_nom.strip() != "" else None
                        ape_param = nuevo_ape if nuevo_ape.strip() != "" else None
                        mail_param = nuevo_mail if nuevo_mail.strip() != "" else None
                        cel_param = nuevo_cel if nuevo_cel.strip() != "" else None
                        contra_param = nueva_contra if nueva_contra.strip() != "" else None

                        self._usu_servicio.editar(id_usu,nom_param,ape_param,mail_param,cel_param,contra_param,rol_param)
                        print(Fore.GREEN + "[OK] Usuario actualizado con exito")
                        continuar()

                    case "4. Eliminar":
                        limpiar_consola()
                        print(Fore.LIGHTBLUE_EX + "--- ELIMINAR USUARIO ---")
                        usuarios = self._usu_servicio.listar()
                        for u in usuarios:
                            print(u)

                        id_usu = int(input("ID del usuario a dar de baja: "))
                        confirmar = questionary.select(
                            message= "¿Eliminar?",
                            choices= ["Si","No"]
                        ).ask()
                        match confirmar:
                            case "Si":
                                self._usu_servicio.eliminar(id_usu,self._usuario.id)
                                print(Fore.GREEN + "[OK] Usuario eliminado logicamente")
                                continuar()

                            case "No":
                                print(Fore.YELLOW + "Operacion cancelada")
                                print("Volviendo al menu...")
                                continuar()

                    case "0. Volver":
                        print("Volviendo al menu principal...")
                        continuar()
                        break

            except ValueError:
                print(Fore.RED + "X Error: Ingrese un numero entero valido")
                continuar()
            except FoodStoreError as e:
                print(Fore.RED + f"X Error de negocio: {e}")
                continuar()

    def _menu_pedidos(self):
        while True:
            limpiar_consola()
            seleccion = questionary.select(
                message= "--- GESTION DE PEDIDOS (ADMIN) ---",
                choices= ["1. Listar todos los pedidos", "2. Crear pedido con detalles", "3. Cambiar estado de un pedido", "4. Cambiar forma de pago", "5. Eliminar Pedido", "0. Volver"]
            ).ask()
            try:
                match seleccion:
                    case "1. Listar todos los pedidos":
                        limpiar_consola()
                        print(Fore.LIGHTBLUE_EX + "--- HISTORIAL GENERAL DE PEDIDOS ---")
                        pedidos = self._ped_servicio.listar()
                        if not pedidos:
                            print(Fore.YELLOW + "! No hay pedidos registrados en el sistema")
                            continuar()
                        else:
                            for ped in pedidos:
                                print(ped)
                                for det in ped.detalles_pedidos:
                                    print(f"   ->{det}")
                            continuar()

                    case "2. Crear pedido con detalles":
                        limpiar_consola()
                        print(Fore.LIGHTBLUE_EX + "--- CREAR PEDIDO CON DETALLES ---")
                        usuarios = self._usu_servicio.listar()
                        for u in usuarios:
                            print(u)
                        id_usu = int(input("ID del usuario (cliente) que realiza el pedido: "))
                        usuario_ped = self._usu_servicio.buscar_por_id(id_usu)
                        pago_select = questionary.select(
                            message= "Seleccione la forma de pago",
                            choices= ["TARJETA","TRANSFERENCIA","EFECTIVO"]
                        ).ask()
                        pago_param = FormaPago[pago_select]

                        carrito = []
                        while True:
                            limpiar_consola()
                            print("--- AGREGANDO PRODUCTOS AL PEDIDO ---")
                            productos = self._prod_servicio.listar_disponibles_clientes()
                            for p in productos:
                                print(p)
                            id_prod = int(input("ID del producto a agregar (0 para terminar el carrito): "))
                            if id_prod == 0:
                                break
                            prod_ped = self._prod_servicio.buscar_por_id(id_prod)
                            cantidad = int(input(f"Cantidad de {prod_ped.nombre}: "))
                            carrito.append((cantidad,prod_ped))
                            print(Fore.GREEN + f"[OK] {prod_ped.nombre} (x{cantidad}) añadido al carrito")
                            continuar()

                        if not carrito:
                            print(Fore.YELLOW + "! Carrito vacio. Pedido cancelado")
                            continuar()
                            continue
                        pedido_final = self._ped_servicio.crear_pedido_con_detalles(pago_param,usuario_ped,carrito)
                        print(Fore.GREEN + f"[OK] Pedido creado con exito con id: {pedido_final.id}")
                        print(Fore.LIGHTGREEN_EX + f"Total consolidado: ${pedido_final.total:.2f}")
                        continuar()

                    case "3. Cambiar estado de un pedido":
                        limpiar_consola()
                        print(Fore.LIGHTBLUE_EX + "--- ACTUALIZAR ESTADO DE PEDIDO ---")
                        pedidos = self._ped_servicio.listar()
                        if not pedidos:
                            print(Fore.YELLOW + "! No hay pedidos registrados en el sistema")
                            continuar()
                            continue

                        for ped in pedidos:
                            print(ped)
                        id_ped = int(input("ID del pedido a modificar: "))
                        estado_select = questionary.select(
                            message= "Seleccione el nuevo estado:",
                            choices=["PENDIENTE","CONFIRMADO","TERMINADO","CANCELADO"]
                        ).ask()
                        estado_param = Estado[estado_select]
                        self._ped_servicio.cambiar_estado(id_ped, estado_param)
                        print(Fore.GREEN + "[OK] Estado actualizado con exito y stock recalculado si correspondia")
                        continuar()

                    case "4. Cambiar forma de pago":
                        limpiar_consola()
                        print(Fore.LIGHTBLUE_EX + "--- CAMBIAR FORMA DE PAGO ---")
                        pedidos = self._ped_servicio.listar()
                        if not pedidos:
                            print(Fore.YELLOW + "! No hay pedidos registrados en el sistema")
                            continuar()
                            continue

                        for ped in pedidos:
                            print(ped)
                        id_ped = int(input("ID del pedido a modificar: "))
                        pago_select = questionary.select(
                            message= "Seleccione el nuevo metodo de pago:",
                            choices= ["TARJETA","TRANSFERENCIA","EFECTIVO"]
                        ).ask()
                        pago_param = FormaPago[pago_select]
                        self._ped_servicio.cambiar_forma_pago(id_ped,pago_param)
                        print(Fore.GREEN + "[OK] Forma de pago actualizada")
                        continuar()

                    case "5. Eliminar Pedido":
                        limpiar_consola()
                        print(Fore.LIGHTBLUE_EX + "--- ELIMINAR UN PEDIDO ---")
                        pedidos = self._ped_servicio.listar()
                        if not pedidos:
                            print(Fore.YELLOW + "! No hay pedidos registrados en el sistema")
                            continuar()
                            continue

                        for ped in pedidos:
                            print(ped)
                        id_ped = int(input("ID del pedido a eliminar: "))
                        confirmar = questionary.select(
                            message= "¿Estas seguro? (Esto realizara una baja logica y devolvera stock si correspondia)",
                            choices= ["Si","No"]
                        ).ask()
                        match confirmar:
                            case "Si":
                                self._ped_servicio.eliminar(id_ped)
                                print(Fore.GREEN + "[OK] Pedido y detalles eliminados con exito")
                                continuar()

                            case "No":
                                print(Fore.YELLOW + "Operacion cancelada")
                                continuar()

                    case "0. Volver":
                        print("Volviendo al menu principal...")
                        continuar()
                        break

            except ValueError:
                print(Fore.RED + "X Error: Ingrese un numero entero valido")
                continuar()
            except FoodStoreError as e:
                print(Fore.RED + f"X Error de negocio: {e}")
                continuar()