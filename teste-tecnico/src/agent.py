import os
import logging
from strands import Agent
from dotenv import load_dotenv
from strands.models.ollama import OllamaModel


# Logs para entender o processo de execução do programa

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AgenteIA")

load_dotenv()

# Lógica para definir se o agente encotnrou a tool de calculo criada no arquivo tools.py, caso encontre, usará ela
# se não encontrar, ele usará a padrão do SDK(calculator)

use_custom = os.getenv("USE_CUSTOM_TOOLS")

if use_custom:
    try:
        from src.tools import calculo
        tool = calculo
        logger.info("Usando a tool criada (calculo)")
    except ImportError as e:
        logger.critical(
            f"Ocorreu um erro de import, verifique ")
        raise e
else:
    from strands_tools import calculator
    tool = calculator
    logger.info("Usando a tool padrão (calculator)")


def agente():
    """Cria a instância do Agente"""

    ollama_model = os.getenv("OLLAMA_MODEL", "llama3")
    host_ollama = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    modelo = OllamaModel(
        host=host_ollama,
        model_id=ollama_model,
        temperature=0.1
    )

    # criando o agente conforme a doc do strandsagents

    agent = Agent(name="Meu agente", model=modelo,


                  tools=[tool],
                  system_prompt=(
                      "Você é um Agente especialista que retorna respostas para uma API de maneira objetiva. "
                      "Sua tarefa é receber uma entrada e retornar APENAS a resposta final. "
                      "REGRAS: "
                      "1. NUNCA deixe seu raciocínio explícito na resposta(ex: 'Vou calcular...', 'A pergunta é...'). "
                      "2. NUNCA mencione que você usou uma tool"
                      "3. Se for um cálculo, retorne apenas o número ou a frase curta de resposta. "
                      "4. Se for uma pergunta geral, responda normalmente. "
                  )
                  )
    return agent


meu_agente = agente()
