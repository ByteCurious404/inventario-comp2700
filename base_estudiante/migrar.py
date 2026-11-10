"""Script para migrar usuarios.json a hashes Argon2id. Se ejecuta una sola vez."""

import json
from pathlib import Path
from seguridad import crear_hash

USUARIOS = Path(__file__).parent / "usuarios.json"

usuarios = json.loads(USUARIOS.read_text(encoding="utf-8"))

for usuario in usuarios:
    usuario["hash"] = crear_hash(usuario["clave"])  # genera el hash
    del usuario["clave"]  # elimina la contrasena legible

USUARIOS.write_text(json.dumps(usuarios, indent=2), encoding="utf-8")

print("Migracion completa.")