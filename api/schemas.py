# Define la "forma" de los datos que entran y salen de la API (JSON).
import uuid
from pydantic import BaseModel, EmailStr
from typing import List, Optional

# --- Esquemas para Instructor ---
class InstructorBase(BaseModel):
    name: str
    email: EmailStr

class InstructorCreate(InstructorBase):
    pass

class InstructorUpdate(InstructorBase):
    pass

class InstructorResponse(InstructorBase):
    id: uuid.UUID
    class Config:
        from_attributes = True # Permite a Pydantic leer datos desde objetos de SQLAlchemy.

# --- Esquemas para Lección ---
class LessonCreate(BaseModel):
    title: str
    video_url: str

class LessonResponse(LessonCreate):
    id: uuid.UUID
    module_id: uuid.UUID
    class Config:
        from_attributes = True

# --- Esquemas para Módulo ---
class ModuleCreate(BaseModel):
    title: str

class ModuleResponse(ModuleCreate):
    id: uuid.UUID
    course_id: uuid.UUID
    lessons: List[LessonResponse] = []
    class Config:
        from_attributes = True

# --- Esquemas para Curso ---
# No creamos un CRUD completo para cursos, solo lo necesario para los endpoints.