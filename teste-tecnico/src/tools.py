from strands import tool
import re
import numexpr
import logging


logger = logging.getLogger("Tools")

# tool de cálculo criada ma nualmente como alternativa a tool padrão


@tool
def calculo(x: str) -> str:
    """
    Realiza cálculos numéricos.
    Use APENAS para expressões contendo números e operadores.
    NÃO use para perguntas de texto ou fatos históricos.

    Args:
        x (str): Expressão matemática.
    """
    entrada = x.strip()

    if entrada == "0" or entrada == "":
        return "Erro: Entrada inválida. Não use a tool para perguntas gerais."

    if not re.search(r'[\d+\-*/^=]', entrada):
        return "Erro: Envie expressões matemáticas."

    logger.info(
        " Cálculo DETECTADO (--> Tool de calculo acionada para essa pergunta <--) \n Expressão: %s", entrada)

    try:
        resultado = numexpr.evaluate(entrada).item()
        return f"Resultado: {resultado}"
    except SyntaxError:
        return "Erro: Verifique a expressão."
    except Exception as e:
        return f"Erro: {e}"
