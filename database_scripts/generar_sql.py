# generar_sql.py
from faker import Faker
import uuid

fake = Faker('es_ES')

# Abre un archivo para escribir los comandos SQL
with open('database_scripts/seed.sql', 'w', encoding='utf-8') as f:
    f.write("-- Script para insertar más de 100 registros de prueba en cada tabla.\n\n")

    # --- Generar 101 Instructores ---
    f.write("-- Insertando 101 Instructores\n")
    instructores = []
    for _ in range(101):
        instructor_id = str(uuid.uuid4())
        name = fake.name().replace("'", "''") # Escapar comillas simples
        email = fake.unique.email()
        instructores.append(instructor_id)
        f.write(f"INSERT INTO instructores (id, name, email) VALUES ('{instructor_id}', '{name}', '{email}');\n")
    f.write("\n")

    # --- Generar 101 Cursos ---
    f.write("-- Insertando 101 Cursos\n")
    cursos = []
    for i in range(101):
        curso_id = str(uuid.uuid4())
        title = f"Curso de {fake.job()}".replace("'", "''")
        is_published = fake.boolean(chance_of_getting_true=80)
        instructor_id = instructores[i]
        cursos.append(curso_id)
        f.write(f"INSERT INTO cursos (id, title, is_published, instructor_id) VALUES ('{curso_id}', '{title}', {is_published}, '{instructor_id}');\n")
    f.write("\n")

    # --- Generar 101 Módulos ---
    f.write("-- Insertando 101 Módulos\n")
    modulos = []
    for i in range(101):
        modulo_id = str(uuid.uuid4())
        title = f"Módulo {i+1}: Introducción".replace("'", "''")
        curso_id = cursos[i]
        modulos.append(modulo_id)
        f.write(f"INSERT INTO modulos (id, title, course_id) VALUES ('{modulo_id}', '{title}', '{curso_id}');\n")
    f.write("\n")

    # --- Generar 101 Lecciones ---
    f.write("-- Insertando 101 Lecciones\n")
    for i in range(101):
        leccion_id = str(uuid.uuid4())
        title = f"Lección {i+1}: Primeros pasos".replace("'", "''")
        video_url = fake.url()
        modulo_id = modulos[i]
        f.write(f"INSERT INTO lecciones (id, title, video_url, module_id) VALUES ('{leccion_id}', '{title}', '{video_url}', '{modulo_id}');\n")

print("Archivo 'database_scripts/seed.sql' generado exitosamente con más de 100 registros por tabla.")