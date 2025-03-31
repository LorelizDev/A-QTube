FROM python:3.12-slim

WORKDIR /app

# Copiar primero los requirements para aprovechar la caché
COPY services/telegram_bot/requirements.txt /app/services/telegram_bot/
COPY shared /app/shared/

# Instalar dependencias
RUN pip install -r /app/services/telegram_bot/requirements.txt

# Copiar el resto del código
COPY services/telegram_bot /app/services/telegram_bot/

# Configurar PYTHONPATH
ENV PYTHONPATH=/app

WORKDIR /app/services/telegram_bot

# Asegurarse de que el script tenga permisos de ejecución
RUN chmod +x main.py

CMD ["python", "main.py"]
