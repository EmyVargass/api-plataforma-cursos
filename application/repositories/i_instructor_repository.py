# Este archivo es un "Contrato". Define las reglas que cualquier repositorio de instructores debe seguir.
from abc import ABC, abstractmethod
from typing import List, Optional
import uuid
from domain.models import Instructor

class IInstructorRepository(ABC):
    @abstractmethod
    def find_by_id(self, instructor_id: uuid.UUID) -> Optional[Instructor]: pass
    
    @abstractmethod
    def find_all(self) -> List[Instructor]: pass
    
    @abstractmethod
    def add(self, instructor: Instructor): pass
    
    @abstractmethod
    def update(self, instructor: Instructor): pass
    
    @abstractmethod
    def delete(self, instructor_id: uuid.UUID): pass
    
    @abstractmethod
    def has_public_courses(self, instructor_id: uuid.UUID) -> bool: pass