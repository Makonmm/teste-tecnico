from strands import tool
import re
import numexpr
import logging


logger = logging.getLogger("Tools")

# tool de cálculo criada manualmente como alternativa a tool padrão


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

# tool que  agente usa para falar algumas informações sobre o autor do projeto.


@tool
# usei "pergunta" como um dummy argument para o agente.
def about_me(pergunta: str) -> str:
    """Retorna informações sobre o desenvolvedor do projeto (Matheus Henrique).

    Quando usar:
    - Quando perguntarem algo relacionado ao autor do projeto, como: "Quem te criou?", "Quem criou isso?, "Quem é o autor?", "Fale sobre o Matheus"   

    """
    logger.info("Tool about me acionada")
    return (
        "---- Informações sobre o autor ----\n"
        "Nome: Matheus Henrique\n"
        "Perfil: Estudante de Ciência Da Computação, apaixonado por IA e Cibersegurança.\n"
        "Algumas implementações do projeto: Segurança anti-RCE, Dockerização, Caching e Arquitetura de IA 'Neuro-simbólica.'\n"
        "Quer saber mais? Verifique no Linkedin: https://www.linkedin.com/in/matheus-henrique-ramos-siqueira-890052200/"
    )
