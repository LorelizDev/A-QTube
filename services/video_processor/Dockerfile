# Base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copiar primero los requirements para aprovechar la caché de Docker
COPY services/video_processor/requirements.txt /app/services/video_processor/
COPY shared /app/shared/

# Instalar dependencias
RUN pip install -r /app/services/video_processor/requirements.txt

# Copiar el resto del código
COPY services/video_processor /app/services/video_processor/

# Crear directorio para descargas
RUN mkdir -p /app/services/video_processor/downloads

# Configurar PYTHONPATH
ENV PYTHONPATH=/app

WORKDIR /app/services/video_processor

# Expose port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
