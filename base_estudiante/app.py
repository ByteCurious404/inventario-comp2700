"""Aplicacion de inventario para COMP 2700. Version corregida."""
import json
from datetime import datetime
from pathlib import Path

from seguridad import verificar_clave

RAIZ = Path(__file__).resolve().parent
DATOS = RAIZ / "inventario.json"
USUARIOS = RAIZ / "usuarios.json"
LOG = RAIZ / "auditoria.jsonl"


def cargar_inventario():
    # Controla archivo ausente y JSON invalido. No sobrescribe el archivo.
    try:
        productos = json.loads(DATOS.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print("Error: no existe el archivo de inventario. Avise al administrador.")
        return None
    except json.JSONDecodeError:
        print("Error: el archivo de inventario tiene JSON invalido. No se modifica.")
        return None
    return productos


def guardar_inventario(productos):
    DATOS.write_text(json.dumps(productos, indent=2), encoding="utf-8")


def registrar_evento(usuario, accion, resultado, **detalles):
    # Guarda una linea JSON por evento en el log de auditoria.
    # Nunca se envian contrasenas ni hashes a esta funcion.
    evento = {}
    evento["fecha_hora"] = datetime.now().isoformat(timespec="seconds")
    evento["usuario"] = usuario
    evento["accion"] = accion
    evento["resultado"] = resultado
    for clave_dato, valor in detalles.items():
        evento[clave_dato] = valor
    with LOG.open("a", encoding="utf-8") as archivo:
        archivo.write(json.dumps(evento) + "\n")


def autenticar(nombre, clave):
    # Verifica la contrasena contra el hash guardado usando seguridad.py.
    try:
        usuarios = json.loads(USUARIOS.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: el archivo de usuarios no esta disponible.")
        return None
    for usuario in usuarios:
        if usuario["usuario"] == nombre:
            if verificar_clave(usuario["hash"], clave):
                sesion = {"usuario": nombre, "rol": usuario["rol"]}
                registrar_evento(nombre, "login", "exitoso")
                return sesion
            break
    # Mismo mensaje para clave incorrecta y usuario inexistente.
    registrar_evento(nombre, "login", "fallido")
    print("Credenciales incorrectas.")
    return None


def consultar_inventario(sesion):
    # Rechaza si no hay sesion activa.
    if sesion is None:
        print("Acceso denegado: debe iniciar sesion para consultar.")
        return
    productos = cargar_inventario()
    if productos is None:
        return
    for producto in productos:
        print(producto["id"], producto["nombre"], producto["cantidad"])


def modificar_cantidad(sesion, identificador, entrada):
    # Verifica sesion y rol AQUI, no solo en el menu.
    if sesion is None:
        registrar_evento("sin_sesion", "modificar", "rechazado",
                         producto=identificador)
        print("Acceso denegado: debe iniciar sesion para modificar.")
        return False
    if sesion["rol"] != "admin":
        registrar_evento(sesion["usuario"], "modificar", "rechazado",
                         producto=identificador)
        print("Acceso denegado: solo admin puede modificar cantidades.")
        return False
    # Valida entero entre 0 y 1000 sin interrumpir el programa.
    try:
        cantidad = int(entrada)
    except ValueError:
        print("Cantidad invalida: debe ser un numero entero.")
        return False
    if cantidad < 0 or cantidad > 1000:
        print("Cantidad fuera de rango: debe estar entre 0 y 1000.")
        return False
    productos = cargar_inventario()
    if productos is None:
        return False
    for producto in productos:
        if producto["id"] == identificador:
            anterior = producto["cantidad"]
            producto["cantidad"] = cantidad
            guardar_inventario(productos)
            registrar_evento(sesion["usuario"], "modificar", "exitoso",
                             producto=identificador, anterior=anterior,
                             nueva=cantidad)
            print("Cantidad actualizada.")
            return True
    # Producto inexistente: se informa, no se crea nada.
    print("Producto no existe.")
    return False


def main():
    print("Inventario")
    print("Estudiante:", input("Escriba su nombre: "))
    sesion = None
    while True:
        if sesion is None:
            nombre = input("Usuario (o salir): ")
            if nombre == "salir":
                break
            sesion = autenticar(nombre, input("Contrasena: "))
            continue
        print("1. Consultar | 2. Modificar | 3. Cerrar sesion | 0. Salir")
        opcion = input("Opcion: ")
        if opcion == "1":
            consultar_inventario(sesion)
        elif opcion == "2":
            identificador = input("ID del producto: ")
            entrada = input("Nueva cantidad: ")
            modificar_cantidad(sesion, identificador, entrada)
        elif opcion == "3":
            sesion = None
        elif opcion == "0":
            break
        else:
            print("Opcion invalida.")


if __name__ == "__main__":
    main()