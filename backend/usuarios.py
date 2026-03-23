import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def cargar_usuarios():
    with open("data/usuarios.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_usuarios(usuarios):
    with open("data/usuarios.json", "w", encoding="utf-8") as archivo:
        json.dump(usuarios, archivo, indent=4)


def registrar_usuario(nombre, email, password):
    usuarios = cargar_usuarios()

    # comprobar si ya existe
    for u in usuarios:
        if u["email"] == email:
            return {"error": "El usuario ya existe"}

    nuevo = {
        "nombre": nombre,
        "email": email,
        "password": password
    }

    usuarios.append(nuevo)
    guardar_usuarios(usuarios)

    return {"mensaje": "Usuario registrado correctamente"}