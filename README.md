# Desafio Técnico - Vaga de Estágio em IA

> API de um Chat que usa um Agente de IA capaz de orquestrar raciocínio via LLM localmente e executar cálculos matemáticos através de tools 

## Arquitetura Da Solução Desenvolvida:

O programa adota uma arquitetura modular baseada no Agente. 
O Agente atua como um "orquestrador" que decide autonomamente quando utilizar ferramentas de cálculo ou quando responder utilizando seu próprio conhecimento de treinamento.



```mermaid
graph LR
    User[Usuário] -->|POST /chat| API[FastAPI + Cache]
    
    subgraph "Core (Orquestração)"
        API -->|Input| Agent{Agente Roteador}
        Agent <-->|Raciocínio| LLM[Ollama Llama 3.1]
    end
    
    subgraph "Execução de Tarefas"
        Agent -- Matemática --> Tool calculo[Ferramenta de Cálculo]
        Agent -- Sobre o Autor --> Tool about_me[Ferramenta de Info Autor]
        Agent -. Conhecimento Geral .-> Direct[Resposta Direta (conhecimento de treinamento)]
    end
    
    Tool calculo -->|Resultado Exato| Agent
    Tool about_me -->|Dados do Desenvolvedor| Agent
    Direct -.->|Texto Gerado| Agent
    
    Agent -->|JSON Final| API
    API -->|Response| User

```

## Uso
Para conseguir executar o projeto, você precisa ter o Ollama instalado e o Python 3.10+ (execução local) ou Docker (container)

1. Configuração do modelo:

```bash
ollama pull llama3.1
```

2. Instalação local:

```bash
# Clone o repositório

git clone https://github.com/Makonmm/teste-tecnico
cd teste-tecnico

# Crie o ambiente virtual e ative
# Windows:

python -m venv .venv
.venv\Scripts\activate

# Linux ou Mac:

python3 -m venv .venv
source .venv/bin/activate

# Instale as dependências do projeto

pip install -r requirements.txt

# Crie um arquivo .env com o seguinte conteúdo:

PORT=8000
HOST=0.0.0.0
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.1
USE_CUSTOM_TOOLS=true

```

3. Execução

```bash
# Inicia a API (projeto)

python manage.py api

# Esse comando apenas roda um teste para verificar se o agente está respondendo corretamente

python manage.py test

```

## Execução via Docker (Opcional)


### 1. Buildando a Imagem

No terminal (na raiz do projeto):

```bash
docker build -t agente-ia-api .
# Se for ambiente windows, rode:
docker run -d -p 8000:8000 --name meu-agente \
  -e OLLAMA_HOST="[http://host.docker.internal:11434](http://host.docker.internal:11434)" \
  agente-ia-api

# Caso seja Linux, rode:

docker run -d --network host --name meu-agente \
  -e OLLAMA_HOST="http://localhost:11434" \
  agente-ia-api

```
## Imagens
![Pergunta exemplo](teste-tecnico/images/1.PNG)
![Resposta](teste-tecnico/images/2.PNG)
![Resposta2](teste-tecnico/images/3.PNG)


## Referências 

Durante o desenvolvimento, as seguintes fontes foram consultadas:

* **Strands SDK:** A implementação do Agente segue a [Documentação Oficial do Strands Agents](https://strandsagents.com/latest/documentation/docs/).
* **Segurança:** A decisão de utilizar `numexpr` (funçã segura) ao invés de `eval()` (função insegura) baseou-se na prevenção de *Remote Code Execution (RCE)* e riscos de injeção detalhados no [OWASP Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html).
* **Performance (Cache):** A implementação do algoritmo **LRU (Least Recently Used)** para o cache em memória. Conceito detalhado em: [Cache Replacement Policies (Wikipedia)](https://en.wikipedia.org/wiki/Cache_replacement_policies#Least_recently_used_(LRU)).
* **Arquitetura (12-Factor App):** A estrutura do projeto segue os princípios do [The Twelve-Factor App](https://12factor.net/pt_br/), garantindo a separação de configurações (`.env`).
* **Orquestração do Agente (ReAct):** A lógica de ação do Agente foi inspirada no padrão *ReAct (Reason + Act)*, onde o modelo raciocina sobre a intenção do usuário antes de decidir invocar uma tool externa. Artigo: [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629).
* **LLM Local:** A configuração do Llama 3 para *Tool Calling* seguiu as diretrizes da [Ollama Library](https://ollama.com/library/llama3).
* **FastAPI Best Practices:** A estruturação modular, validação com Pydantic e uso de Middleware seguem a [Documentação Oficial do FastAPI](https://fastapi.tiangolo.com/).