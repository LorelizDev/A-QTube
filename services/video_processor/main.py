from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from shared.utils.logger import setup_logger

from .src.cache import get_from_cache, save_to_cache
from .src.downloader import download_audio
from .src.transcriber import transcribe_audio

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
        cached_transcription = get_from_cache(video_id)
        if cached_transcription:
            logger.info("Transcripción encontrada en caché.")
            return {"transcription": cached_transcription}

        # Descargar el audio
        audio_path = download_audio(video_url)

        # Transcribir el audio
        transcription = transcribe_audio(audio_path)

        # Guardar la transcripción en caché
        save_to_cache(video_id, transcription)

        logger.info("Proceso completado exitosamente.")
        return {"transcription": transcription}
    except Exception as e:
        logger.error(f"Error al procesar el video: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


def extract_video_id(url):
    """Extrae el ID del video de la URL de YouTube."""
    from urllib.parse import parse_qs, urlparse

    query = urlparse(url).query
    return parse_qs(query).get("v", [None])[0]
