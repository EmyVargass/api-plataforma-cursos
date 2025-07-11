# Este archivo define las TABLAS de la base de datos usando SQLAlchemy.
import uuid
from sqlalchemy import Boolean, Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID # Usamos UUID de Postgres, funciona bien con SQLite
from .database import Base # Importamos la Base desde nuestro archivo database.py

class Instructor(Base):
    __tablename__ = "instructores" # Nombre de la tabla
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    courses = relationship("Course", back_populates="instructor")

class Course(Base):
    __tablename__ = "cursos"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, index=True)
    is_published = Column(Boolean, default=False)
    instructor_id = Column(PG_UUID(as_uuid=True), ForeignKey("instructores.id"))
    instructor = relationship("Instructor", back_populates="courses")
    modules = relationship("Module", back_populates="course", cascade="all, delete-orphan")

class Module(Base):
    __tablename__ = "modulos"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, index=True)
    course_id = Column(PG_UUID(as_uuid=True), ForeignKey("cursos.id"))
    course = relationship("Course", back_populates="modules")
    lessons = relationship("Lesson", back_populates="module", cascade="all, delete-orphan")

class Lesson(Base):
    __tablename__ = "lecciones"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    video_url = Column(String)
    module_id = Column(PG_UUID(as_uuid=True), ForeignKey("modulos.id"))
    module = relationship("Module", back_populates="lessons")