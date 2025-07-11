import uuid
from typing import List, Optional
from domain.models import Instructor, ErrorDeDominio
from application.repositories.i_instructor_repository import IInstructorRepository

class InstructorService:
    # El servicio usa el "contrato" (interfaz), no la implementación directa.
    def __init__(self, repo: IInstructorRepository):
        self.repo = repo

    def create_instructor(self, name: str, email: str) -> Instructor:
        nuevo_instructor = Instructor(name=name, email=email)
        self.repo.add(nuevo_instructor)
        return nuevo_instructor

    def get_all_instructors(self) -> List[Instructor]:
        return self.repo.find_all()

    def get_instructor_by_id(self, instructor_id: uuid.UUID) -> Optional[Instructor]:
        return self.repo.find_by_id(instructor_id)

    def update_instructor(self, instructor_id: uuid.UUID, name: str, email: str) -> Instructor:
        instructor = self.repo.find_by_id(instructor_id)
        if not instructor:
            raise ValueError("Instructor no encontrado.")
        instructor.update(name=name, email=email)
        self.repo.update(instructor)
        return instructor

    def delete_instructor(self, instructor_id: uuid.UUID):
        # Regla de negocio crítica: no eliminar instructores con cursos públicos.
        if self.repo.has_public_courses(instructor_id):
            raise ErrorDeDominio("No se puede eliminar un instructor que aún tenga cursos públicos.")
        
        instructor = self.repo.find_by_id(instructor_id)
        if not instructor:
            raise ValueError("Instructor no encontrado.")
            
        self.repo.delete(instructor_id)