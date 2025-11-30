import numexpr
from strands import tool
from strands_tools import calculator


@tool
# tool de cálculo criada manualmente como alternativa a tool padrão
def calculo(x: str) -> str:
    """
    Função responsável pelos cálculos matemáticos.

    Args:
        x (str): A expressão matemática "x" a ser calculada.

    Returns:
        str: O resultado ou uma mensagem de erro.
    """

    try:
        limpa_entrada = x.strip()
        resultado = numexpr.evaluate(limpa_entrada).item()

        return f"Resultado: {resultado}"
    except SyntaxError:
        return f"Erro, verifique a expressão"
    except Exception as e:
        return f"Erro: {e}"
