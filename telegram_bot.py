import logging
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Función para conectar a la base de datos
def connect_db():
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        port=int(os.getenv('MYSQL_PORT')),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DB')
    )

# Comando /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('¡Hola! Envía una película para recomendar.')

# Manejar mensajes de texto
async def handle_message(update: Update, context: CallbackContext) -> None:
    movie_title = update.message.text
    user_id = update.message.from_user.id

    try:
        connection = connect_db()
        cursor = connection.cursor()

        # Guardar la película recomendada en la base de datos
        cursor.execute("INSERT INTO Peliculas (titulo) VALUES (%s)", (movie_title,))
        connection.commit()

        await update.message.reply_text(f'Recomendación de película "{movie_title}" guardada.')
    except Error as e:
        logger.error("Error al insertar en la base de datos:", e)
        await update.message.reply_text('Hubo un error al guardar la recomendación.')
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

# Función principal
def main():
    # Token del bot
    TOKEN = os.getenv('TELEGRAM_TOKEN')

    # Crear Application
    application = Application.builder().token(TOKEN).build()

    # Manejar comandos y mensajes
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Iniciar el bot
    application.run_polling()

if __name__ == '__main__':
    main()
