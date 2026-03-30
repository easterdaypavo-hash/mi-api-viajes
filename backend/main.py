from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from backend.recomendador import recomendar_destinos
from backend.usuarios import registrar_usuario
import os

# Inicializa FastAPI con documentación accesible
app = FastAPI(docs_url="/docs", redoc_url="/redoc")

# Configuración CORS → permite cualquier frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cualquier dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monta la carpeta frontend para archivos estáticos
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# ENDPOINT RAÍZ → sirve index.html (ajustado para Render)
@app.get("/")
def root():
    file_path = os.path.join("frontend", "index.html")
    return FileResponse(file_path)

# =====================
# MODELOS
# =====================

class SolicitudViaje(BaseModel):
    presupuesto: int
    tipo_viaje: str
    mes: str
    continente: str | None = None

class Usuario(BaseModel):
    nombre: str
    email: str
    password: str

class ChatRequest(BaseModel):
    mensaje: str

# =====================
# ENDPOINTS
# =====================

@app.post("/recomendar")
def recomendar(solicitud: SolicitudViaje):
    resultados = recomendar_destinos(
        solicitud.presupuesto,
        solicitud.tipo_viaje,
        solicitud.mes,
        solicitud.continente
    )
    return {"recomendaciones": resultados}

@app.post("/registro")
def registro(usuario: Usuario):
    resultado = registrar_usuario(
        usuario.nombre,
        usuario.email,
        usuario.password
    )
    return resultado

# =====================
# CHAT INTELIGENTE
# =====================

@app.post("/chat")
def chat(req: ChatRequest):
    texto = req.mensaje.lower()

    # Valores por defecto
    presupuesto = 150
    tipo_viaje = "cultura"
    mes = "verano"
    continente = None

    # Detectar tipo de viaje
    if "playa" in texto:
        tipo_viaje = "playa"
    elif "aventura" in texto:
        tipo_viaje = "aventura"
    elif "fiesta" in texto:
        tipo_viaje = "fiesta"
    elif "relax" in texto:
        tipo_viaje = "relax"
    elif "naturaleza" in texto:
        tipo_viaje = "naturaleza"

    # Detectar presupuesto
    if "barato" in texto or "económico" in texto:
        presupuesto = 100
    elif "medio" in texto:
        presupuesto = 200
    elif "lujo" in texto:
        presupuesto = 500

    # Detectar mes
    if "enero" in texto:
        mes = "enero"
    elif "febrero" in texto:
        mes = "febrero"
    elif "marzo" in texto:
        mes = "marzo"
    elif "abril" in texto:
        mes = "abril"
    elif "mayo" in texto:
        mes = "mayo"
    elif "junio" in texto:
        mes = "junio"
    elif "julio" in texto:
        mes = "julio"
    elif "agosto" in texto:
        mes = "agosto"
    elif "septiembre" in texto:
        mes = "septiembre"
    elif "octubre" in texto:
        mes = "octubre"
    elif "noviembre" in texto:
        mes = "noviembre"
    elif "diciembre" in texto:
        mes = "diciembre"

    # Llamar al recomendador real
    destinos = recomendar_destinos(
        presupuesto,
        tipo_viaje,
        mes,
        continente
    )

    # Construir respuesta
    if destinos:
        respuesta = "Te recomiendo estos destinos:\n"
        for d in destinos:
            respuesta += f"- {d['ciudad']} ({d['pais']})\n"
    else:
        respuesta = "No encontré destinos con esos criterios."

    return {"respuesta": respuesta}