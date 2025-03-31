from transformers import pipeline

from shared.utils.logger import setup_logger

from .cache import get_from_cache, save_to_cache

logger = setup_logger()

model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
text_generator = pipeline("text-generation", model=model_name)

PROMPT_TEMPLATE = """
Eres un asistente especializado en responder preguntas sobre videos de YouTube.
A continuación se proporciona la transcripción completa del video:

TRANSCRIPCIÓN:
{context}

PREGUNTA DEL USUARIO:
{question}

INSTRUCCIONES ESENCIALES:
1. Responde ÚNICAMENTE usando la información proporcionada en la transcripción.
2. SI LA INFORMACIÓN NO ESTÁ EN LA TRANSCRIPCIÓN, RESPONDE: "Lo siento, esa información no se menciona en el video."
3. NO INVENTES NINGÚN DETALLE NI USES CONOCIMIENTO EXTERNO.
4. Proporciona una respuesta clara, concisa y directamente relacionada con la pregunta.

Tu respuesta:
"""


def create_prompt(question: str, context: str) -> str:
    return PROMPT_TEMPLATE.format(question=question, context=context)


def generate_response(transcription, question):
    try:
        # Generar una clave única para la pregunta
        cache_key = f"{transcription[:50]}:{question}"

        cached_response = get_from_cache(cache_key)
        if cached_response:
            logger.info("Respuesta encontrada en caché.")
            return cached_response

        logger.info(f"Generando respuesta para la pregunta: {question}")

        prompt = create_prompt(question=question, context=transcription)

        response = text_generator(prompt, max_new_tokens=50)[0]["generated_text"]

        # Extraer y limpiar la respuesta generada
        response = response.split("Tu respuesta:")[-1].strip()

        # Limpiar cualquier texto adicional del prompt que pueda aparecer
        for word in ["PREGUNTA", "INSTRUCCIONES", "TRANSCRIPCIÓN"]:
            if word in response:
                response = response.split(word)[0].strip()

        save_to_cache(cache_key, response)

        logger.info("Respuesta generada y guardada en caché.")
        return response
    except Exception as e:
        logger.error(f"Error al generar la respuesta: {str(e)}")
        return "No se pudo generar una respuesta para esta pregunta."
