from faster_whisper import WhisperModel

from shared.utils.logger import setup_logger

logger = setup_logger()

model = WhisperModel("tiny")


def transcribe_audio(audio_path):
    try:
        logger.info(f"Transcribiendo audio desde: {audio_path}")
        segments, _ = model.transcribe(audio_path)
        transcription = " ".join(segment.text for segment in segments)
        logger.info("Transcripción completada.")
        return transcription
    except Exception as e:
        logger.error(f"Error al transcribir el audio: {str(e)}")
        raise
