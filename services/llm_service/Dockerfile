FROM python:3.12-slim

WORKDIR /app

# Copiar primero los requirements para aprovechar la caché
COPY services/llm_service/requirements.txt /app/services/llm_service/
COPY shared /app/shared/

# Instalar dependencias
RUN pip install -r /app/services/llm_service/requirements.txt

# Copiar el resto del código
COPY services/llm_service /app/services/llm_service/

# Configurar PYTHONPATH
ENV PYTHONPATH=/app

WORKDIR /app/services/llm_service

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
