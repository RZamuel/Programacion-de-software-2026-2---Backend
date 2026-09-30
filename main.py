import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.miembros import miembros_router
from src.api.membresias import membresias_router
from src.api.inscripciones import inscripciones_router
from src.api.entrenadores import entrenadores_router
from src.api.clases import clases_router
from src.api.pagos import pagos_router
from src.api.reservas import reservas_router
from src.api.rutinas import rutinas_router

app = FastAPI(
    title="API Gimnasio — Programacion de software 2026-2",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en desarrollo; luego el origen real del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(miembros_router)
app.include_router(membresias_router)
app.include_router(inscripciones_router)
app.include_router(entrenadores_router)
app.include_router(clases_router)
app.include_router(pagos_router)
app.include_router(reservas_router)
app.include_router(rutinas_router)


@app.get("/")
def raiz():
    return {"mensaje": "API en marcha"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
