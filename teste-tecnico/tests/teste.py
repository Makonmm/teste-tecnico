from src.agent import meu_agente

pergunta = input("Digite uma expressao matemática ou uma pergunta geral: ")
print(f"Pergunta: {pergunta}")
print("\n")
print("...(talvez leve um tempinho)")
print("\n")

resposta = meu_agente(pergunta)

print("\n" * 2)
print(f"Resposta do Agente: {resposta}")
