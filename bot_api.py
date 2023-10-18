from flask import Flask, request, jsonify, url_for, session, redirect
from main import SimpleSpacyBot, load_training_data, add_to_training_data
from flask_cors import CORS
from tools.tools import validate_facebook_token
from flasgger import Swagger, swag_from
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# db = SQLAlchemy(app)

CORS(app)
swagger = Swagger(app)
training_data = load_training_data("/home/fernando/projects/chatbot-be/chatbot-be/training_data.txt")

state = {
    'collecting_data': False,
    'data': {
        'nome': None,
        'telefone': None,
        'email': None
    }
} 

# state = {
#     'conversation': []
# }



# class Usuario(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     nome = db.Column(db.String(80))
#     telefone = db.Column(db.String(20))
#     email = db.Column(db.String(120))

#     def __repr__(self):
#         return '<Usuario %r>' % self.nome

# Inicialize o banco de dados
# db.create_all()


def bot_response(user_input):
    bot = SimpleSpacyBot()
    training_data = load_training_data("/home/fernando/projects/chatbot-be/chatbot-be/training_data.txt")
    bot.train(training_data)
    user_input = bot.respond(user_input)
  
    return user_input

@app.route('/')
def index():
    return 'Bem-vindo ao aplicativo Flask! <a href="/login">Login com Facebook</a>'




@app.route('/pergunta', methods=['POST'])
@swag_from({
    'tags': ['Perguntas'],
    'description': 'Endpoint para fazer uma pergunta ao bot',
    'consumes': ['application/json'],
    'produces': ['application/json'],
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': 'true',
        'schema': {
            'id': 'UserInput',
            'required': ['question'],
            'properties': {
                'question': {
                    'type': 'string',
                    'description': 'A pergunta que o usuário deseja fazer'
                }
            }
        }
    }],
    'responses': {
        '200': {
            'description': 'Resposta do bot',
            'schema': {
                'type': 'object',
                'properties': {
                    'answer': {
                        'type': 'string',
                        'description': 'Resposta do bot à pergunta do usuário'
                    }
                }
            }
        },
        '400': {
            'description': 'Requisição inválida'
        }
    }
})
def ask_bot():
    data = request.get_json()
    user_input = data.get("user_input")
    if user_input == "sair":
        state['conversation'] = []  # Limpa o estado/conversação
        return jsonify({"response": "Conversa reiniciada."})
    
    if not user_input:
        return jsonify({"response": "Olá! Como posso ajudar você hoje?"})
    
    if 'quero agendar' in user_input:
        state['collecting_data'] = True
        return jsonify({"response": "Por favor, insira o seu nome:"})
    

    if state['collecting_data']:
        if state['data']['nome'] is None:
            state['data']['nome'] = user_input
            return jsonify({"response": "Obrigado! Agora, por favor insira o seu telefone:"})

        elif state['data']['telefone'] is None:
            state['data']['telefone'] = user_input
            return jsonify({"response": "Obrigado! Por favor, insira o seu e-mail:"})

        elif state['data']['email'] is None:
            state['data']['email'] = user_input
            state['collecting_data'] = False  # Termina a coleta de dados
            # Salvando no banco de dados
            novo_usuario = Usuario(nome=state['data']['nome'], telefone=state['data']['telefone'], email=state['data']['email'])
            db.session.add(novo_usuario)
            db.session.commit()
            return jsonify({"response": "Obrigado! Seus dados foram coletados com sucesso."})
             
    # if not user_input:
    #     return jsonify({"error": "Input não foi fornecido."}), 400

    response = bot_response(user_input)
    # state['conversation'].append({'user': user_input, 'bot': response})

    return jsonify({"response": response})



@app.route('/add', methods=['POST'])
@swag_from({
    'tags': ['Adicionar Perguntas'],
    'description': 'Endpoint para adicionar novas perguntas e respostas',
    'consumes': ['application/json'],
    'produces': ['application/json'],
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': 'true',
        'schema': {
            'id': 'QuestionAnswerPair',
            'required': ['question', 'answer'],
            'properties': {
                'question': {
                    'type': 'string',
                    'description': 'A pergunta que será adicionada'
                },
                'answer': {
                    'type': 'string',
                    'description': 'A resposta correspondente à pergunta'
                }
            }
        }
    }],
    'responses': {
        '200': {
            'description': 'Pergunta e resposta adicionadas com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'description': 'Mensagem de confirmação'
                    }
                }
            }
        },
        '400': {
            'description': 'Requisição inválida'
        }
    }
})
def add_data():
    data = request.get_json()
    question = data.get("question")
    answer = data.get("answer")

    if not question or not answer:
        return jsonify({"error": "Pergunta e resposta são necessárias!"}), 400

    add_to_training_data(question, answer)
    return jsonify({"success": "Dados adicionados com sucesso!"})






# @app.route('/autentica/facebook', methods=['POST'])
# @swag_from({
#     'responses': {
#         200: {
#             'description': 'Usuário autenticado',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'message': {
#                         'type': 'string'
#                     }
#                 }
#             }
#         }
#     },
#     'parameters': [{
#         'name': 'access_token',
#         'in': 'formData',
#         'type': 'string',
#         'required': 'true',
#         'description': 'Token de acesso do Facebook'
#     }],
#     'tags': ['Autenticação com Facebook']
# })
# def facebook_auth():
#     access_token = request.json.get('access_token')
    
#     if not access_token:
#         return jsonify(message="Access token missing"), 400

#     # Valide o token de acesso e obtenha informações do usuário
#     user_info = validate_facebook_token(access_token)

#     if not user_info:
#         return jsonify(message="Invalid token or could not fetch user info"), 400

#     # Aqui, você pode criar uma sessão para o usuário ou emitir um token JWT, por exemplo.
#     # Por simplicidade, estamos apenas retornando as informações do usuário.

#     return jsonify(user_info)


# @app.route('/relatorio', methods=['GET'])
# def relatorio():
#     usuarios = Usuario.query.all()
#     return jsonify([{'nome': u.nome, 'telefone': u.telefone, 'email': u.email} for u in usuarios])



@app.route('/apidocs/')
def swagger_ui():
    return flasgger.render_template(app, ["/auth/facebook"])



if __name__ == '__main__':
    # with app.app_context():
        # db.create_all()
    app.run(debug=True)

# db.init_app(app)






