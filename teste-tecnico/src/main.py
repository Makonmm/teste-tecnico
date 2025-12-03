from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import logging
import time
from src.agent import meu_agente
from src.cache import cache_em_memoria

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("API")


app = FastAPI(title="API Do Agente de IA",
              description="API que conecta o Agente com a tool solicitada, usando ollama",
              version="1.0.0")


# modelos

class ChatReq(BaseModel):  # requisição
    message: str
    model_config = {
        "json_schema_extra": {
            "examples": [{"message": "Quem é o autor do projeto? Me fale o que você sabe sobre ele?"}]
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
        cache_key = req.message.strip().lower()
        saved_resp = cache_em_memoria.get(cache_key)

        if saved_resp:
            logger.info(
                "HIT: Respondendo '%s' com armazenamento em cache", req.message)
            return ChatResp(response=saved_resp)

        logger.info("Mensagem (processando): %s", req.message)

        agent_resp = meu_agente(req.message)
        parsed_agent_resp = str(agent_resp)

        cache_em_memoria.set(cache_key, parsed_agent_resp)

        logger.info("\tResposta gerada e salva no cache.\n")

        return ChatResp(response=f"{parsed_agent_resp}")

    except Exception as e:
        logger.error(
            "Ocorreu algum erro ao tentar processar a mensagem: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
