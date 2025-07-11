# Esta es la implementación REAL del repositorio de instructores usando SQL.
import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from application.repositories.i_instructor_repository import IInstructorRepository
import domain.models as Domain
import infrastructure.models as Infra

class SqlInstructorRepository(IInstructorRepository):
    def __init__(self, db: Session):
        self.db = db

    # Mapeador para convertir del modelo de base de datos al modelo de dominio.
    def _to_domain(self, instructor_db: Infra.Instructor) -> Domain.Instructor:
        return Domain.Instructor(
            id=instructor_db.id,
            name=instructor_db.name,
            email=instructor_db.email
        )

    def find_by_id(self, instructor_id: uuid.UUID) -> Optional[Domain.Instructor]:
        db_instructor = self.db.query(Infra.Instructor).filter(Infra.Instructor.id == instructor_id).first()
        return self._to_domain(db_instructor) if db_instructor else None

    def find_all(self) -> List[Domain.Instructor]:
        db_instructors = self.db.query(Infra.Instructor).all()
        return [self._to_domain(i) for i in db_instructors]

    def add(self, instructor: Domain.Instructor):
        db_instructor = Infra.Instructor(id=instructor.id, name=instructor.name, email=instructor.email)
        self.db.add(db_instructor)
        self.db.commit()

    def update(self, instructor: Domain.Instructor):
        db_instructor = self.db.query(Infra.Instructor).filter(Infra.Instructor.id == instructor.id).first()
        if db_instructor:
            db_instructor.name = instructor.name
            db_instructor.email = instructor.email
            self.db.commit()

    def delete(self, instructor_id: uuid.UUID):
        db_instructor = self.db.query(Infra.Instructor).filter(Infra.Instructor.id == instructor_id).first()
        if db_instructor:
            self.db.delete(db_instructor)
            self.db.commit()

    def has_public_courses(self, instructor_id: uuid.UUID) -> bool:
        count = self.db.query(Infra.Course).filter(
            Infra.Course.instructor_id == instructor_id,
            Infra.Course.is_published == True
        ).count()
        return count > 0