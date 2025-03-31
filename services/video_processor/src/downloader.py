import yt_dlp

from shared.utils.logger import setup_logger

logger = setup_logger()


def download_audio(url, output_path="downloads/"):
    try:
        logger.info(f"Descargando audio desde: {url}")
        ydl_opts = {
            "format": "bestaudio",
            "outtmpl": f"{output_path}/%(id)s.%(ext)s",  # Usa el ID del video como nombre
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_title = info["title"]
            file_path = ydl.prepare_filename(info)
        logger.info(f"Audio descargado en: {file_path}")
        return file_path, video_title
    except Exception as e:
        logger.error(f"Error al descargar el audio: {str(e)}")
        raise
