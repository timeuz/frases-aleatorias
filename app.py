import os
import json
import random
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import google.generativeai as genai
import redis

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

# --- Configuração do Redis ---
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

redis_client = None
try:
    redis_client = redis.Redis(
        host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True
    )
    redis_client.ping()
    # Conexão com Redis estabelecida
except redis.exceptions.ConnectionError as e:
    print(
        f"Erro ao conectar ao Redis: {e}. O rate limiter e o armazenamento de frases podem não funcionar corretamente.",
        flush=True,
    )
    redis_client = None

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=(
        f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}" if redis_client else "memory://"
    ),
    strategy="fixed-window",
)

CATEGORIES = [
    "naos",
    "curiosidades",
    "frases_geek",
    "insultis",
    "desmotivacionais",
    "bomdia",
]


def load_json_file_to_redis(file_path, category_name):
    """
    Carrega frases de um arquivo JSON e as armazena em uma lista Redis.
    Cada frase é armazenada como um item na lista da chave 'phrases:<category_name>'.
    """
    redis_key = f"phrases:{category_name}"
    try:
        with open(file_path, encoding="utf-8") as json_file:
            phrases_data = json.load(json_file)

            if not isinstance(phrases_data, list):
                return f"Erro: O arquivo {file_path} não contém uma lista JSON."

            if redis_client:
                redis_client.delete(redis_key)
                for item in phrases_data:
                    if isinstance(item, str):
                        redis_client.rpush(redis_key, item)
                    else:
                        # Em caso de estrutura inesperada, tenta serializar
                        redis_client.rpush(redis_key, json.dumps(item))
                return None
            else:
                return f"Erro: Redis não conectado para carregar {file_path}."
    except FileNotFoundError:
        return f"Erro: Arquivo {file_path} não encontrado no diretório data/."
    except json.JSONDecodeError:
        return f"Erro: Arquivo {file_path} não é um JSON válido."
    except Exception as e:
        return f"Erro inesperado ao carregar {file_path} para Redis: {e}"


def load_phrases_from_redis_or_json():
    """
    Verifica se as frases já existem no Redis. Se não, carrega dos arquivos JSON e popula o Redis.
    """
    if not redis_client:
        print(
            "Redis não está conectado. As frases não serão carregadas para o Redis na inicialização.",
            flush=True,
        )
        return

    # Verificamos uma categoria como exemplo para saber se o Redis já está populado.
    # Se 'phrases:naos' existir, assumimos que todas as outras também foram carregadas.
    if redis_client.exists(f"phrases:{CATEGORIES[0]}"):
        # Frases já existem no Redis, pulando carregamento de JSONs.
        return

    # Frases não encontradas no Redis. Carregando dos arquivos JSONs e populando o Redis.
    for category in CATEGORIES:
        file_path = f"data/{category}.json"
        error = load_json_file_to_redis(file_path, category)
        if error:
            print(f"Falha ao carregar '{category}': {error}", flush=True)


# --- Configurações e Inicialização da IA ---
# Lendo as variáveis de ambiente. Usamos .get() para fornecer valores padrão.
IA_ATIVADA = os.getenv("IA_ATIVADA", "False").lower() == "true"
PERCENTUAL_IA = int(os.getenv("PERCENTUAL_IA", "0"))
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

gemini_model = None
if IA_ATIVADA and GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel("gemini-2.5-flash")  # Modelo Gemini
        # Modelo Gemini configurado com sucesso.
    except Exception as e:
        print(
            f"Erro ao configurar o modelo Gemini: {e}. A geração por IA estará desabilitada.",
            flush=True,
        )
        IA_ATIVADA = False
else:
    # Geração de IA desativada ou GEMINI_API_KEY não fornecida.
    pass  # Removido print aqui para manter logs limpos


# --- Funções para gerar frases (existentes e com IA) ---
def get_random_phrase_from_redis(category_name):
    """
    Retorna uma frase aleatória de uma categoria específica armazenada no Redis.
    Assume que as frases são armazenadas como strings simples no Redis.
    """
    redis_key = f"phrases:{category_name}"
    if not redis_client or not redis_client.exists(redis_key):
        return f"Nenhuma frase disponível para a categoria '{category_name}'.", 500

    list_length = redis_client.llen(redis_key)
    if list_length == 0:
        return f"Nenhuma frase disponível para a categoria '{category_name}'.", 500

    random_index = random.randint(0, list_length - 1)
    phrase_data = redis_client.lindex(redis_key, random_index)

    return phrase_data


def generate_phrase_with_ai(prompt):
    """Gera uma frase usando a API do Gemini com um prompt específico."""
    if not IA_ATIVADA or not gemini_model:
        return None

    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Erro ao chamar a API do Gemini com prompt '{prompt}': {e}", flush=True)
        return None


# --- Função auxiliar para decidir entre IA e frase existente por categoria ---
def get_phrase_for_category_with_ia_logic(category_name, ai_prompt_template):
    """
    Decide se gera uma frase com IA ou usa uma existente para a categoria,
    e retorna o JSON response.
    """
    if IA_ATIVADA and PERCENTUAL_IA > 0 and random.randint(1, 100) <= PERCENTUAL_IA:
        generated_phrase = generate_phrase_with_ai(ai_prompt_template)
        if generated_phrase:
            if redis_client:
                redis_key = f"phrases:{category_name}"
                redis_client.rpush(redis_key, generated_phrase)
                print(
                    f"Frase gerada por IA adicionada ao Redis na chave '{redis_key}'.",
                    flush=True,
                )
            return jsonify({"tipo": "IA", "frase": generated_phrase})
        else:
            # Fallback para existente se IA falhar
            frase = get_random_phrase_from_redis(category_name)
            if isinstance(frase, tuple):
                return jsonify({"tipo": "existente", "frase": frase[0]}), frase[1]
            return jsonify({"tipo": "existente", "frase": frase})
    else:
        # Pega frase existente
        frase = get_random_phrase_from_redis(category_name)
        if isinstance(frase, tuple):
            return jsonify({"tipo": "existente", "frase": frase[0]}), frase[1]
        return jsonify({"tipo": "existente", "frase": frase})


# --- Rotas da Aplicação ---
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/naos")
@limiter.limit("5 per second;10 per minute")
def naos():
    prompt_naos = "Gere apenas uma frase curta que expresse uma negação ou desaprovação de forma bem-humorada, irônica ou sarcástica."
    return get_phrase_for_category_with_ia_logic("naos", prompt_naos)


@app.route("/curiosidades")
@limiter.limit("5 per second;10 per minute")
def curiosidades():
    prompt_curiosidades = "Me mostre apenas uma curiosidade científica, histórica ou tecnológica REAL. O texto tem que ser curto. Ao fim da curiosidade informe a fonte seguindo o formato: 'Frase - Fonte'"
    return get_phrase_for_category_with_ia_logic("curiosidades", prompt_curiosidades)


@app.route("/frases_geek")
@limiter.limit("5 per second;10 per minute")
def frases_geek():
    prompt_geek = "Me mostre apenas uma citação inspiradora, divertida ou marcante com tema geek, de filmes, séries, jogos ou livros. Ao fim da citação informe de qual filme, série, jogo ou filme foi tirado e se for o caso, qual personagem que falou seguindo o formato: 'Frase - Origem - Personagem'"
    return get_phrase_for_category_with_ia_logic("frases_geek", prompt_geek)


@app.route("/insultis")
@limiter.limit("5 per second;10 per minute")
def insultis():
    prompt_insultis = (
        "Gere apenas um insulto inteligente, bem-humorado, irônico, sem ser ofensivo."
    )
    return get_phrase_for_category_with_ia_logic("insultis", prompt_insultis)


@app.route("/desmotivacionais")
@limiter.limit("5 per second;10 per minute")
def desmotivacionais():
    prompt_desmotivacionais = "Gere apenas uma frase desmotivacional curta e engraçada, com um tom sarcástico, irônico e criativamente pessimista"
    return get_phrase_for_category_with_ia_logic(
        "desmotivacionais", prompt_desmotivacionais
    )


@app.route("/bomdia")
@limiter.limit("5 per second;10 per minute")
def bomdia():
    prompt_bomdia = "Gere apenas uma frase de 'bom dia' irônica ou sarcástica, divertida mas com um toque de humor sombrio."
    return get_phrase_for_category_with_ia_logic("bomdia", prompt_bomdia)


@app.errorhandler(429)
def ratelimit_handler(e):
    return (
        f"Você excedeu o limite de requisições. Por favor, tente novamente mais tarde. Limite: {e.description}",
        429,
    )


# Carrega as frases para o Redis na inicialização da aplicação
load_phrases_from_redis_or_json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
