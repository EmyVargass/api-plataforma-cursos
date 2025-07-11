-- Script para la creación de la estructura de la base de datos de la Plataforma de Cursos.

-- Eliminar tablas si ya existen, para poder ejecutar el script varias veces.
DROP TABLE IF EXISTS lecciones;
DROP TABLE IF EXISTS modulos;
DROP TABLE IF EXISTS cursos;
DROP TABLE IF EXISTS instructores;

-- Tabla para almacenar los instructores
CREATE TABLE instructores (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
);

-- Tabla para almacenar los cursos
CREATE TABLE cursos (
    id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    is_published BOOLEAN DEFAULT false,
    instructor_id UUID NOT NULL,
    FOREIGN KEY (instructor_id) REFERENCES instructores (id) ON DELETE RESTRICT
);

-- Tabla para almacenar los módulos de cada curso
CREATE TABLE modulos (
    id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    course_id UUID NOT NULL,
    FOREIGN KEY (course_id) REFERENCES cursos (id) ON DELETE CASCADE
);

-- Tabla para almacenar las lecciones de cada módulo
CREATE TABLE lecciones (
    id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    video_url VARCHAR(255),
    module_id UUID NOT NULL,
    FOREIGN KEY (module_id) REFERENCES modulos (id) ON DELETE CASCADE
);

-- Mensaje de finalización
-- \echo 'Estructura de la base de datos creada exitosamente.';