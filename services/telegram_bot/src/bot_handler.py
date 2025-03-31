# isort:skip_file
import os

import requests
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from .cache import get_from_cache, save_to_cache

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

VIDEO_PROCESSOR_URL = os.getenv(
    "VIDEO_PROCESSOR_URL", "http://video-processor:8000/process-video"
)
LLM_SERVICE_URL = os.getenv(
    "LLM_SERVICE_URL", "http://llm-service:8001/generate-response"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Soy un bot que te ayuda a procesar videos de YouTube. "
        "Envíame un enlace de YouTube para comenzar."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = update.message.text

    if "youtube.com" in message or "youtu.be" in message:
        await process_video(user_id, message, update)
    else:
        await handle_question(user_id, message, update)


async def process_video(user_id, video_url, update: Update):
    try:
        await update.message.reply_text(
            "Procesando el video... Esto puede tardar unos minutos."
        )

        # Llamar al microservicio de procesamiento de video
        response = requests.post(VIDEO_PROCESSOR_URL, json={"video_url": video_url})
        response.raise_for_status()
        data = response.json()

        # Guardar la transcripción y el título
        save_to_cache(f"user:{user_id}:transcription", data["transcription"])
        save_to_cache(f"user:{user_id}:title", data["title"])

        await update.message.reply_text(
            "Video procesado exitosamente.\n\n"
            "Ahora puedes hacer preguntas sobre el contenido del video."
        )
    except Exception as e:
        print(f"Error al procesar el video: {str(e)}")
        await update.message.reply_text("Ocurrió un error al procesar el video.")


async def handle_question(user_id, question, update: Update):
    try:
        transcription = get_from_cache(f"user:{user_id}:transcription")
        if not transcription:
            await update.message.reply_text(
                "No has procesado ningún video aún. Envíame un enlace de YouTube."
            )
            return

        title = get_from_cache(f"user:{user_id}:title")
        if not title:
            title = "Video sin título"

        await update.message.reply_text("Voy a revisar el video y te responderé...")

        # Llamar al microservicio de LLM para responder la pregunta
        answer = await ask_question(transcription, question, title)

        # Crear botones inline
        keyboard = [
            [
                InlineKeyboardButton("Hacer otra pregunta", callback_data="ask_more"),
                InlineKeyboardButton("Subir otro video", callback_data="new_video"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Enviar respuesta con botones
        await update.message.reply_text(answer, reply_markup=reply_markup)
    except Exception as e:
        print(f"Error al responder la pregunta: {str(e)}")
        await update.message.reply_text("Ocurrió un error al responder la pregunta.")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "ask_more":
        await query.message.reply_text(
            "¡Perfecto! ¿Qué más quieres saber sobre el video?"
        )
    elif query.data == "new_video":
        await query.message.reply_text(
            "Envíame el enlace del nuevo video que quieres procesar."
        )


async def ask_question(transcription, question, title):
    try:
        response = requests.post(
            LLM_SERVICE_URL,
            json={"transcription": transcription, "question": question, "title": title},
        )
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        print(f"Error al hacer la pregunta: {str(e)}")
        raise


def run_bot(token):
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_callback))

    app.run_polling()


if __name__ == "__main__":
    TELEGRAM_BOT_TOKEN = TELEGRAM_BOT_TOKEN
    run_bot(TELEGRAM_BOT_TOKEN)
