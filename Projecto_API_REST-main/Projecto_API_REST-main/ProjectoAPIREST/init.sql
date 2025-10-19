-- Script de inicialización de la base de datos
-- Se ejecuta automáticamente cuando se crea el contenedor de MySQL

USE movies_catalog;

-- Crear tabla de películas (se hará automáticamente con SQLAlchemy)
-- Pero podemos insertar algunos datos de ejemplo

-- Esperar a que SQLAlchemy cree las tablas
-- Insertar datos de ejemplo
INSERT INTO peliculas (nombre, categoria, año, director, duracion, calificacion) VALUES
('El Padrino', 'Drama', 1972, 'Francis Ford Coppola', 175, 9.2),
('Pulp Fiction', 'Crimen', 1994, 'Quentin Tarantino', 154, 8.9),
('El Señor de los Anillos: La Comunidad del Anillo', 'Fantasía', 2001, 'Peter Jackson', 178, 8.8),
('Matrix', 'Ciencia Ficción', 1999, 'Lana Wachowski, Lilly Wachowski', 136, 8.7),
('Forrest Gump', 'Drama', 1994, 'Robert Zemeckis', 142, 8.8),
('El Caballero Oscuro', 'Acción', 2008, 'Christopher Nolan', 152, 9.0),
('Schindler''s List', 'Drama', 1993, 'Steven Spielberg', 195, 9.0),
('Goodfellas', 'Crimen', 1990, 'Martin Scorsese', 146, 8.7),
('12 Hombres en Pugna', 'Drama', 1957, 'Sidney Lumet', 96, 9.0),
('Cadena Perpetua', 'Drama', 1994, 'Frank Darabont', 142, 9.3);


