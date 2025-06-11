import os
import json
from random import randrange
from flask import Flask, redirect, url_for, render_template_string, request, abort, jsonify # Importado jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False 

# Configuração do Flask-Limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address, # Limitar por endereço IP remoto
    default_limits=["200 per day", "50 per hour"], # Limites padrão
    storage_uri="memory://", # Armazenamento em memória (bom para testes, mas não persistente entre reinícios)
    # storage_uri="redis://localhost:6379", # Exemplo para Redis (mais robusto para produção)
    # strategy="fixed-window" # Estratégia de janela (fixed-window é o padrão, leaky-bucket é mais suave)
)

# --- Estrutura para armazenar dados e erros de carregamento ---
# Dicionário para guardar todas as frases carregadas
all_phrases_data = {
    'naos': [],
    'science_facts': [],
    'geek_quotes': [],
    'subtle_insults': []
}

# Dicionário para guardar mensagens de erro de carregamento (se houver)
load_errors = {
    'naos': None,
    'science_facts': None,
    'geek_quotes': None,
    'subtle_insults': None
}

# Função auxiliar para carregar um arquivo JSON
def load_json_file(file_path, category_name):
    """
    Carrega um arquivo JSON e armazena os dados em all_phrases_data,
    e quaisquer erros em load_errors.
    """
    try:
        with open(file_path, encoding="utf-8") as json_file:
            all_phrases_data[category_name] = json.load(json_file)
            load_errors[category_name] = None # Limpa qualquer erro anterior se o carregamento for bem-sucedido
    except FileNotFoundError:
        load_errors[category_name] = f"Erro: Arquivo {file_path} não encontrado no diretório data/."
        all_phrases_data[category_name] = [] # Garante que a lista esteja vazia em caso de erro
    except json.JSONDecodeError:
        load_errors[category_name] = f"Erro: Arquivo {file_path} não é um JSON válido."
        all_phrases_data[category_name] = [] # Garante que a lista esteja vazia em caso de erro
    except Exception as e: # Captura qualquer outra exceção inesperada
        load_errors[category_name] = f"Erro inesperado ao carregar {file_path}: {e}"
        all_phrases_data[category_name] = [] # Garante que a lista esteja vazia em caso de erro

# --- Chame a função de carregamento para cada arquivo no início do app ---
load_json_file("data/naos.json", "naos")
load_json_file("data/science_facts.json", "science_facts")
load_json_file("data/geek_quotes.json", "geek_quotes")
load_json_file("data/subtle_insults.json", "subtle_insults")

# --- Rotas da Aplicação ---

@app.route('/')
def index():
    # Uma página simples para listar as rotas disponíveis
    return render_template_string("""
        <h1>Bem-vindo às Frases Aleatórias!</h1>
        <p>Acesse as seguintes rotas para obter uma frase:</p>
        <ul>
            <li><a href="/naoz">/naoz</a> - Frases de 'Não'</li>
            <li><a href="/science_facts">/science_facts</a> - Curiosidades Científicas</li>
            <li><a href="/geek_quotes">/geek_quotes</a> - Citações Geek (Filmes, Séries, Jogos)</li>
            <li><a href="/subtle_insults">/subtle_insults</a> - Insultos Sutis para Colegas</li>
        </ul>
        <p>Lembre-se dos limites de requisição!</p>
    """)

@app.route('/naos')
@limiter.limit("5 per second;10 per minute")
def naos():
    error_message = load_errors['naos']
    if error_message: # Verifica se houve um erro de carregamento
        return error_message, 500

    frases_list = all_phrases_data['naos'] # Pega a lista de frases para esta categoria
    if not frases_list: # Verifica se a lista está vazia (mesmo sem erro de arquivo)
        return "Nenhuma frase 'não' disponível.", 500 # Mensagem mais genérica para lista vazia

    total_frases = len(frases_list)
    aleat = randrange(total_frases)
    aleat_frase = frases_list[aleat]
    return aleat_frase

@app.route('/science_facts')
@limiter.limit("5 per second;10 per minute")
def science_facts():
    error_message = load_errors['science_facts']
    if error_message:
        return error_message, 500

    frases_list = all_phrases_data['science_facts']
    if not frases_list:
        return "Nenhuma curiosidade científica disponível.", 500

    total_frases = len(frases_list)
    aleat = randrange(total_frases)
    aleat_frase = frases_list[aleat]
    return aleat_frase["fact"]

@app.route('/geek_quotes')
@limiter.limit("5 per second;10 per minute")
def geek_quotes():
    error_message = load_errors['geek_quotes']
    if error_message:
        return error_message, 500

    frases_list = all_phrases_data['geek_quotes']
    if not frases_list:
        return "Nenhuma citação geek disponível.", 500

    total_frases = len(frases_list)
    aleat = randrange(total_frases)
    aleat_frase = frases_list[aleat]
    return f"'{aleat_frase['quote']}' - {aleat_frase['character']} ({aleat_frase['source']})"

@app.route('/subtle_insults')
@limiter.limit("5 per second;10 per minute")
def subtle_insults():
    error_message = load_errors['subtle_insults']
    if error_message:
        return error_message, 500

    frases_list = all_phrases_data['subtle_insults']
    if not frases_list:
        return "Nenhum insulto sutil disponível.", 500

    total_frases = len(frases_list)
    aleat = randrange(total_frases)
    aleat_frase = frases_list[aleat]
    return aleat_frase["insult"]

# --- Tratamento de Erro para Limite de Requisições ---
@app.errorhandler(429)
def ratelimit_handler(e):
    return f"Você excedeu o limite de requisições. Por favor, tente novamente mais tarde. Limite: {e.description}", 429
    
# --- Execução da Aplicação ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)