# Base educativa — COMP 2700

Esta versión contiene debilidades intencionales. Utilice únicamente los datos
ficticios incluidos, en su computadora. No es una aplicación de producción.

Requiere Python 3.10 o posterior. Desde esta carpeta:

    python -m venv .venv

Windows CMD:

    .venv\Scripts\activate.bat

macOS/Linux:

    source .venv/bin/activate

Luego:

    python -m pip install -r requirements.txt
    python app.py

En algunos sistemas debe utilizar python3 en lugar de python.

Cuentas públicas y exclusivamente ficticias:
- admin / AdminDemo2700!
- user / UserDemo2700!

Comience probando consulta y cambio de cantidad con admin. La base no aplica
todos los controles: user también puede modificar, las claves están legibles,
las entradas inválidas pueden causar errores y no se guarda auditoría.
Los TODO de app.py guían las correcciones; seguridad.py contiene funciones listas.

Para migrar las contraseñas, cree un pequeño script que llame crear_hash para
cada cuenta y guarde el resultado en un campo hash. Elimine el campo clave del
archivo final. Adapte autenticar para llamar verificar_clave. No compare dos
hashes recién generados: sus salts serán diferentes.

Los archivos se resuelven respecto a app.py. Guarde una copia del inventario
antes de las pruebas de errores. Use P001 con cantidad 10 al comenzar.

Puede hacer pruebas directas desde un script que importe app:

    import app
    sesion = app.autenticar("user", "UserDemo2700!")
    app.modificar_cantidad(sesion, "P001", "99")

Después de corregir los permisos, esa llamada debe rechazarse sin cambiar P001.
Repita con None como sesión. No fabrique un diccionario con rol admin para
simular una sesión válida: esta aplicación confía en su propio proceso.

JSON almacena un documento completo (lista de productos o usuarios).
Solamente auditoria.jsonl utiliza un objeto por línea.

Complete este README con su nombre, ejecución, pruebas, fuentes y uso de IA.
No suba .venv, __pycache__, credenciales reales ni datos personales de terceros.






## Autor

Daniel Velez(Y00631574) — COMP 2700


## Estado del proyecto

Versión final corregida. 

Los TODO de app.py fueron resueltos:
contraseñas migradas a hashes Argon2id (usuarios.json ya viene migrado,
no es necesario correr migrar.py de nuevo), autorización verificada
dentro de las funciones protegidas, validación de cantidades entre 0 y
1000, auditoría en auditoria.jsonl y manejo de errores del archivo de
inventario.


## Ejecución

Nota sobre la estructura: los archivos del proyecto están dentro de la
carpeta base_estudiante del repositorio. Al clonar, entre primero a esa
carpeta antes de ejecutar cualquier comando.

    git clone https://github.com/ByteCurious404/inventario-comp2700.git
    cd inventario-comp2700
    cd base_estudiante

Requiere Python 3.10 o posterior. Desde esta carpeta:

    python -m venv .venv

Windows CMD:

    .venv\Scripts\activate.bat

macOS/Linux:

    source .venv/bin/activate

Luego:

    python -m pip install -r requirements.txt
    python app.py

En algunos sistemas debe utilizar python3 en lugar de python.

Nota: usuarios.json ya contiene los hashes Argon2id, por lo que NO es
necesario ejecutar migrar.py. Ese script se conserva como evidencia del
proceso de migración que se realizó una sola vez.

## Contenido

- app.py: aplicación de inventario con autenticación, autorización,
  validación, auditoría y manejo de errores.
- seguridad.py: funciones de hash Argon2id aplicadas.
- migrar.py: script de migración de contraseñas a hashes.
- usuarios.json: cuentas ficticias con hashes Argon2id.
- inventario.json: inventario ficticio.
- auditoria.jsonl: Log de auditoría.
- prueba_auth.py: prueba de autorización.

## Fuentes y uso de IA

Utilicé Lumo para: comprender los requisitos
de las preguntas, revisar el código base y corregir los TODO de app.py;
obtener recomendaciones para la redacción de las explicaciones de cada
parte; recibir ayuda con los comandos de terminal como: creación del entorno
virtual, git y GitHub; y la redacción de los pasos de trabajo y de este
README. Verifiqué cada recomendación ejecutando el programa personalmente con los
casos de prueba de cada parte: comprobé que la migración a hashes
funcionara entrando con las cuentas originales, que user no puede modificar
aunque se llame a la función desde un script, y que las entradas inválidas
no rompan el programa. 

Páginas útiles para búsquedas y apoyo:
- W3Schools (https://www.w3schools.com/python/) — consulta general de
  sintaxis de Python.
- Documentación oficial del módulo json de Python
  (https://docs.python.org/3/library/json.html).
- Documentación de argon2-cffi en PyPI
  (https://pypi.org/project/argon2-cffi/).
- Documentación de Git y GitHub
  (https://docs.github.com/es).

El código final lo ejecuté y validé yo mismo; las fuentes y la IA no
reemplazaron las pruebas.

## Limitaciones

Los permisos se aplican dentro del programa; una persona con acceso de
escritura a los archivos locales puede alterarlos, incluido el log de
auditoría. El prototipo no incluye cifrado de datos, MFA, ni protección
del log contra modificaciones externas.
