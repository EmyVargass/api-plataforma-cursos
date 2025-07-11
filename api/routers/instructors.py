# Define los endpoints (rutas) para todo lo relacionado con los instructores.
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
from application.services.instructor_service import InstructorService
from infrastructure.database import get_db
from infrastructure.repositories.sql_instructor_repository import SqlInstructorRepository
from domain.models import ErrorDeDominio
from api import schemas

# Creamos un "router" para agrupar los endpoints de instructores.
router = APIRouter(prefix="/api/instructors", tags=["Instructores"])

# Función de ayuda para la inyección de dependencias.
# Crea el servicio con su repositorio en cada petición.
def obtener_servicio_instructor(db: Session = Depends(get_db)) -> InstructorService:
    repo = SqlInstructorRepository(db)
    return InstructorService(repo)

@router.post("/", response_model=schemas.InstructorResponse, status_code=201)
def crear_instructor(req: schemas.InstructorCreate, service: InstructorService = Depends(obtener_servicio_instructor)):
    return service.create_instructor(name=req.name, email=req.email)

@router.get("/", response_model=List[schemas.InstructorResponse])
def obtener_todos_los_instructores(service: InstructorService = Depends(obtener_servicio_instructor)):
    return service.get_all_instructors()

@router.get("/{instructor_id}", response_model=schemas.InstructorResponse)
def obtener_instructor(instructor_id: uuid.UUID, service: InstructorService = Depends(obtener_servicio_instructor)):
    instructor = service.get_instructor_by_id(instructor_id)
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor no encontrado")
    return instructor

@router.put("/{instructor_id}", response_model=schemas.InstructorResponse)
def actualizar_instructor(instructor_id: uuid.UUID, req: schemas.InstructorUpdate, service: InstructorService = Depends(obtener_servicio_instructor)):
    try:
        return service.update_instructor(instructor_id, req.name, req.email)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{instructor_id}", status_code=204)
def eliminar_instructor(instructor_id: uuid.UUID, service: InstructorService = Depends(obtener_servicio_instructor)):
    try:
        service.delete_instructor(instructor_id)
    except ErrorDeDominio as e:
        # Capturamos el error de nuestra regla de negocio y lo mostramos al usuario.
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))