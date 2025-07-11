# Este archivo configura la conexión a la base de datos con SQLAlchemy.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Usamos SQLite para desarrollo local por su simplicidad.
SQLALCHEMY_DATABASE_URL = "sqlite:///./plataforma_cursos.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} # Requerido solo para SQLite.
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para que los modelos de la base de datos hereden de ella.
Base = declarative_base()

# Función para obtener una sesión de la base de datos en cada petición.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()