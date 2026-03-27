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

# MODELOS
class SolicitudViaje(BaseModel):
    presupuesto: int
    tipo_viaje: str
    mes: str
    continente: str | None = None

class Usuario(BaseModel):
    nombre: str
    email: str
    password: str

# ENDPOINTS
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