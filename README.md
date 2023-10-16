# Chatbot - BE

Este projeto é uma API backend desenvolvida em Python para fornecer funcionalidades de um chatbot e gerenciamento de perguntas e respostas.


## Características
 - Endpoint de pergunta e resposta
 - Cadastro de novas perguntas
 - Estrutura modular e escalável

## Requisitos
     - Python 3.6 ou superior
     - Flask
     - Outras bibliotecas listadas em requirements.txt

## Instalação e Configuração

1 - Clone o Repositório:
    git clone https://link-do-seu-repositorio.git
    cd nome-do-seu-projeto

2 - Crie um Ambiente Virtual (recomendado):
    python3 -m venv venv
    source venv/bin/activate  # No Windows use: venv\Scripts\activate

3 - Instale as Dependências:
    pip install -r requirements.txt

4 - Execute a api:
    python3 bot_api.py

## Isso irá iniciar o servidor Flask, e a API estará disponível em http://127.0.0.1:5000/.


## Endpoints
# Perguntar ao Chatbot:
    Método: POST
    URL: /pergunta
    Body: {"user_input": "sua pergunta aqui"}

# Adicionar Nova Pergunta:
    Método: POST
    URL: /add
    Body: {"question": "sua pergunta aqui", "answer": "resposta aqui"}



## Testes

Para executar os testes:
    pytest


## Documentação das APIs
    http://127.0.0.1:5000/apidocs/
