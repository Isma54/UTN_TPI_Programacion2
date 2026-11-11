# Food Store - TPI Programación II

Sistema de gestión de pedidos de comida en consola. El programa aplica los conceptos de POO para procesar, validar y organizar el flujo de un comercio de comida rapida mediante el uso de python. Los datos se guardan en memoria durante la ejecucion, al cerrar el programa se pierden.

## Requisitos
- Python 3.12 o superior
- Dependencias de consola: `questionary` y `colorama`

Instalar dependencias:

`python -m pip install questionary`

`python -m pip install colorama`

## Ejecución

Desde la capeta raíz del proyecto:

`python main.py`

Para ejecutar las pruebas automatizadas:

`python pruebas.py`

## Credenciales de acceso

´main.py´ carga estos usuarios al iniciar su ejecucion:

- Administrador: `administrador@foodstore.com` / `admin123`
- Cliente: `cliente@foodstore.com´ / ´cliente123`

## Organización

- `entidades/`: Capa que contiene el modelo del dominio y sus validaciones
- `servicios/`: Capa encargada de las reglas de negocio y manipulación de las colecciones
- `consola/`: Capa que contiene los menús interactivos para el administrador y el cliente
- `enums`: Capa que contiene los roles, estados y formas de pago
- `excepciones`: Capa que contiene las excepciones del dominio
- `main.py`: Ejecuta el inicio de sesión además de los respectivos menús
- `pruebas.py`: Ejecuta los test automáticos, valida cálculos, stock y la correcta captura de excepciones

Repositorio: https://github.com/Isma54/UTN_TPI_Programacion2

Video demostrativo: PENDIENTE
