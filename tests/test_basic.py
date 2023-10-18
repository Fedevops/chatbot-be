# coding: utf-8
from flask_testing import TestCase
from bot_api import app


class APITest(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_ask_question(self):
        response = self.client.post('/pergunta', json={"user_input": "Qual o seu time do coração ?"})
        print(response)
        self.assert200(response)  # verifica se o status é 200 OK
        json_response = response.get_json()
        
        self.assertEqual(json_response["response"], "Bot diz: Palmeiras")


    def test_add_question(self):
        response = self.client.post('/add', json={
            "question": "O que é Python?",
            "answer": "Python é uma linguagem de programação."
        })
        
        self.assert200(response)  # verifica se o status é 200 OK
        json_response = response.get_json()
        
        self.assertEqual(json_response["success"], 'Dados adicionados com sucesso!')

