# A-QTube: Bot de Telegram con Procesamiento de Videos de YouTube y Respuestas IA

Este proyecto es un sistema distribuido que permite procesar videos de YouTube, transcribir su contenido y responder preguntas sobre el mismo utilizando inteligencia artificial.

## Arquitectura del Sistema

El sistema está compuesto por tres microservicios principales:

1. **Telegram Bot** (Puerto: Default Telegram)
   - Interfaz de usuario a través de Telegram
   - Maneja las interacciones con los usuarios
   - Coordina las solicitudes entre servicios

2. **Video Processor** (Puerto: 8000)
   - Descarga y procesa videos de YouTube
   - Extrae el audio y realiza transcripciones
   - Utiliza Faster Whisper para transcripción

3. **LLM Service** (Puerto: 8001)
   - Servicio de procesamiento de lenguaje natural
   - Genera respuestas basadas en las transcripciones
   - Utiliza TinyLlama como modelo de IA

## Tecnologías Utilizadas

- **Python 3.12**
- **Docker** y **Docker Compose**
- **Redis** para caché
- **FastAPI** para servicios web
- **python-telegram-bot** para la interfaz de Telegram
- **yt-dlp** para descarga de videos
- **Faster Whisper** para transcripción de audio
- **TinyLlama** para procesamiento de lenguaje natural
- **Transformers** (Hugging Face) para el modelo de IA

## Requisitos Previos

- Python 3.10+
- Docker y Docker Compose
- Token de Bot de Telegram (obtenido a través de @BotFather)

## Instalación y Configuración

1. Clonar el repositorio:
```bash
git clone https://github.com/LorelizDev/A-QTube.git
cd A-QTube
```

2. Crear archivo `.env` en la raíz del proyecto:
```bash
TELEGRAM_BOT_TOKEN=tu_token_aquí
REDIS_URL=redis://redis:6379
VIDEO_PROCESSOR_URL=http://video-processor:8000
LLM_SERVICE_URL=http://llm-service:8001
```

3. Construir y ejecutar los contenedores:
```bash
docker-compose up --build
```

## Uso del Bot

1. Buscar el bot en Telegram usando el nombre configurado
2. Iniciar una conversación con el comando `/start`
3. Enviar un enlace de YouTube válido
4. Esperar a que el video sea procesado
5. Realizar preguntas sobre el contenido del video

## Estructura del Proyecto

```
.
├── services/
│ ├── telegram_bot/
│ ├── video_processor/
│ ├── llm_service/
│ └── shared/
├── docker-compose.yml
└── README.md
```


## Características Principales

- Procesamiento asíncrono de videos
- Sistema de caché para resultados
- Transcripción automática de audio
- Respuestas contextuales usando IA
- Interfaz amigable a través de Telegram
- Arquitectura distribuida y escalable

## Limitaciones

- Solo procesa videos de YouTube
- El tamaño máximo del video puede estar limitado por recursos
- Las respuestas de IA dependen de la calidad de la transcripción
- El modelo TinyLlama tiene limitaciones en comparación con modelos más grandes

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
