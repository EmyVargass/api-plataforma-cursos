# Este es el "Contrato" para las operaciones de los cursos.
from abc import ABC, abstractmethod
from typing import Optional
import uuid
from domain.models import Course, Module, Lesson

class ICourseRepository(ABC):
    @abstractmethod
    def find_by_id(self, course_id: uuid.UUID) -> Optional[Course]: pass

    @abstractmethod
    def find_module_by_id(self, module_id: uuid.UUID) -> Optional[Module]: pass

    @abstractmethod
    def add_module_to_course(self, course: Course, module: Module): pass
    
    @abstractmethod
    def add_lesson_to_module(self, course: Course, module: Module, lesson: Lesson): pass
    
    @abstractmethod
    def update(self, course: Course): pass