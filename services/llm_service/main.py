from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from services.llm_service.src.llm_model import generate_response
from shared.utils.logger import setup_logger

logger = setup_logger()

app = FastAPI()


class QuestionRequest(BaseModel):
    transcription: str
    question: str
    title: str


@app.post("/generate-response")
async def generate_response_endpoint(request: QuestionRequest):
    try:
        logger.info("Recibiendo solicitud para generar una respuesta.")

        # Generar la respuesta usando el modelo de IA
        response = generate_response(
            request.transcription, request.question, request.title
        )

        logger.info("Proceso completado exitosamente.")
        return {"response": response}
    except Exception as e:
        logger.error(f"Error al generar la respuesta: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
