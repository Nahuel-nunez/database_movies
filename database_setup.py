import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

try:
    # Conectar a MySQL usando variables de entorno
    connection = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        port=int(os.getenv('MYSQL_PORT')),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD')
    )

    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS database_movies")
        cursor.execute("USE database_movies")

        # Crear tabla Usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255),
                telegram_id INT UNIQUE
            )
        """)

        # Crear tabla Peliculas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Peliculas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                titulo VARCHAR(255),
                año INT,
                género VARCHAR(100),
                director VARCHAR(255)
            )
        """)

        # Crear tabla Puntuaciones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Puntuaciones (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT,
                pelicula_id INT,
                puntuacion INT CHECK (puntuacion BETWEEN 1 AND 5),
                visto BOOLEAN,
                FOREIGN KEY (usuario_id) REFERENCES Usuarios(id),
                FOREIGN KEY (pelicula_id) REFERENCES Peliculas(id)
            )
        """)

        print("Base de datos y tablas creadas exitosamente.")

except Error as e:
    print("Error al conectar a MySQL:", e)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Conexión a MySQL cerrada.")
