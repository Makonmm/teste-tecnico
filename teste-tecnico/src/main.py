from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from src.agent import meu_agente

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("API")


app = FastAPI(title="API Do Agente de IA",
              description="API que conectará o Agente com a tool solicitada, usando ollama",
              versin="1.0.0")


# modelos

class ChatReq(BaseModel):  # requisição
    message: str


class ChatResp(BaseModel):  # resposta
    response: str

# endpoints


@app.get("/", tags=["Health"], status_code=200)
def health_check():
    """
    Verifica o status da aplicação e retorna alguns metadados.
    """
    return {
        "status": "operational",
        "service": "api-agente-ia",
        "version": "1.0.0",
        "documentation": "/docs",
        "author": "https://github.com/Makonmm"
    }


@app.post("/chat", response_model=ChatResp, tags=["Chat"])
def chat_endpoint(req: ChatReq):
    """Esse endpoint receberá a PERGUNTA, depois passará para o agente, retornando a resposta"""

    try:
        logger.info(f"Mensagem: {req.message}")

        agent_resp = meu_agente(req.message)

        logger.info("\tResposta gerada\n")

        return ChatResp(response=f"{agent_resp}")

    except Exception as e:
        logger.error(f"Ocorreu algum erro ao tentar processar a mensagem: {e}")
        raise HTTPException(status_code=500, detail=str(e))
