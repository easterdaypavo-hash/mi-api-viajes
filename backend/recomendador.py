import json
import os

# 📌 Ruta base del archivo actual (backend/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def cargar_destinos():
    # 📌 Subimos un nivel y entramos en /data
    path = os.path.join(BASE_DIR, "..", "data", "destinos.json")

    with open(path, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def recomendar_destinos(presupuesto, tipo_viaje, mes, continente=None):
    destinos = cargar_destinos()
    resultados = []

    for destino in destinos:

        # 🌍 FILTRO POR CONTINENTE
        if continente and destino.get("continente", "").lower() != continente.lower():
            continue

        puntuacion = 0

        # 🎯 Tipo de viaje
        if tipo_viaje.lower() in [t.lower() for t in destino.get("tipo", [])]:
            puntuacion += 2

        # 💰 Presupuesto
        if destino.get("precio_vuelo", 99999) <= presupuesto:
            puntuacion += 1

        # 📅 Mes recomendado
        if mes.lower() in [m.lower() for m in destino.get("mes_recomendado", [])]:
            puntuacion += 1

        resultados.append({
            "ciudad": destino.get("ciudad"),
            "pais": destino.get("pais"),
            "continente": destino.get("continente"),
            "precio_vuelo": destino.get("precio_vuelo"),
            "puntuacion": puntuacion,
            "aeropuerto": destino.get("aeropuerto"),
            "tiempo_vuelo_horas": destino.get("tiempo_vuelo_horas"),
            "imagen": destino.get("imagen"),
            "lat": destino.get("lat"),
            "lng": destino.get("lng"),
            "descripcion": destino.get("descripcion")
        })

    resultados.sort(key=lambda x: x["puntuacion"], reverse=True)

    return resultados[:3]