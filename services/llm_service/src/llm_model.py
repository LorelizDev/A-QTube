from transformers import pipeline

from services.llm_service.src.cache import get_from_cache, save_to_cache
from shared.utils.logger import setup_logger

logger = setup_logger()

model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
text_generator = pipeline(
    "text-generation",
    model=model_name,
    truncation=True,  # Habilitar truncamiento automático
)

PROMPT_TEMPLATE = """Contexto: {context}
Título del video: {title}
Pregunta: {question}
Instrucción: Responde brevemente usando solo la información del contexto.
Si no está la información, di: Lo siento, esa información no se menciona en el video.
Respuesta:"""


def create_prompt(question: str, context: str, title: str) -> str:
    return PROMPT_TEMPLATE.format(question=question, context=context, title=title)


def generate_response(transcription, question, title):
    try:
        # Generar una clave única para la pregunta
        cache_key = f"{transcription[:50]}:{question}"

        cached_response = get_from_cache(cache_key)
        if cached_response:
            logger.info("Respuesta encontrada en caché.")
            return cached_response

        logger.info(f"Generando respuesta para la pregunta: {question}")

        # Limitar el contexto a aproximadamente 1500 caracteres
        if len(transcription) > 1500:
            transcription = transcription[:1500] + "..."

        prompt = create_prompt(question=question, context=transcription, title=title)

        logger.info(f"Prompt generado con título: {title}")

        response = text_generator(
            prompt,
            max_new_tokens=100,
            num_return_sequences=1,
            pad_token_id=text_generator.tokenizer.eos_token_id,
            do_sample=True,
            temperature=0.3,
            top_p=0.9,
            repetition_penalty=1.2,
            no_repeat_ngram_size=3,
        )[0]["generated_text"]

        # Extraer y limpiar la respuesta generada
        response = response.split("Respuesta:")[-1].strip()

        save_to_cache(cache_key, response)

        logger.info("Respuesta generada y guardada en caché.")
        return response
    except Exception as e:
        logger.error(f"Error al generar la respuesta: {str(e)}")
        return "No se pudo generar una respuesta para esta pregunta."
