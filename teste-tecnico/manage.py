import sys
import subprocess


def run_api():
    """Inicia a API usando o comando Uvicorn"""
    print("Comando recebido, executando...")

    cmd = [sys.executable, "-m", "uvicorn", "src.main:app", "--reload"]
    subprocess.run(cmd)


def run_test():
    """Roda o teste simples que verifica a integração com o ollama (se o modelo está respondendo)"""
    print("Rodando teste...")
    cmd = [sys.executable, "-m", "tests.teste"]
    subprocess.run(cmd)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Como usar: python manage.py [api|test]")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "api":
        run_api()
    elif command == "test":
        run_test()
    else:
        print(f"Esse comando: '{command}' não existe")
