# Define los endpoints para el contenido de los cursos.
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from application.services.course_service import CourseService
from infrastructure.database import get_db
from infrastructure.repositories.sql_course_repository import SqlCourseRepository
from domain.models import ErrorDeDominio
from api import schemas

router = APIRouter(tags=["Contenido de Cursos"])

# Función de ayuda para la inyección de dependencias.
def obtener_servicio_curso(db: Session = Depends(get_db)) -> CourseService:
    repo = SqlCourseRepository(db)
    return CourseService(repo)

@router.post("/api/courses/{course_id}/modules", response_model=schemas.ModuleResponse, status_code=201)
def crear_modulo_para_curso(course_id: uuid.UUID, req: schemas.ModuleCreate, service: CourseService = Depends(obtener_servicio_curso)):
    try:
        modulo = service.create_module(course_id, req.title)
        # Convertimos el objeto de dominio a un diccionario para que Pydantic pueda validarlo.
        # Esto es un pequeño truco ya que el objeto de dominio no tiene la lista de lecciones.
        modulo_dict = modulo.__dict__
        modulo_dict['lessons'] = []
        return modulo_dict
    except (ValueError, ErrorDeDominio) as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/api/modules/{module_id}/lessons", response_model=schemas.LessonResponse, status_code=201)
def crear_leccion_para_modulo(module_id: uuid.UUID, req: schemas.LessonCreate, service: CourseService = Depends(obtener_servicio_curso)):
    try:
        return service.create_lesson(module_id, req.title, req.video_url)
    except (ValueError, ErrorDeDominio) as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/api/courses/{course_id}/publish", status_code=200)
def publicar_curso(course_id: uuid.UUID, service: CourseService = Depends(obtener_servicio_curso)):
    try:
        service.publish_course(course_id)
        return {"mensaje": "El curso ha sido publicado exitosamente."}
    except (ValueError, ErrorDeDominio) as e:
        raise HTTPException(status_code=400, detail=str(e))