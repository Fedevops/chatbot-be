import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import time
import requests


# def load_training_data(filename):
#     with open(filename, 'r', encoding='utf-8') as file:
#         lines = file.readlines()
#         qa_pairs = [tuple(line.strip().split('|')) for line in lines]
#     return qa_pairs


def load_training_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        # Aqui, vamos tentar processar cada linha e capturar possíveis erros
        qa_pairs = []
        for line in lines:
            try:
                q, a = line.strip().split('|')
                qa_pairs.append((q, a))
            except ValueError:
                print(f"Couldn't process line: {line.strip()}")

        return qa_pairs



def add_to_training_data(question, answer):
    with open("training_data.txt", "a") as file:
        file.write(f"{question}|{answer}\n")



def validate_facebook_token(access_token):
    # Verifique o token de acesso com a Graph API do Facebook
    graph_api_url = "https://graph.facebook.com/v12.0/me?fields=id,name,email&access_token=" + access_token
    response = requests.get(graph_api_url)
    data = response.json()

    # Em uma implementação real, você deve tratar possíveis erros,
    # como token inválido, problemas de rede, etc.
    if "error" in data:
        return None

    return data
