import os
import logging
from src.tools import author
from typing import Any
from strands import Agent
from strands.models.ollama import OllamaModel
from dotenv import load_dotenv

# Logs para entender o processo de execução do programa
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AgenteIA")

load_dotenv()

SYSTEM_PROMPT = (
    "Você é um Agente de IA de uma API. Seu único objetivo é retornar a resposta final correta para o usuário.\n\n"

    "<protocolo_decisao>\n"
    "Para CADA mensagem, analise silenciosamente:\n"
    "1. É MATEMÁTICA PURA (ex: '10*10', 'raiz de 50', '5+5')? -> USE A TOOL 'calculo'.\n"
    "2. É CONHECIMENTO GERAL (ex: 'Quem é...', 'O que é...', 'Capital de...')? -> NÃO USE TOOL. Responda direto.\n"
    "3. É ÁLGEBRA/TEORIA (ex: 'Fórmula de Bhaskara', 'O que é derivada')? -> NÃO USE TOOL. Responda direto.\n"
    "4. É SOBRE O AUTOR/CRIADOR -> USE A TOOL 'author'.\n"
    "</protocolo_decisao>\n\n"

    "<regras_criticas>\n"
    "- PROIBIDO usar a tool 'calculo' para perguntas que não contenham números explícitos.\n"
    "- PROIBIDO retornar JSON interno (ex: {'name': 'None'}). Retorne apenas o texto da resposta.\n"
    "- Se a pergunta for sobre o Matheus Henrique ou sobre quem criou este projeto, USE a tool 'author'.\n"
    "- Se a pergunta for sobre uma PESSOA (ex: 'Quem é Messi', 'Quem foi Newton'), IGNORE a tool e responda com texto.\n"
    "- Responda de forma direta, sem introduções como 'A resposta é...'.\n"
    "</regras_criticas>\n\n"

    "<exemplos_few_shot>\n"
    "User: 'Qual a capital da França?'\n"
    "Assistant: Paris.\n\n"

    "User: 'Quanto é 123 * 4?'\n"
    "Assistant: [CHAMA TOOL calculo('123 * 4')]\n\n"

    "User: 'Quem foi Albert Einstein?'\n"
    "Assistant: Um físico teórico alemão famoso pela teoria da relatividade.\n\n"

    "User: 'Calcule a raiz de 144'\n"
    "Assistant: [CHAMA TOOL calculo('sqrt(144)')]\n"
    "</exemplos_few_shot>"
)


def _define_tool() -> Any:
    # Lógica para definir se o agente encotnrou a tool de calculo criada no arquivo tools.py, caso encontre, usará ela
    # se não encontrar, ele usará a padrão do SDK(calculator)
    use_custom = os.getenv("USE_CUSTOM_TOOLS")

    if use_custom:
        try:
            from src.tools import calculo
            logger.info("Usando a tool criada (calculo)")
            return calculo
        except ImportError as e:
            logger.critical("Ocorreu um erro de import, verifique ")
            raise e
    else:
        from strands_tools import calculator
        logger.info("Usando a tool padrão (calculator)")
        return calculator


def agente() -> Agent:
    """Cria a instância do Agente"""

    ollama_model = os.getenv("OLLAMA_MODEL", "llama3")
    host_ollama = os.getenv("OLLAMA_HOST", "http://localhost:11434")

    modelo = OllamaModel(
        host=host_ollama,
        model_id=ollama_model,
        temperature=0.1
    )

    tool_selecionada = _define_tool()

    # criando o agente conforme a doc do strandsagents
    agent = Agent(
        name="Meu agente",
        model=modelo,
        tools=[tool_selecionada, author],
        system_prompt=SYSTEM_PROMPT
    )
    return agent


meu_agente = agente()
