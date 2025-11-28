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
        from src.tools import calc
        tool = calc
        logger.info("Usando a tool criada (calc)")
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
                  system_prompt=("Você é um especialista em cálculos matemáticos."
                                 "Sempre que o usuário enviar uma expressão matemática, USE a ferramenta matemática 'calc' para garantir precisão, não calcule por conta própria."
                                 "Para outros tipos de perguntas (que não envolvem expressões matemáticas), responda normalmente.")
                  )
    return agent


meu_agente = agente()
