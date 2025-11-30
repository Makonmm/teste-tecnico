import os
import logging
from typing import Any
from strands import Agent
from strands.models.ollama import OllamaModel
from dotenv import load_dotenv

# Logs para entender o processo de execução do programa
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AgenteIA")

load_dotenv()

SYSTEM_PROMPT = (
    "Você é um Agente especialista que retorna respostas para uma API de maneira objetiva. "
    "Sua tarefa é receber uma entrada e retornar a resposta final. "
    "REGRAS: "
    "1. NUNCA deixe seu raciocínio explícito na resposta (ex: 'Vou calcular...', 'A pergunta é...'). "
    "2. Se for um cálculo, retorne o resultado numérico ou frase curta. "
    "3. Quando você tiver usado a tool de cálculo, informe que ela foi usada **junto com o resultado**. "
    "   Exemplo: 'Usada a tool de cálculo. Resultado: 250'. "
    "4. Se for uma pergunta geral, responda normalmente. "
    "5. Você só deve utilizar a tool de cálculo quando a pergunta do usuário estiver relacionada com cálculos matemáticos (expressões). "
    "6. Você não deve usar a tool de cálculo em casos que não é necessário (perguntas que não têm relação com cálculos matemáticos). "
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
        tools=[tool_selecionada],
        system_prompt=SYSTEM_PROMPT
    )
    return agent


meu_agente = agente()
