import uuid
from domain.models import Module, Lesson, ErrorDeDominio
from application.repositories.i_course_repository import ICourseRepository

class CourseService:
    def __init__(self, repo: ICourseRepository):
        self.repo = repo

    def create_module(self, course_id: uuid.UUID, title: str) -> Module:
        curso = self.repo.find_by_id(course_id)
        if not curso:
            raise ValueError("Curso no encontrado.")
        
        # La regla de negocio se ejecuta en la entidad de dominio.
        # El servicio solo orquesta la operación.
        nuevo_modulo = Module(title=title, course_id=curso.id)
        curso.add_module(nuevo_modulo) 
        
        self.repo.add_module_to_course(curso, nuevo_modulo)
        return nuevo_modulo

    def create_lesson(self, module_id: uuid.UUID, title: str, video_url: str) -> Lesson:
        modulo = self.repo.find_module_by_id(module_id)
        if not modulo:
            raise ValueError("Módulo no encontrado.")
        
        curso = self.repo.find_by_id(modulo.course_id)
        if not curso:
            raise ValueError("El curso asociado al módulo no fue encontrado.")

        # Validamos la regla de negocio antes de crear la lección.
        if curso.is_published:
            raise ErrorDeDominio("No se puede añadir una lección a un curso que ya está publicado.")
            
        nueva_leccion = Lesson(title=title, video_url=video_url, module_id=modulo.id)
        modulo.add_lesson(nueva_leccion)
        
        self.repo.add_lesson_to_module(curso, modulo, nueva_leccion)
        return nueva_leccion

    def publish_course(self, course_id: uuid.UUID):
        curso = self.repo.find_by_id(course_id)
        if not curso:
            raise ValueError("Curso no encontrado.")
        
        # La lógica de publicación está encapsulada en la entidad.
        curso.publish() 
        self.repo.update(curso)