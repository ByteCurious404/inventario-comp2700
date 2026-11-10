"""Prueba de autorizacion: llamo modificar_cantidad directamente."""
import app

# CASO 1: sesion de user (sin rol admin), tomada de autenticar
sesion_user = app.autenticar("user", "UserDemo2700!")
print("Prueba 1 - user intenta modificar:")
app.modificar_cantidad(sesion_user, "P001", "99")

# CASO 2: sesion None
print("\nPrueba 2 - sesion None intenta modificar:")
app.modificar_cantidad(None, "P001", "99")

# CASO 3: sesion None intenta consultar
print("\nPrueba 3 - sesion None intenta consultar:")
app.consultar_inventario(None)

# Verifico que P001 sigue en 10
print("\nEstado final de P001:")
productos = app.cargar_inventario()
for p in productos:
    if p["id"] == "P001":
        print(p)