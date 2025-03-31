from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from services.video_processor.src.cache import get_from_cache, save_to_cache
from services.video_processor.src.downloader import download_audio
from services.video_processor.src.transcriber import transcribe_audio
from shared.utils.logger import setup_logger

logger = setup_logger()

app = FastAPI()


class VideoRequest(BaseModel):
    video_url: str


@app.post("/process-video")
async def process_video_endpoint(request: VideoRequest):
    try:
        video_url = request.video_url
        video_id = extract_video_id(video_url)
        logger.info(f"Procesando video con ID: {video_id}")

        # Verificar si el video ya está en caché
        cached_data = get_from_cache(video_id)
        if cached_data:
            logger.info("Datos encontrados en caché.")
            return cached_data

        # Descargar el audio y obtener el título del video
        audio_path, video_title = download_audio(video_url)

        # Transcribir el audio
        transcription = transcribe_audio(audio_path)

        # Crear respuesta con transcripción y título
        response_data = {"transcription": transcription, "title": video_title}

        # Guardar en caché
        save_to_cache(video_id, response_data)

        logger.info("Proceso completado exitosamente.")
        return response_data
    except Exception as e:
        logger.error(f"Error al procesar el video: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


def extract_video_id(url):
    """Extrae el ID del video de la URL de YouTube."""
    from urllib.parse import parse_qs, urlparse

    parsed_url = urlparse(url)

    # Maneja enlaces cortos de youtu.be
    if "youtu.be" in parsed_url.netloc:
        return parsed_url.path.strip("/")

    # Maneja enlaces tradicionales de youtube.com
    query = parsed_url.query
    return parse_qs(query).get("v", [None])[0]
