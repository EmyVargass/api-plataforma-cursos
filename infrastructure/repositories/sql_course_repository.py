# Implementación REAL del repositorio de cursos usando SQL.
import uuid
from typing import Optional
from sqlalchemy.orm import Session
from application.repositories.i_course_repository import ICourseRepository
import domain.models as Domain
import infrastructure.models as Infra

class SqlCourseRepository(ICourseRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, course_db: Infra.Course) -> Domain.Course:
        return Domain.Course(
            id=course_db.id,
            title=course_db.title,
            is_published=course_db.is_published,
            instructor_id=course_db.instructor_id
        )

    def find_by_id(self, course_id: uuid.UUID) -> Optional[Domain.Course]:
        db_course = self.db.query(Infra.Course).filter(Infra.Course.id == course_id).first()
        return self._to_domain(db_course) if db_course else None

    def find_module_by_id(self, module_id: uuid.UUID) -> Optional[Domain.Module]:
        db_module = self.db.query(Infra.Module).filter(Infra.Module.id == module_id).first()
        if db_module:
            return Domain.Module(id=db_module.id, title=db_module.title, course_id=db_module.course_id)
        return None

    def add_module_to_course(self, course: Domain.Course, module: Domain.Module):
        db_module = Infra.Module(id=module.id, title=module.title, course_id=course.id)
        self.db.add(db_module)
        self.db.commit()

    def add_lesson_to_module(self, course: Domain.Course, module: Domain.Module, lesson: Domain.Lesson):
        db_lesson = Infra.Lesson(id=lesson.id, title=lesson.title, video_url=lesson.video_url, module_id=module.id)
        self.db.add(db_lesson)
        self.db.commit()

    def update(self, course: Domain.Course):
        db_course = self.db.query(Infra.Course).filter(Infra.Course.id == course.id).first()
        if db_course:
            db_course.is_published = course.is_published
            self.db.commit()