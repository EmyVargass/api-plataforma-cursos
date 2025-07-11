import uuid
from typing import List

# Creamos una excepción personalizada para nuestras reglas de negocio.
class ErrorDeDominio(Exception):
    pass

class Lesson:
    def __init__(self, title: str, video_url: str, module_id: uuid.UUID, id: uuid.UUID = None):
        self.id = id or uuid.uuid4()
        self.title = title
        self.video_url = video_url
        self.module_id = module_id

class Module:
    def __init__(self, title: str, course_id: uuid.UUID, id: uuid.UUID = None):
        self.id = id or uuid.uuid4()
        self.title = title
        self.course_id = course_id
        self._lessons: List[Lesson] = []

    @property
    def lessons(self) -> List[Lesson]:
        return self._lessons

    def add_lesson(self, lesson: Lesson):
        # La regla de "curso publicado" se valida en la entidad Curso.
        self._lessons.append(lesson)

class Course:
    def __init__(self, title: str, instructor_id: uuid.UUID, id: uuid.UUID = None, is_published: bool = False):
        self.id = id or uuid.uuid4()
        self.title = title
        self.instructor_id = instructor_id
        self.is_published = is_published
        self._modules: List[Module] = []

    @property
    def modules(self) -> List[Module]:
        return self._modules

    def publish(self):
        # Regla de negocio: no se puede publicar un curso ya publicado.
        if self.is_published:
            raise ErrorDeDominio("El curso ya está publicado.")
        self.is_published = True

    def add_module(self, module: Module):
        # Regla de negocio crítica: no se puede modificar un curso publicado.
        if self.is_published:
            raise ErrorDeDominio("No se puede añadir un módulo a un curso que ya está publicado.")
        self._modules.append(module)

class Instructor:
    def __init__(self, name: str, email: str, id: uuid.UUID = None):
        self.id = id or uuid.uuid4()
        self.name = name
        self.email = email
        self._courses: List[Course] = []

    @property
    def courses(self) -> List[Course]:
        return self._courses

    def update(self, name: str, email: str):
        self.name = name
        self.email = email