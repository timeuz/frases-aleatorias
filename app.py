import os
import json
from random import randrange
from flask import Flask, redirect, url_for, render_template_string, render_template, request, abort, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False 

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
    # storage_uri="redis://localhost:6379", # Exemplo para Redis (mais robusto para produção)
    # strategy="fixed-window" # Estratégia de janela (fixed-window é o padrão, leaky-bucket é mais suave)
)

all_phrases_data = {
    'naos': [],
    'curiosidades': [],
    'frases_geek': [],
    'insultis': [],
    'desmotivacionais': []
}

load_errors = {
    'naos': None,
    'curiosidades': None,
    'frases_geek': None,
    'insultis': None,
    'desmotivacionais': None
}

def load_json_file(file_path, category_name):
    try:
        with open(file_path, encoding="utf-8") as json_file:
            all_phrases_data[category_name] = json.load(json_file)
            load_errors[category_name] = None
    except FileNotFoundError:
        load_errors[category_name] = f"Erro: Arquivo {file_path} não encontrado no diretório data/."
        all_phrases_data[category_name] = []
    except json.JSONDecodeError:
        load_errors[category_name] = f"Erro: Arquivo {file_path} não é um JSON válido."
        all_phrases_data[category_name] = []
    except Exception as e:
        load_errors[category_name] = f"Erro inesperado ao carregar {file_path}: {e}"
        all_phrases_data[category_name] = []

load_json_file("data/naos.json", "naos")
load_json_file("data/curiosidades.json", "curiosidades")
load_json_file("data/frases_geek.json", "frases_geek")
load_json_file("data/insultis.json", "insultis")
load_json_file("data/desmotivacionais.json", "desmotivacionais")
load_json_file("data/bomdia.json", "bomdia")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/naos')
@limiter.limit("5 per second;10 per minute")
def naos():
    error_message = load_errors['naos']
    if error_message:
        return error_message, 500

    frases_list = all_phrases_data['naos']
    if not frases_list:
        return "Nenhuma frase 'não' disponível.", 500

    total_frases = len(frases_list)
    aleat = randrange(total_frases)
    aleat_frase = frases_list[aleat]
    return aleat_frase

@app.route('/curiosidades')
@limiter.limit("5 per second;10 per minute")
def curiosidades():
    error_message = load_errors['curiosidades']
    if error_message:
        return error_message, 500

    frases_list = all_phrases_data['curiosidades']
    if not frases_list:
        return "Nenhuma curiosidade disponível.", 500

    total_frases = len(frases_list)
    aleat = randrange(total_frases)
    aleat_frase = frases_list[aleat]
    return aleat_frase["fact"]

@app.route('/frases_geek')
@limiter.limit("5 per second;10 per minute")
def frases_geek():
    error_message = load_errors['frases_geek']
    if error_message:
        return error_message, 500

    frases_list = all_phrases_data['frases_geek']
    if not frases_list:
        return "Nenhuma citação geek disponível.", 500

    total_frases = len(frases_list)
    aleat = randrange(total_frases)
    aleat_frase = frases_list[aleat]
    return f"'{aleat_frase['quote']}' - {aleat_frase['character']} ({aleat_frase['source']})"

@app.route('/insultis')
@limiter.limit("5 per second;10 per minute")
def insultis():
    error_message = load_errors['insultis']
    if error_message:
        return error_message, 500

    frases_list = all_phrases_data['insultis']
    if not frases_list:
        return "Nenhum insulto sutil disponível.", 500

    total_frases = len(frases_list)
    aleat = randrange(total_frases)
    aleat_frase = frases_list[aleat]
    return aleat_frase["insult"]

@app.route('/desmotivacionais')
@limiter.limit("5 per second;10 per minute")
def desmotivacionais():
    error_message = load_errors['desmotivacionais']
    if error_message:
        return error_message, 500

    frases_list = all_phrases_data['desmotivacionais']
    if not frases_list:
        return "Nenhuma frase 'desmotivacional' disponível.", 500

    total_frases = len(frases_list)
    aleat = randrange(total_frases)
    aleat_frase = frases_list[aleat]
    return aleat_frase

@app.route('/bomdia')
@limiter.limit("5 per second;10 per minute")
def bomdia():
    error_message = load_errors['bomdia']
    if error_message:
        return error_message, 500

    frases_list = all_phrases_data['bomdia']
    if not frases_list:
        return "Nenhuma frase de 'bom dia' disponível.", 500

    total_frases = len(frases_list)
    aleat = randrange(total_frases)
    aleat_frase = frases_list[aleat]
    return aleat_frase

@app.errorhandler(429)
def ratelimit_handler(e):
    return f"Você excedeu o limite de requisições. Por favor, tente novamente mais tarde. Limite: {e.description}", 429
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)