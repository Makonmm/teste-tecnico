from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import logging
import time
from src.agent import meu_agente

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("API")


app = FastAPI(title="API Do Agente de IA",
              description="API que conecta o Agente com a tool solicitada, usando ollama",
              versin="1.0.0")


# modelos

class ChatReq(BaseModel):  # requisição
    message: str
    model_config = {
        "json_schema_extra": {
            "examples": [{"message": "Quanto é a raiz quadrada de 144 vezes 10? Primeiro tire a raiz quadrada de 144, depois multiplique o resultado por 10."}]
        }
    }


class ChatResp(BaseModel):  # resposta
    response: str


# middleware

@app.middleware("http")
async def process_time(request: Request, call_next):
    """Função que calcula (processa) o tempo que a resposta leva para chegar ao usuário"""
    start_time = time.time()
    response = await call_next(request)
    process = time.time() - start_time
    response.headers["X-Process-Time"] = str(round(process, 4))
    logger.info("TEMPO DE RESPOSTA: %ss", round(process, 4))

    return response

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
        logger.info("Mensagem: %s", req.message)

        agent_resp = meu_agente(req.message)

        logger.info("\tResposta gerada\n")

        return ChatResp(response=f"{agent_resp}\t")

    except Exception as e:
        logger.error(
            "Ocorreu algum erro ao tentar processar a mensagem: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
