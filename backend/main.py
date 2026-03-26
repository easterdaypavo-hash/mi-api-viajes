from fastapi import FastAPI
from pydantic import BaseModel
from backend.recomendador import recomendar_destinos
from backend.usuarios import registrar_usuario
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI()

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ ENDPOINT RAÍZ → sirve tu index.html
@app.get("/")
def root():
    return FileResponse("frontend/index.html")


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


# ENDPOINTS EXISTENTES
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