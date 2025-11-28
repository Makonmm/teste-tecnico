from src.agent import meu_agente

pergunta = "Quanto é 10 elevado a 6?"
print("\n")
print(f"Pergunta: {pergunta}")
print("\n")
print("Aguarde...(talvez leve um tempinho)")

resposta = meu_agente(pergunta)

print("\n" * 2)
print(f"Resposta do Agente: {resposta}")
