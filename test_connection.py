import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def test_connection():
    try:
        # Conectar a MySQL usando variables de entorno
        connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            port=int(os.getenv('MYSQL_PORT')),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD')
        )

        if connection.is_connected():
            print("Conexión exitosa a MySQL!")
            db_info = connection.get_server_info()
            print("Versión del servidor MySQL:", db_info)
        else:
            print("Conexión fallida a MySQL.")

    except Error as e:
        print("Error al conectar a MySQL:", e)

    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Conexión a MySQL cerrada.")

if __name__ == "__main__":
    test_connection()
