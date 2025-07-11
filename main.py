from fastapi import FastAPI
from infrastructure.database import engine
from infrastructure import models as infra_models
from api.routers import instructors, courses

# Esta línea crea todas las tablas en la base de datos si no existen.
infra_models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Plataforma de Cursos",
    description="API para gestionar cursos, módulos, lecciones e instructores, construida con Arquitectura Limpia."
)

# Se incluyen los routers de la API en la aplicación principal.
app.include_router(instructors.router)
app.include_router(courses.router)

@app.get("/")
def leer_raiz():
    return {"mensaje": "Bienvenido a la API de la Plataforma de Cursos. Visita /docs para ver la documentación interactiva."}